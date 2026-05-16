import json
import subprocess
import sys
from pathlib import Path


def test_render_audit_report_from_minimal_trajectory(tmp_path: Path):
    trajectory = {
        "experiment_name": "unit_audit",
        "seed": 1,
        "metadata": {"order_simulator": "realistic-order-simulator"},
        "steps": [
            {
                "timestamp": "2026-01-01T00:00:00",
                "observation": {"prices": {"SYN": 100.0}, "news_count": 0, "macro_count": 0},
                "signals": [
                    {
                        "symbol": "SYN",
                        "score": 0.5,
                        "confidence": 0.8,
                        "rationale": "unit signal",
                        "metadata": {"analyst": "unit"},
                    }
                ],
                "decisions": [
                    {
                        "symbol": "SYN",
                        "side": "buy",
                        "target_weight": 0.75,
                        "confidence": 0.8,
                        "rationale": "unit decision",
                        "metadata": {},
                    }
                ],
                "approved_decisions": [
                    {
                        "symbol": "SYN",
                        "side": "buy",
                        "target_weight": 0.25,
                        "confidence": 0.8,
                        "rationale": "unit decision",
                        "metadata": {"risk_clipped_from": 0.75},
                    }
                ],
                "orders": [{"symbol": "SYN", "side": "buy", "quantity": 10}],
                "fills": [],
                "portfolio": {"cash": 100000.0, "positions": {}, "last_prices": {"SYN": 100.0}, "equity": 100000.0},
                "reproducibility_state": {
                    "prompt_version": "unit",
                    "model_version": "deterministic",
                    "market_data_timestamp": "2026-01-01T00:00:00",
                    "memory_digest": "abc123",
                    "random_seed": 1,
                },
                "agent_trace": {},
                "risk_report": _risk_report("pre_trade", clipped=1),
                "in_trade_report": _risk_report("in_trade", clipped=0),
                "post_trade_report": _risk_report("post_trade", clipped=0),
                "execution_report": {
                    "submitted_orders": 1,
                    "eligible_orders": 0,
                    "filled_orders": 0,
                    "partial_fills": 0,
                    "pending_orders": 1,
                    "rejected_orders": 0,
                    "total_commission": 0.0,
                    "total_slippage": 0.0,
                    "average_latency_steps": 0.0,
                },
                "risk_violations": [],
                "memory_events": [],
            }
        ],
    }
    trajectory_path = tmp_path / "trajectory.json"
    output_path = tmp_path / "report.html"
    trajectory_path.write_text(json.dumps(trajectory), encoding="utf-8")

    subprocess.run(
        [
            sys.executable,
            "scripts/render_audit_report.py",
            "--trajectory",
            str(trajectory_path),
            "--output",
            str(output_path),
        ],
        check=True,
    )

    html = output_path.read_text(encoding="utf-8")
    assert "TradeArena Audit Report" in html
    assert "Proposed vs Risk-Approved Decisions" in html
    assert "unit decision" in html
    assert "abc123" in html


def _risk_report(phase: str, clipped: int) -> dict:
    return {
        "timestamp": "2026-01-01T00:00:00",
        "checks": [
            {
                "name": "unit_check",
                "passed": True,
                "severity": "warning" if clipped else "info",
                "message": "unit risk message",
                "metadata": {},
            }
        ],
        "approved_count": 1,
        "blocked_count": 0,
        "clipped_count": clipped,
        "phase": phase,
        "budget": {},
        "violations": [],
    }
