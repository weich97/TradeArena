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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run a small provider-backed model matrix and write redacted benchmark manifests."
    )
    parser.add_argument("--models", default=",".join(DEFAULT_MODELS), help="Comma-separated provider:model entries.")
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
    output_dir.mkdir(parents=True, exist_ok=True)
    submission_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)

    symbols = tuple(symbol.strip() for symbol in args.symbols.split(",") if symbol.strip())
    model_specs = [_parse_model_spec(item) for item in args.models.split(",") if item.strip()]
    rows: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []

    for provider, model in model_specs:
        try:
            row = _run_one(
                provider=provider,
                model=model,
                symbols=symbols,
                periods=args.periods,
                seed=args.seed,
                output_dir=output_dir,
                submission_dir=submission_dir,
                cache_dir=cache_dir,
            )
            rows.append(row)
            print(f"OK {provider}:{model} -> {row['submission']}")
        except Exception as exc:  # pragma: no cover - exercised only by live provider failures
            failures.append({"provider": provider, "model": model, "error": type(exc).__name__})
            print(f"FAILED {provider}:{model}: {type(exc).__name__}: {exc}", file=sys.stderr)

    _write_matrix_table(output_dir / "leaderboard_model_matrix.csv", rows)
    _write_matrix_markdown(output_dir / "leaderboard_model_matrix.md", rows, failures)
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
    symbols: tuple[str, ...],
    periods: int,
    seed: int,
    output_dir: Path,
    submission_dir: Path,
    cache_dir: Path,
) -> dict[str, Any]:
    slug = _slug(f"{provider}-{model}")
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
        llm_cache_path=str(cache_dir / f"{slug}.jsonl"),
        llm_mask_timestamps=True,
        llm_use_risk_feedback=True,
        llm_risk_feedback_mode="true",
    ).run()

    parse_coverage = _parse_coverage(trajectory.to_dict(), symbols)
    summary = {
        "schema_version": "0.1",
        "scenario_id": "leaderboard_llm_smoke_synthetic_v0_1",
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
            "scenario_id": "leaderboard_llm_smoke_synthetic_v0_1",
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
                "data_hash": f"sha256:synthetic-seed-{seed}-symbols-{'-'.join(symbols)}-periods-{periods}",
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


def _write_matrix_markdown(path: Path, rows: list[dict[str, Any]], failures: list[dict[str, str]]) -> None:
    lines = [
        "# Leaderboard Model Matrix",
        "",
        "This table is generated by `python scripts/run_leaderboard_model_matrix.py --update-registry`.",
        "It records redacted smoke-test manifests only; raw provider prompts and responses remain in ignored local caches.",
        "",
        "| Provider | Model | Parse | Return | Max DD | Sharpe | Fill | Rejected | Risk edits | Submission |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
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


def _slug(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "_", value).strip("_").lower()


def _rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def _fmt(value: Any) -> str:
    return f"{float(value):.4f}"


if __name__ == "__main__":
    raise SystemExit(main())
