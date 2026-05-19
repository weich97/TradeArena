# Community Benchmark Registry

This registry is generated from redacted benchmark submission manifests.
It is designed to compare audit-ready runs without exposing raw provider
prompts, responses, private portfolios, or credentials.

| Entry | Scenario | Agent | Prompt | Feedback | Parse | Data | Return | Max DD | Fill | Rejected | Risk edits | Audit | Badges | Hash |
| --- | --- | --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| ta-aad1948b44bf | crisis_scene_llm_redacted_example | poe / frontier-chat-model-redacted | rationale | true | 0.9670 | yahoo-finance-csv (hourly, 3 symbols) | 0.0108 | -0.0187 | 0.7816 | 28 | 196 | 1.0000 | Reproducible; Redacted | `sha256:aad1948b44b...` |
| ta-ed2d5e4f2ff3 | quickstart_core_synthetic_v0_1 | deterministic / signal-weighted-baseline | none | true | 1.0000 | synthetic-market (daily, 2 symbols) | 0.3508 | -0.0126 | 0.9034 | 14 | 124 | 1.0000 | Reproducible; Redacted | `sha256:ed2d5e4f2ff...` |
| ta-1924d80a1f01 | leaderboard_llm_calm_trend_synthetic_v0_1 | deepseek / deepseek-v4-flash | rationale | true | 1.0000 | synthetic-market (daily, 2 symbols) | 0.0257 | -0.0008 | 0.8333 | 0 | 12 | 1.0000 | Reproducible; Redacted | `sha256:1924d80a1f0...` |
| ta-ec719fd98b6d | leaderboard_llm_calm_trend_synthetic_v0_1 | deepseek / deepseek-v4-pro | rationale | true | 1.0000 | synthetic-market (daily, 2 symbols) | 0.0240 | -0.0005 | 0.6667 | 1 | 4 | 1.0000 | Reproducible; Redacted | `sha256:ec719fd98b6...` |
| ta-f377c7a750f3 | leaderboard_llm_calm_trend_synthetic_v0_1 | poe / claude-opus-4.7 | rationale | true | 1.0000 | synthetic-market (daily, 2 symbols) | 0.0309 | -0.0008 | 0.8462 | 0 | 12 | 1.0000 | Reproducible; Redacted | `sha256:f377c7a750f...` |
| ta-43369d81d970 | leaderboard_llm_calm_trend_synthetic_v0_1 | poe / gemini-3.1-pro | rationale | true | 1.0000 | synthetic-market (daily, 2 symbols) | 0.0253 | -0.0008 | 0.6667 | 2 | 6 | 1.0000 | Reproducible; Redacted | `sha256:43369d81d97...` |
| ta-ee0a005f6c91 | leaderboard_llm_calm_trend_synthetic_v0_1 | poe / glm-5 | rationale | true | 1.0000 | synthetic-market (daily, 2 symbols) | 0.0257 | -0.0008 | 0.8333 | 0 | 12 | 1.0000 | Reproducible; Redacted | `sha256:ee0a005f6c9...` |
| ta-0e024cf49171 | leaderboard_llm_calm_trend_synthetic_v0_1 | poe / gpt-5.5 | rationale | true | 1.0000 | synthetic-market (daily, 2 symbols) | 0.0288 | -0.0008 | 0.8333 | 0 | 11 | 1.0000 | Reproducible; Redacted | `sha256:0e024cf4917...` |
| ta-657372beb82d | leaderboard_llm_calm_trend_synthetic_v0_1 | poe / kimi-k2.5 | rationale | true | 1.0000 | synthetic-market (daily, 2 symbols) | 0.0319 | -0.0008 | 0.7500 | 1 | 11 | 1.0000 | Reproducible; Redacted | `sha256:657372beb82...` |
| ta-e44dbb8a0035 | leaderboard_llm_high_vol_synthetic_v0_1 | deepseek / deepseek-v4-flash | rationale | true | 1.0000 | synthetic-market (daily, 2 symbols) | 0.0033 | -0.0075 | 0.7692 | 1 | 10 | 1.0000 | Reproducible; Redacted | `sha256:e44dbb8a003...` |
| ta-ab28baf636c6 | leaderboard_llm_high_vol_synthetic_v0_1 | deepseek / deepseek-v4-pro | rationale | true | 1.0000 | synthetic-market (daily, 2 symbols) | 0.0043 | -0.0065 | 0.7500 | 1 | 9 | 1.0000 | Reproducible; Redacted | `sha256:ab28baf636c...` |
| ta-a26229c4bfd1 | leaderboard_llm_high_vol_synthetic_v0_1 | poe / claude-opus-4.7 | rationale | true | 1.0000 | synthetic-market (daily, 2 symbols) | 0.0045 | -0.0058 | 0.7500 | 1 | 8 | 1.0000 | Reproducible; Redacted | `sha256:a26229c4bfd...` |
| ta-f17bd495aee1 | leaderboard_llm_high_vol_synthetic_v0_1 | poe / gemini-3.1-pro | rationale | true | 1.0000 | synthetic-market (daily, 2 symbols) | 0.0144 | -0.0040 | 0.7500 | 2 | 6 | 1.0000 | Reproducible; Redacted | `sha256:f17bd495aee...` |
| ta-a784bb18edb4 | leaderboard_llm_high_vol_synthetic_v0_1 | poe / glm-5 | rationale | true | 1.0000 | synthetic-market (daily, 2 symbols) | 0.0030 | -0.0058 | 0.8462 | 0 | 8 | 1.0000 | Reproducible; Redacted | `sha256:a784bb18edb...` |
| ta-ca1ac51567e2 | leaderboard_llm_high_vol_synthetic_v0_1 | poe / gpt-5.5 | rationale | true | 1.0000 | synthetic-market (daily, 2 symbols) | 0.0038 | -0.0065 | 0.7500 | 1 | 8 | 1.0000 | Reproducible; Redacted | `sha256:ca1ac51567e...` |
| ta-d049a9252a5d | leaderboard_llm_high_vol_synthetic_v0_1 | poe / kimi-k2.5 | rationale | true | 1.0000 | synthetic-market (daily, 2 symbols) | 0.0037 | -0.0052 | 0.8462 | 0 | 8 | 1.0000 | Reproducible; Redacted | `sha256:d049a9252a5...` |
| ta-92c579427c5c | leaderboard_llm_jump_tail_synthetic_v0_1 | deepseek / deepseek-v4-flash | rationale | true | 1.0000 | synthetic-market (daily, 2 symbols) | 0.0167 | -0.0214 | 0.6667 | 3 | 12 | 1.0000 | Reproducible; Redacted | `sha256:92c579427c5...` |
| ta-e1635368569c | leaderboard_llm_jump_tail_synthetic_v0_1 | deepseek / deepseek-v4-pro | rationale | true | 1.0000 | synthetic-market (daily, 2 symbols) | 0.0167 | -0.0214 | 0.7692 | 2 | 9 | 1.0000 | Reproducible; Redacted | `sha256:e1635368569...` |
| ta-23a56b641e23 | leaderboard_llm_jump_tail_synthetic_v0_1 | poe / claude-opus-4.7 | rationale | true | 1.0000 | synthetic-market (daily, 2 symbols) | 0.0167 | -0.0214 | 0.6667 | 3 | 10 | 1.0000 | Reproducible; Redacted | `sha256:23a56b641e2...` |
| ta-1429af5bf985 | leaderboard_llm_jump_tail_synthetic_v0_1 | poe / gemini-3.1-pro | rationale | true | 1.0000 | synthetic-market (daily, 2 symbols) | 0.0157 | -0.0075 | 0.6429 | 3 | 9 | 1.0000 | Reproducible; Redacted | `sha256:1429af5bf98...` |
| ta-004d1b457862 | leaderboard_llm_jump_tail_synthetic_v0_1 | poe / glm-5 | rationale | true | 1.0000 | synthetic-market (daily, 2 symbols) | 0.0167 | -0.0214 | 0.7143 | 3 | 11 | 1.0000 | Reproducible; Redacted | `sha256:004d1b45786...` |
| ta-2982046ca04d | leaderboard_llm_jump_tail_synthetic_v0_1 | poe / gpt-5.5 | rationale | true | 1.0000 | synthetic-market (daily, 2 symbols) | 0.0167 | -0.0214 | 0.6667 | 3 | 12 | 1.0000 | Reproducible; Redacted | `sha256:2982046ca04...` |
| ta-f7385c431cb1 | leaderboard_llm_jump_tail_synthetic_v0_1 | poe / kimi-k2.5 | rationale | true | 1.0000 | synthetic-market (daily, 2 symbols) | 0.0167 | -0.0214 | 0.6667 | 3 | 11 | 1.0000 | Reproducible; Redacted | `sha256:f7385c431cb...` |

## Submission Rules

- Submit redacted manifests, not raw model prompt/response caches.
- Do not include broker credentials, API keys, or private holdings.
- Keep `reproducibility_hash` stable for the same scenario, data,
  execution config, risk config, agent metadata, and trajectory manifest.
