# TradeArena v0.2 Benchmark Spec

`benchmarks/v0.2/spec.json` is the frozen comparison contract for the next
public benchmark card. The goal is to make model rows comparable before adding
more features or more providers.

## Frozen Surfaces

The v0.2 spec fixes:

- data windows, asset pools, frequency, and rolling-window offsets;
- market rules, risk limits, cash/leverage constraints, and default execution
  stress parameters;
- allowed information, timestamp masking, prompt/version recording, cache
  policy, and redaction requirements;
- seeds, deterministic anchors, classical baselines, and model audit fields;
- metrics, confidence intervals, paired bootstrap tests, paired sign-flip
  permutation tests, and failure accounting.

The spec boundary is explicit: v0.2 measures agent reliability and
intent-to-execution auditability. It does not claim live profitability or
broker-grade transaction-cost prediction unless a row attaches quote/fill
calibration provenance.

## Validation

Run:

```bash
python scripts/validate_benchmark_spec.py benchmarks/v0.2/spec.json
```

The validator checks required fields and prints a canonical SHA-256 hash. Use
that hash in release notes and reproduction reports so a benchmark row can name
the exact protocol it followed.

## Failure Accounting

Failures are part of the benchmark:

- provider call failures are recorded with provider, model, scenario, seed, and
  error class;
- parser failures lower `parse_coverage` and use the declared parser fallback;
- risk blocks count as valid risk interventions;
- execution rejections count as attempted orders;
- missing data invalidates a row unless the scenario declares a data-gap rule
  before evaluation.

This makes bad rows visible instead of letting leaderboard scripts quietly
select only successful runs.
