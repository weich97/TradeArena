from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS_DIR = ROOT / "examples" / "skill_tasks"


def test_skill_tasks_have_inputs_and_rubrics():
    task_dirs = sorted(path for path in TASKS_DIR.iterdir() if path.is_dir())

    assert {path.name for path in task_dirs} == {
        "claim_boundary_001",
        "execution_boundary_001",
        "plugin_author_001",
        "risk_gate_review_001",
        "trajectory_audit_001",
    }
    for task_dir in task_dirs:
        assert (task_dir / "input.md").exists()
        rubric = json.loads((task_dir / "rubric.json").read_text(encoding="utf-8"))
        assert rubric["task_id"] == task_dir.name
        assert rubric["skill"].startswith("tradearena-")
        assert len(rubric["criteria"]) >= 4
        assert 1 <= int(rubric["pass_threshold"]) <= len(rubric["criteria"])
