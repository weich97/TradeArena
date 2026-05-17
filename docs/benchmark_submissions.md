# Benchmark Submissions

TradeArena accepts redacted benchmark manifests so users can compare runs
without sharing raw provider prompts, responses, credentials, or private
portfolio data.

## Validate One Submission

```bash
tradearena validate-submission examples/benchmark_submissions/example_redacted_submission.json
```

Equivalent script entry:

```bash
python scripts/validate_benchmark_submission.py examples/benchmark_submissions/example_redacted_submission.json
```

## Build The Registry

```bash
tradearena build-registry examples/benchmark_submissions \
  --output docs/results/community_registry.md \
  --csv-output docs/results/community_registry.csv \
  --html-output docs/results/community_registry.html
```

The generated registry is tracked at
[`docs/results/community_registry.md`](results/community_registry.md).
The browser-readable version is
[`docs/results/community_registry.html`](results/community_registry.html).

## Hash A Trajectory

```bash
tradearena hash-run outputs/examples/audit_walkthrough_trajectory.json
```

The hash is computed from stable scenario, data, execution, risk, agent,
redaction, and trajectory-manifest fields. Outcome metrics are intentionally
excluded so the fingerprint identifies the reproducible run context rather than
the score.

## Safety Boundary

Submissions should include:

- redacted model metadata,
- execution and risk configuration,
- compact metrics,
- trajectory manifest path or URI,
- reproducibility hash.

Submissions should not include:

- API keys or broker credentials,
- raw model prompts or responses,
- private holdings,
- live-order instructions.
