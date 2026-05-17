# Community Benchmark Registry

This registry is generated from redacted benchmark submission manifests.
It is designed to compare audit-ready runs without exposing raw provider
prompts, responses, private portfolios, or credentials.

| Scenario | Agent | Data | Return | Max DD | Fill | Rejected | Risk edits | Audit | Hash |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| quickstart_core_synthetic_v0_1 | deterministic / signal-weighted-baseline | synthetic-market (daily, 2 symbols) | 0.3508 | -0.0126 | 0.9034 | 14 | 124 | 1.0000 | `sha256:8389671da54...` |

## Submission Rules

- Submit redacted manifests, not raw model prompt/response caches.
- Do not include broker credentials, API keys, or private holdings.
- Keep `reproducibility_hash` stable for the same scenario, data,
  execution config, risk config, agent metadata, and trajectory manifest.
