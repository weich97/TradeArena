# Governance

TradeArena is maintained as an open benchmark and audit framework for financial
AI agents. The project prioritizes reproducibility, safe execution boundaries,
and reviewable artifacts over short-term performance claims.

## Version Policy

- `v0.x` APIs are experimental.
- Core schemas and protocol objects receive stricter review than examples.
- Examples may evolve quickly when they improve reproducibility or onboarding.

## Review Principles

- Core protocol changes should preserve replayable trajectories and audit logs.
- Provider adapters must avoid committing raw prompt/response caches.
- Broker or execution adapters must default to offline, paper-only, or
  human-approved behavior.
- New benchmark rows should include data/source notes, execution assumptions,
  risk assumptions, and a reproducibility hash.

## Maintainer Decisions

Maintainers may reject contributions that blur the boundary between benchmark
research and live financial advice, expose credentials or private data, or make
unverifiable profitability claims.
