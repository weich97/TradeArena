from __future__ import annotations

import csv
from pathlib import Path

from trading_agent_os.core.serialization import write_json
from trading_agent_os.factory import build_default_system


OUTPUT_DIR = Path("outputs/examples")


def main() -> int:
    cases = [
        ("ideal_no_friction", {"execution_mode": "ideal", "commission_bps": 0.0, "slippage_bps": 0.0}),
        ("realistic_default", {"execution_mode": "realistic"}),
        (
            "low_liquidity",
            {"execution_mode": "realistic", "participation_rate": 0.015, "market_impact": 0.38, "slippage_bps": 5.0},
        ),
        (
            "high_latency",
            {"execution_mode": "realistic", "latency_steps": 4, "participation_rate": 0.03, "market_impact": 0.24},
        ),
    ]
    rows = []
    for name, overrides in cases:
        _, metrics = build_default_system(
            name=f"execution_realism_{name}",
            symbols=("SYN", "ALT", "DEF"),
            periods=50,
            seed=19,
            strategy_name="signal-weighted",
            risk_name="max-position",
            max_position_weight=0.28,
            **overrides,
        ).run()
        rows.append(
            {
                "case": name,
                "total_return": metrics["total_return"],
                "max_drawdown": metrics["max_drawdown"],
                "fill_rate": metrics["execution_fill_rate"],
                "partial_fill_rate": metrics["partial_fill_rate"],
                "rejected_orders": metrics["rejected_order_count"],
                "pending_orders": metrics["pending_order_count"],
                "slippage_cost": metrics["total_slippage_cost"],
                "commission": metrics["total_commission"],
            }
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUTPUT_DIR / "execution_realism_sweep_summary.json", {"rows": rows})
    _write_csv(OUTPUT_DIR / "execution_realism_sweep.csv", rows)
    _write_svg(OUTPUT_DIR / "execution_realism_sweep.svg", rows)

    print("Execution realism sweep demo")
    for row in rows:
        print(
            f"  {row['case']}: return={row['total_return']:.4f} "
            f"fill={row['fill_rate']:.3f} slippage={row['slippage_cost']:.1f} rejected={row['rejected_orders']}"
        )
    print(f"\nWrote {OUTPUT_DIR / 'execution_realism_sweep.svg'}")
    return 0


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _write_svg(path: Path, rows: list[dict[str, object]]) -> None:
    width, height = 920, 360
    max_slip = max(1.0, max(float(row["slippage_cost"]) for row in rows))
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Execution realism sweep">',
        '<rect width="100%" height="100%" fill="#f8fafc"/>',
        _text(36, 44, "Execution realism changes the measured strategy", 22, "#0f172a", 800),
        _text(36, 72, "Same agent and market, different simulator frictions: ideal fills, liquidity, latency, slippage, rejections.", 13, "#64748b", 400),
    ]
    for idx, row in enumerate(rows):
        x = 62 + idx * 210
        ret = float(row["total_return"])
        fill = float(row["fill_rate"])
        slip = float(row["slippage_cost"])
        ret_h = min(110, abs(ret) * 170)
        fill_h = fill * 120
        slip_h = slip / max_slip * 120
        parts.append(f'<rect x="{x}" y="{255 - fill_h:.1f}" width="38" height="{fill_h:.1f}" rx="5" fill="#2563eb"/>')
        parts.append(f'<rect x="{x + 48}" y="{255 - slip_h:.1f}" width="38" height="{slip_h:.1f}" rx="5" fill="#f59e0b"/>')
        color = "#059669" if ret >= 0 else "#dc2626"
        y = 255 - ret_h if ret >= 0 else 255
        parts.append(f'<rect x="{x + 96}" y="{y:.1f}" width="38" height="{ret_h:.1f}" rx="5" fill="{color}"/>')
        parts.append(_text(x + 67, 294, str(row["case"]).replace("_", " "), 12, "#0f172a", 700, "middle"))
        parts.append(_text(x + 67, 315, f"rej {int(row['rejected_orders'])}", 11, "#64748b", 500, "middle"))
    parts.append(_text(62, 334, "Blue=fill rate, amber=slippage cost scaled, green/red=absolute return magnitude", 12, "#64748b", 500))
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def _text(x: float, y: float, value: str, size: int, color: str, weight: int, anchor: str = "start") -> str:
    return f'<text x="{x}" y="{y}" font-family="Inter,Arial,sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{value}</text>'


if __name__ == "__main__":
    raise SystemExit(main())
