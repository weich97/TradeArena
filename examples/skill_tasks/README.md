# TradeArena Skill Task Suite

This directory contains small, deterministic tasks for evaluating whether a
human reviewer or coding agent can use TradeArena skills without turning them
into trading prompts.

Each task includes:

- `input.md`: the instruction shown to the reviewer or model;
- one small artifact or expected-output note when useful;
- `rubric.json`: machine-readable grading criteria.

These tasks evaluate audit, reproduction, calibration, claim-boundary, and
plugin-authoring ability. They do not evaluate trading profitability.
