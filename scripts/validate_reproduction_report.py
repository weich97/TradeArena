from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "reproduction_report.schema.json"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a TradeArena external reproduction report.")
    parser.add_argument("report", help="Path to an external reproduction manifest JSON.")
    parser.add_argument(
        "--allow-command-failures",
        action="store_true",
        help="Accept schema-valid reports that document command failures or missing artifacts.",
    )
    args = parser.parse_args(argv)

    report_path = Path(args.report)
    payload = json.loads(report_path.read_text(encoding="utf-8"))
    errors = validate_reproduction_report(payload, allow_command_failures=args.allow_command_failures)
    if errors:
        print(f"Invalid reproduction report: {report_path}")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"Valid reproduction report: {report_path}")
    return 0


def validate_reproduction_report(
    payload: dict[str, Any],
    *,
    allow_command_failures: bool = False,
) -> list[str]:
    errors: list[str] = []
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors.extend(sorted((error.message for error in validator.iter_errors(payload)), key=str))
    if errors:
        return errors

    if not allow_command_failures:
        for command in payload["commands"]:
            returncode = command.get("returncode")
            if returncode not in {0, None}:
                errors.append(f"command {command.get('id', '<unknown>')} returned {returncode}")
        missing_artifacts = [artifact["path"] for artifact in payload["artifacts"] if not artifact.get("exists")]
        if missing_artifacts:
            errors.append(f"missing artifacts: {', '.join(missing_artifacts)}")

    trajectory_hash = payload.get("trajectory_hash", {})
    if not isinstance(trajectory_hash, dict):
        errors.append("trajectory_hash must be an object")
    elif not str(trajectory_hash.get("reproducibility_hash", "")).startswith("sha256:"):
        errors.append("trajectory_hash.reproducibility_hash must start with sha256:")

    for artifact in payload["artifacts"]:
        if artifact.get("exists") and not str(artifact.get("sha256", "")).startswith("sha256:"):
            errors.append(f"artifact {artifact['path']} is missing a sha256 digest")

    return errors


if __name__ == "__main__":
    raise SystemExit(main())
