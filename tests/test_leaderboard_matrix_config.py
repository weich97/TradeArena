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


def _load_classical_matrix_module():
    path = ROOT / "scripts" / "run_classical_baseline_matrix.py"
    spec = importlib.util.spec_from_file_location("run_classical_baseline_matrix", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_quality_decomposition_module():
    path = ROOT / "scripts" / "build_quality_decomposition.py"
    spec = importlib.util.spec_from_file_location("build_quality_decomposition", path)
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


def test_classical_matrix_includes_non_llm_strong_baselines():
    module = _load_classical_matrix_module()

    assert set(module.CLASSICAL_BASELINES) == {
        "naive_momentum",
        "mean_reversion",
        "risk_parity",
        "min_var",
    }
    assert module.CLASSICAL_BASELINES["risk_parity"]["strategy"] == "risk-parity"
    assert module.CLASSICAL_BASELINES["min_var"]["strategy"] == "min-var"


def test_quality_decomposition_uses_three_benchmark_axes():
    module = _load_quality_decomposition_module()

    assert module.DIMENSIONS == (
        ("alpha_quality_score", "Alpha quality"),
        ("risk_discipline_score", "Risk discipline"),
        ("execution_robustness_score", "Execution robustness"),
    )
    assert len(module.INPUTS) == 4
