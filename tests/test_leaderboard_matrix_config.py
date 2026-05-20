from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_model_matrix_module():
    path = ROOT / "scripts" / "run_leaderboard_model_matrix.py"
    spec = importlib.util.spec_from_file_location("run_leaderboard_model_matrix", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_default_model_matrix_includes_execution_shock_scenarios():
    module = _load_model_matrix_module()

    assert module.DEFAULT_SCENARIOS == (
        "calm_trend",
        "high_vol",
        "jump_tail",
        "liquidity_collapse",
        "spread_explosion",
        "latency_spike",
    )

    liquidity = module._scenario_execution_config(module._scenario("liquidity_collapse"))
    spread = module._scenario_execution_config(module._scenario("spread_explosion"))
    latency = module._scenario_execution_config(module._scenario("latency_spike"))

    assert liquidity["participation_rate"] < 0.01
    assert spread["spread_bps"] >= 100.0
    assert latency["latency_steps"] >= 4
