# Execution Calibration Priority

The next credibility milestone is execution calibration, not a larger model
matrix. The default simulator remains a transparent stress model until a result
attaches quote, order-book, or realized fill evidence.

## Priority Order

1. **Quote/fill fit:** fit spread, residual slippage, participation, latency,
   and market impact from top-of-book quotes plus realized fills.
2. **Quote or Level-2 replay:** replay decisions against observed bid/ask and,
   when available, depth constraints.
3. **OHLCV diagnostic:** use bar range and dollar volume only as a weak
   plausibility diagnostic.

The repository now includes a concrete quote/fill calibration entry point:

```bash
python scripts/calibrate_quote_fill_model.py \
  --quotes data/public/microstructure_sample/quotes.csv \
  --fills data/public/microstructure_sample/fills.csv \
  --output docs/results/execution_quote_fill_calibration_sample.json \
  --markdown-output docs/results/execution_quote_fill_calibration_sample.md
```

The checked-in microstructure files are a small reproducible fixture. They test
the calibration pipeline and report format. They are not a venue-wide execution
claim. A publishable calibration row should replace them with public exchange
quote/order-book data, licensed data, or broker fills and should report source,
venue, date range, order type, sample size, and licensing/redaction limits.

## Required Calibration Report Fields

Every calibrated execution report should include:

- quote source and fill source;
- symbol universe and date range;
- order type, reference-price definition, and fee treatment;
- aligned quote/fill sample size;
- median and tail spread;
- fitted base slippage and market-impact coefficient;
- latency summary when timestamps exist;
- residual mean, residual MAE, and residual max absolute bps;
- exact command, commit or tag, and output hashes.

Rows that do not provide these fields should be described as stress-simulator
results, not calibrated transaction-cost results.
