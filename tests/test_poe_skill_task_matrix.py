from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "run_poe_skill_task_matrix.py"


def _load_runner():
    spec = importlib.util.spec_from_file_location("run_poe_skill_task_matrix", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_prompt_variant_parser_keeps_order_and_deduplicates():
    runner = _load_runner()

    assert runner._parse_prompt_variants("standard,skeptical_reviewer,standard") == (
        "standard",
        "skeptical_reviewer",
    )


def test_prompt_variant_parser_rejects_unknown_variant():
    runner = _load_runner()

    with pytest.raises(SystemExit):
        runner._parse_prompt_variants("standard,profit_maximizer")


def test_deepseek_models_must_use_direct_provider_namespace():
    runner = _load_runner()

    with pytest.raises(SystemExit):
        runner._parse_model_specs("poe:deepseek-v4-pro")

    assert runner._parse_model_specs("deepseek:deepseek-v4-pro") == (("deepseek", "deepseek-v4-pro"),)


def test_challenge_prompt_includes_variant_and_claim_boundary_language():
    runner = _load_runner()
    prompt = runner._build_prompt(
        ROOT / "examples" / "skill_tasks_challenge" / "stress_calibration_overclaim_001",
        ROOT / "skills",
        "adversarial_claim_boundary",
    )

    assert "adversarial_claim_boundary" in prompt
    assert "Stress-test every claim boundary" in prompt
    assert "stress simulator" in prompt
    assert "Required Answer Format" in prompt


def test_challenge_skill_task_rubrics_validate():
    result = subprocess.run(
        [
            sys.executable,
            "scripts/score_skill_task.py",
            "--tasks-dir",
            "examples/skill_tasks_challenge",
            "--validate-only",
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
