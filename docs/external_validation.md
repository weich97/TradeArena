# External Validation Protocol

External validation is the evidence that makes a benchmark more than a
maintainer-run demo. A validation report should let another reader reproduce the
same result or understand why the result diverged.

## What Counts As External Validation?

External validation must come from a person or organization outside the
maintainer set. It can be:

- a deterministic smoke-test reproduction;
- a redacted LLM benchmark row;
- a historical-market replay using documented data sources;
- a quote/fill-log execution calibration report;
- a critique that finds a reproducibility, documentation, or methodology issue.

Owner-authored examples and internal paper artifacts do not count as external
validation.

## Minimal Reproduction

Run the no-key path first:

```bash
git clone https://github.com/weich97/TradeArena.git
cd TradeArena
python -m pip install -e ".[dev]"
tradearena --benchmark tradearena-core
python scripts/check_release_readiness.py
```

For the v0.2 no-key reproduction pack, run:

```bash
python scripts/run_external_reproduction_pack.py
```

This writes `outputs/reproduction/v0_2/manifest.json` with commit, Python
version, commands, output hashes, trajectory hash, and whether live APIs,
downloaded market data, or private fills were used.

Report:

- commit hash or release tag;
- operating system and Python version;
- install command;
- exact commands;
- whether all checks passed;
- output paths and any deviations.

## LLM Validation

For a live or cache-backed LLM row, submit a redacted benchmark manifest rather
than raw prompts or responses:

```bash
tradearena validate-submission examples/benchmark_submissions/example_redacted_submission.json
tradearena build-registry examples/benchmark_submissions
```

The manifest should include provider family, model display name, prompt mode,
risk-feedback mode, parse coverage, metrics, and a reproducibility hash. It
should not include raw provider text, API keys, private data, or account
information.

## Execution Calibration Validation

Execution realism needs quote/fill evidence. If you have private or licensed
fills, keep them outside Git and run:

```bash
python scripts/compare_execution_to_fills.py \
  --fills data/private/historical_fills.csv \
  --output docs/results/execution_fill_comparison.json \
  --markdown-output docs/results/execution_fill_comparison.md
```

A useful calibration report should name:

- asset universe and date range;
- venue or broker, if shareable;
- order type and reference price definition;
- sample size;
- residual mean, residual MAE, and residual max absolute bps;
- whether latency timestamps, spread observations, and bar volume were supplied;
- any reason the report cannot be made public.

## Submission Path

Open an issue using the external validation template or submit a pull request
with a redacted manifest under `examples/benchmark_submissions/`.

Maintainers should review whether:

- the commands are reproducible;
- the artifact omits secrets and raw provider text;
- the data source and license are acceptable;
- the reported claim matches the evidence.

Accepted validations can be linked from the benchmark registry or release notes.
