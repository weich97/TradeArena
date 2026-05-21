# Decision Quality vs Execution Quality

This diagnostic separates three axes that are easy to conflate in a single return table:

- Alpha quality: pre-risk, pre-cost intended allocation quality.
- Risk discipline: how often proposals survive the risk gate without clips, blocks, or violations.
- Execution robustness: how well approved orders survive fills, liquidity, latency, rejection, and cost.

![Three-axis radar chart](decision_execution_radar.svg)

| Family | Rows | Alpha quality | Risk discipline | Execution robustness | Pre-risk alpha return | Realized return | Worst DD | Fill rate | Risk edits | Violations |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| LLM synthetic | 102 | 0.623 | 0.653 | 0.778 | 2.89% | 0.88% | -5.42% | 48.37% | 384 | 188 |
| LLM real-market | 90 | 0.489 | 0.412 | 0.687 | 0.48% | -4.38% | -20.58% | 65.10% | 1871 | 717 |
| Classical synthetic | 24 | 0.743 | 0.458 | 0.731 | 3.12% | 1.37% | -5.21% | 71.40% | 0 | 126 |
| Classical real-market | 8 | 0.694 | 0.212 | 0.722 | 4.18% | 1.21% | -15.38% | 78.12% | 0 | 138 |
