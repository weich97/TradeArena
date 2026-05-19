from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from tradearena.core.reproducibility import attach_reproducibility_hash, sha256_file  # noqa: E402
from tradearena.factory import build_default_system  # noqa: E402


DEFAULT_MODELS = (
    "poe:gpt-5.5",
    "poe:gemini-3.1-pro",
    "poe:kimi-k2.5",
    "poe:glm-5",
    "poe:claude-opus-4.7",
    "deepseek:deepseek-v4-flash",
    "deepseek:deepseek-v4-pro",
)

SCENARIOS: dict[str, dict[str, Any]] = {
    "calm_trend": {
        "scenario_id": "leaderboard_llm_calm_trend_synthetic_v0_1",
        "label": "Calm trend",
        "seed_offset": 0,
        "synthetic": {
            "synthetic_volatility_scale": 1.0,
            "synthetic_trend_scale": 1.0,
            "synthetic_seasonal_scale": 1.0,
            "synthetic_macro_scale": 1.0,
        },
    },
    "high_vol": {
        "scenario_id": "leaderboard_llm_high_vol_synthetic_v0_1",
        "label": "High volatility",
        "seed_offset": 10,
        "synthetic": {
            "synthetic_volatility_scale": 2.25,
            "synthetic_trend_scale": 0.65,
            "synthetic_seasonal_scale": 1.2,
            "synthetic_macro_scale": 1.4,
        },
    },
    "jump_tail": {
        "scenario_id": "leaderboard_llm_jump_tail_synthetic_v0_1",
        "label": "Jump and tail risk",
        "seed_offset": 22,
        "synthetic": {
            "synthetic_volatility_scale": 1.65,
            "synthetic_trend_scale": 0.85,
            "synthetic_seasonal_scale": 1.0,
            "synthetic_macro_scale": 1.5,
            "synthetic_tail_df": 3,
            "synthetic_jump_probability": 0.15,
            "synthetic_jump_scale": 0.08,
        },
    },
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run a small provider-backed model matrix and write redacted benchmark manifests."
    )
    parser.add_argument("--models", default=",".join(DEFAULT_MODELS), help="Comma-separated provider:model entries.")
    parser.add_argument(
        "--scenarios",
        default="calm_trend,high_vol,jump_tail",
        help=f"Comma-separated scenario presets. Available: {', '.join(SCENARIOS)}.",
    )
    parser.add_argument("--periods", type=int, default=8)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--symbols", default="SYN,ALT")
    parser.add_argument("--output-dir", default="docs/results/model_matrix")
    parser.add_argument("--submission-dir", default="examples/benchmark_submissions/model_matrix")
    parser.add_argument("--cache-dir", default="outputs/llm_cache/leaderboard_model_matrix")
    parser.add_argument("--update-registry", action="store_true")
    args = parser.parse_args(argv)

    output_dir = ROOT / args.output_dir
    submission_dir = ROOT / args.submission_dir
    cache_dir = ROOT / args.cache_dir
    _clean_generated_dir(output_dir)
    _clean_generated_dir(submission_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    submission_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)

    symbols = tuple(symbol.strip() for symbol in args.symbols.split(",") if symbol.strip())
    model_specs = [_parse_model_spec(item) for item in args.models.split(",") if item.strip()]
    scenarios = [_scenario(name) for name in args.scenarios.split(",") if name.strip()]
    rows: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []

    for scenario in scenarios:
        for provider, model in model_specs:
            try:
                row = _run_one(
                    provider=provider,
                    model=model,
                    scenario=scenario,
                    symbols=symbols,
                    periods=args.periods,
                    seed=args.seed + int(scenario["seed_offset"]),
                    output_dir=output_dir,
                    submission_dir=submission_dir,
                    cache_dir=cache_dir,
                )
                rows.append(row)
                print(f"OK {row['scenario_key']} {provider}:{model} -> {row['submission']}")
            except Exception as exc:  # pragma: no cover - exercised only by live provider failures
                failures.append(
                    {
                        "scenario": str(scenario["key"]),
                        "provider": provider,
                        "model": model,
                        "error": type(exc).__name__,
                    }
                )
                print(
                    f"FAILED {scenario['key']} {provider}:{model}: {type(exc).__name__}: {exc}",
                    file=sys.stderr,
                )

    _write_matrix_table(output_dir / "leaderboard_model_matrix.csv", rows)
    aggregate_rows = _aggregate_rows(rows)
    _write_aggregate_table(output_dir / "leaderboard_model_matrix_aggregate.csv", aggregate_rows)
    _write_matrix_markdown(output_dir / "leaderboard_model_matrix.md", rows, aggregate_rows, failures)
    if failures:
        (output_dir / "leaderboard_model_matrix_failures.json").write_text(
            json.dumps(failures, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    if args.update_registry:
        from tradearena.evaluation.submissions import build_registry_rows, write_registry_html, write_registry_markdown

        registry_rows, errors = build_registry_rows(ROOT / "examples" / "benchmark_submissions")
        if errors:
            raise RuntimeError("Registry build failed:\n" + "\n".join(errors))
        for row in registry_rows:
            source_file = Path(str(row.get("source_file", "")))
            if source_file.is_absolute():
                try:
                    row["source_file"] = source_file.resolve().relative_to(ROOT).as_posix()
                except ValueError:
                    row["source_file"] = source_file.as_posix()
        write_registry_markdown(registry_rows, ROOT / "docs/results/community_registry.md")
        write_registry_html(registry_rows, ROOT / "docs/results/community_registry.html")
        _write_registry_csv(registry_rows, ROOT / "docs/results/community_registry.csv")

    print(f"Successful model rows: {len(rows)}")
    if failures:
        print(f"Failed model rows: {len(failures)}")
    return 0 if rows else 1


def _run_one(
    *,
    provider: str,
    model: str,
    scenario: dict[str, Any],
    symbols: tuple[str, ...],
    periods: int,
    seed: int,
    output_dir: Path,
    submission_dir: Path,
    cache_dir: Path,
) -> dict[str, Any]:
    model_slug = _slug(f"{provider}-{model}")
    scenario_key = str(scenario["key"])
    slug = f"{scenario_key}__{model_slug}"
    analyst_name = "poe-llm" if provider == "poe" else "deepseek-llm"
    trajectory, metrics = build_default_system(
        name=f"leaderboard_{slug}",
        symbols=symbols,
        periods=periods,
        seed=seed,
        analyst_names=(analyst_name,),
        strategy_name="signal-weighted",
        risk_name="max-position",
        execution_mode="realistic",
        llm_model=model,
        llm_cache_path=str(cache_dir / f"{model_slug}.jsonl"),
        llm_mask_timestamps=True,
        llm_use_risk_feedback=True,
        llm_risk_feedback_mode="true",
        **scenario["synthetic"],
    ).run()

    parse_coverage = _parse_coverage(trajectory.to_dict(), symbols)
    summary = {
        "schema_version": "0.1",
        "scenario_id": scenario["scenario_id"],
        "scenario_label": scenario["label"],
        "provider": provider,
        "model": model,
        "symbols": list(symbols),
        "periods": periods,
        "seed": seed,
        "parse_coverage": parse_coverage,
        "metrics": metrics,
        "redaction": {
            "raw_prompts_included": False,
            "raw_responses_included": False,
            "timestamps_masked": True,
        },
    }
    summary_path = output_dir / f"{slug}_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary_hash = sha256_file(summary_path)

    submission = attach_reproducibility_hash(
        {
            "schema_version": "0.1",
            "scenario_id": scenario["scenario_id"],
            "agent": {
                "provider": provider,
                "agent_type": "llm_policy",
                "model_family": model,
                "model_display_name": model,
                "model_identifier_redacted": False,
                "prompt_mode": "rationale",
                "risk_feedback_mode": "true",
                "parse_coverage": parse_coverage,
                "response_format": "json_object",
                "prompt_version": "risk-feedback-v1",
                "agent_commit": "redacted-or-local",
            },
            "data_source": {
                "name": "synthetic-market",
                "frequency": "daily",
                "symbols": list(symbols),
                "timestamp_policy": "relative_masked",
                "data_hash": (
                    f"sha256:{scenario_key}-synthetic-seed-{seed}-symbols-"
                    f"{'-'.join(symbols)}-periods-{periods}"
                ),
            },
            "execution_config": {
                "commission_bps": 1.0,
                "base_slippage_bps": 2.0,
                "spread_bps": 0.0,
                "latency_steps": 1,
                "participation_rate": 0.05,
                "market_impact": 0.15,
            },
            "risk_config": {
                "risk_manager": "max-position",
                "risk_budget": {
                    "max_position_weight": 0.35,
                    "max_gross_exposure": 1.0,
                    "max_single_step_turnover": 0.75,
                    "risk_feedback_mode": "true",
                },
            },
            "metrics": {
                "total_return": float(metrics.get("total_return", 0.0)),
                "max_drawdown": float(metrics.get("max_drawdown", 0.0)),
                "sharpe": float(metrics.get("sharpe", 0.0)),
                "execution_fill_rate": float(metrics.get("execution_fill_rate", 0.0)),
                "rejected_order_count": int(metrics.get("rejected_order_count", 0)),
                "risk_clipped_decisions": int(metrics.get("risk_clipped_decisions", 0)),
                "risk_violation_count": int(metrics.get("risk_violation_count", 0)),
                "trajectory_reproducibility_coverage": float(
                    metrics.get("trajectory_reproducibility_coverage", 0.0)
                ),
            },
            "trajectory_manifest": {
                "format": "redacted_manifest",
                "path_or_uri": _rel(summary_path),
                "raw_prompts_included": False,
                "raw_responses_included": False,
                "manifest_hash": summary_hash,
                "artifact_hashes": {"redacted_summary": summary_hash},
            },
            "redaction": {
                "provider_secrets_removed": True,
                "timestamps_masked": True,
                "raw_provider_text_removed": True,
                "notes": (
                    "Leaderboard smoke manifest generated from a live or cache-backed provider run; "
                    "raw prompts and responses remain in ignored local cache files."
                ),
            },
        }
    )
    submission_path = submission_dir / f"{slug}.json"
    submission_path.write_text(json.dumps(submission, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return {
        "scenario_key": scenario_key,
        "scenario_id": scenario["scenario_id"],
        "scenario_label": scenario["label"],
        "provider": provider,
        "model": model,
        "parse_coverage": parse_coverage,
        "total_return": submission["metrics"]["total_return"],
        "max_drawdown": submission["metrics"]["max_drawdown"],
        "sharpe": submission["metrics"]["sharpe"],
        "execution_fill_rate": submission["metrics"]["execution_fill_rate"],
        "rejected_order_count": submission["metrics"]["rejected_order_count"],
        "risk_clipped_decisions": submission["metrics"]["risk_clipped_decisions"],
        "reproducibility_hash": submission["reproducibility_hash"],
        "submission": _rel(submission_path),
        "summary": _rel(summary_path),
    }


def _parse_model_spec(value: str) -> tuple[str, str]:
    if ":" in value:
        provider, model = value.split(":", 1)
    else:
        provider, model = "poe", value
    provider = provider.strip().lower()
    model = model.strip()
    if provider not in {"poe", "deepseek"}:
        raise ValueError(f"Unsupported provider in model spec: {value}")
    if not model:
        raise ValueError(f"Missing model name in model spec: {value}")
    return provider, model


def _scenario(name: str) -> dict[str, Any]:
    key = name.strip()
    if key not in SCENARIOS:
        raise ValueError(f"Unknown scenario preset: {key}. Available: {', '.join(SCENARIOS)}")
    scenario = dict(SCENARIOS[key])
    scenario["key"] = key
    scenario["synthetic"] = dict(scenario["synthetic"])
    return scenario


def _parse_coverage(trajectory: dict[str, Any], symbols: tuple[str, ...]) -> float:
    steps = trajectory.get("steps", [])
    expected = max(1, len(steps) * max(1, len(symbols)))
    observed = 0
    for step in steps:
        signals = step.get("signals", []) if isinstance(step, dict) else []
        if isinstance(signals, list):
            observed += sum(1 for signal in signals if isinstance(signal, dict) and signal.get("symbol") in symbols)
    return round(min(1.0, observed / expected), 4)


def _write_matrix_table(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = [
        "scenario_key",
        "scenario_id",
        "scenario_label",
        "provider",
        "model",
        "parse_coverage",
        "total_return",
        "max_drawdown",
        "sharpe",
        "execution_fill_rate",
        "rejected_order_count",
        "risk_clipped_decisions",
        "reproducibility_hash",
        "submission",
        "summary",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _aggregate_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault((str(row["provider"]), str(row["model"])), []).append(row)
    aggregate_rows = []
    for (provider, model), model_rows in sorted(grouped.items()):
        aggregate_rows.append(
            {
                "provider": provider,
                "model": model,
                "scenario_count": len(model_rows),
                "avg_return": _avg(row["total_return"] for row in model_rows),
                "worst_drawdown": min(float(row["max_drawdown"]) for row in model_rows),
                "avg_sharpe": _avg(row["sharpe"] for row in model_rows),
                "avg_fill_rate": _avg(row["execution_fill_rate"] for row in model_rows),
                "total_rejected_orders": sum(int(row["rejected_order_count"]) for row in model_rows),
                "total_risk_edits": sum(int(row["risk_clipped_decisions"]) for row in model_rows),
                "avg_parse_coverage": _avg(row["parse_coverage"] for row in model_rows),
            }
        )
    return sorted(
        aggregate_rows,
        key=lambda row: (
            -float(row["avg_return"]),
            float(row["worst_drawdown"]),
            -float(row["avg_fill_rate"]),
        ),
    )


def _write_aggregate_table(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = [
        "provider",
        "model",
        "scenario_count",
        "avg_return",
        "worst_drawdown",
        "avg_sharpe",
        "avg_fill_rate",
        "total_rejected_orders",
        "total_risk_edits",
        "avg_parse_coverage",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_matrix_markdown(
    path: Path,
    rows: list[dict[str, Any]],
    aggregate_rows: list[dict[str, Any]],
    failures: list[dict[str, str]],
) -> None:
    lines = [
        "# Leaderboard Model Matrix",
        "",
        "This table is generated by `python scripts/run_leaderboard_model_matrix.py --update-registry`.",
        "It records redacted model manifests only; raw provider prompts and responses remain in ignored local caches.",
        "",
        "## Cross-Scenario Aggregate",
        "",
        "| Rank | Provider | Model | Scenarios | Avg return | Worst DD | Avg Sharpe | Avg fill | Rejected | Risk edits | Parse |",
        "| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for rank, row in enumerate(aggregate_rows, start=1):
        lines.append(
            "| "
            + " | ".join(
                [
                    str(rank),
                    str(row["provider"]),
                    str(row["model"]),
                    str(row["scenario_count"]),
                    _fmt(row["avg_return"]),
                    _fmt(row["worst_drawdown"]),
                    _fmt(row["avg_sharpe"]),
                    _fmt(row["avg_fill_rate"]),
                    str(row["total_rejected_orders"]),
                    str(row["total_risk_edits"]),
                    _fmt(row["avg_parse_coverage"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Scenario Rows",
        "",
            "| Scenario | Provider | Model | Parse | Return | Max DD | Sharpe | Fill | Rejected | Risk edits | Submission |",
            "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["scenario_label"]),
                    str(row["provider"]),
                    str(row["model"]),
                    _fmt(row["parse_coverage"]),
                    _fmt(row["total_return"]),
                    _fmt(row["max_drawdown"]),
                    _fmt(row["sharpe"]),
                    _fmt(row["execution_fill_rate"]),
                    str(row["rejected_order_count"]),
                    str(row["risk_clipped_decisions"]),
                    f"[manifest](../../{row['submission']})",
                ]
            )
            + " |"
        )
    if failures:
        lines.extend(["", "## Provider Failures", ""])
        for failure in failures:
            lines.append(f"- `{failure['provider']}:{failure['model']}` failed with `{failure['error']}`.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_registry_csv(rows: list[dict[str, object]], path: Path) -> None:
    fieldnames = list(rows[0]) if rows else ["scenario_id"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _clean_generated_dir(path: Path) -> None:
    if not path.exists():
        return
    for child in path.iterdir():
        if child.is_file() and child.suffix.lower() in {".json", ".csv", ".md"}:
            child.unlink()


def _slug(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "_", value).strip("_").lower()


def _rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def _fmt(value: Any) -> str:
    return f"{float(value):.4f}"


def _avg(values: Any) -> float:
    numbers = [float(value) for value in values]
    return sum(numbers) / len(numbers) if numbers else 0.0


if __name__ == "__main__":
    raise SystemExit(main())
