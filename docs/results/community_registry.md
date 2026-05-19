# Community Benchmark Registry

This registry is generated from redacted benchmark submission manifests.
It is designed to compare audit-ready runs without exposing raw provider
prompts, responses, private portfolios, or credentials.

| Entry | Scenario | Agent | Prompt | Feedback | Parse | Data | Return | Max DD | Fill | Rejected | Risk edits | Audit | Badges | Hash |
| --- | --- | --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| ta-aad1948b44bf | crisis_scene_llm_redacted_example | poe / frontier-chat-model-redacted | rationale | true | 0.9670 | yahoo-finance-csv (hourly, 3 symbols) | 0.0108 | -0.0187 | 0.7816 | 28 | 196 | 1.0000 | Reproducible; Redacted | `sha256:aad1948b44b...` |
| ta-ed2d5e4f2ff3 | quickstart_core_synthetic_v0_1 | deterministic / signal-weighted-baseline | none | true | 1.0000 | synthetic-market (daily, 2 symbols) | 0.3508 | -0.0126 | 0.9034 | 14 | 124 | 1.0000 | Reproducible; Redacted | `sha256:ed2d5e4f2ff...` |
| ta-dd24cf8c1010 | leaderboard_llm_smoke_synthetic_v0_1 | deepseek / deepseek-v4-flash | rationale | true | 1.0000 | synthetic-market (daily, 2 symbols) | 0.0257 | -0.0008 | 0.8333 | 0 | 12 | 1.0000 | Reproducible; Redacted | `sha256:dd24cf8c101...` |
| ta-292f01e9176b | leaderboard_llm_smoke_synthetic_v0_1 | deepseek / deepseek-v4-pro | rationale | true | 1.0000 | synthetic-market (daily, 2 symbols) | 0.0240 | -0.0005 | 0.6667 | 1 | 4 | 1.0000 | Reproducible; Redacted | `sha256:292f01e9176...` |
| ta-ddd0c821f951 | leaderboard_llm_smoke_synthetic_v0_1 | poe / claude-opus-4.7 | rationale | true | 1.0000 | synthetic-market (daily, 2 symbols) | 0.0309 | -0.0008 | 0.8462 | 0 | 12 | 1.0000 | Reproducible; Redacted | `sha256:ddd0c821f95...` |
| ta-ba0fcb46ea63 | leaderboard_llm_smoke_synthetic_v0_1 | poe / gemini-3.1-pro | rationale | true | 1.0000 | synthetic-market (daily, 2 symbols) | 0.0253 | -0.0008 | 0.6667 | 2 | 6 | 1.0000 | Reproducible; Redacted | `sha256:ba0fcb46ea6...` |
| ta-c7e6cbf723e1 | leaderboard_llm_smoke_synthetic_v0_1 | poe / glm-5 | rationale | true | 1.0000 | synthetic-market (daily, 2 symbols) | 0.0257 | -0.0008 | 0.8333 | 0 | 12 | 1.0000 | Reproducible; Redacted | `sha256:c7e6cbf723e...` |
| ta-e7e610e43ae0 | leaderboard_llm_smoke_synthetic_v0_1 | poe / gpt-5.5 | rationale | true | 1.0000 | synthetic-market (daily, 2 symbols) | 0.0288 | -0.0008 | 0.8333 | 0 | 11 | 1.0000 | Reproducible; Redacted | `sha256:e7e610e43ae...` |
| ta-a4801f76be7c | leaderboard_llm_smoke_synthetic_v0_1 | poe / kimi-k2.5 | rationale | true | 1.0000 | synthetic-market (daily, 2 symbols) | 0.0319 | -0.0008 | 0.7500 | 1 | 11 | 1.0000 | Reproducible; Redacted | `sha256:a4801f76be7...` |

## Submission Rules

- Submit redacted manifests, not raw model prompt/response caches.
- Do not include broker credentials, API keys, or private holdings.
- Keep `reproducibility_hash` stable for the same scenario, data,
  execution config, risk config, agent metadata, and trajectory manifest.
