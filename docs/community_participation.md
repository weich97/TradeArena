# Community Participation

TradeArena should not describe itself as community-backed until public,
reviewable participation exists. This document defines what counts and how to
contribute without exposing provider text, credentials, or private trading data.

## Current Position

TradeArena is an early-stage research prototype. Maintainer-authored examples,
release notes, benchmark cards, and generated demos are scaffolding. They are
not evidence of external adoption.

## What Counts

| Contribution type | Counts as community evidence? | Notes |
| --- | --- | --- |
| Non-maintainer bug report with reproduction | Yes | Include environment, command, and observed output |
| External validation report | Yes | Use `docs/external_validation.md` |
| Redacted benchmark manifest | Yes, after review | Must pass schema validation and omit raw provider text |
| New data, risk, execution, or evaluator plugin | Yes, after merge | Include a demo and test |
| Maintainer-generated paper artifacts | No | Useful but not external participation |
| Star count or download count alone | No | Interest is not validation |

## Good First Participation Paths

- Reproduce `tradearena --benchmark tradearena-core` and file an external
  validation issue.
- Submit one redacted benchmark manifest for a model or deterministic baseline.
- Add a small execution stress preset with a CSV/JSON/SVG artifact.
- Improve a documentation page by mapping one claim to one runnable command.
- Add a data sidecar example with a clear license and no private fields.

## Review Standards

A community contribution should be small enough to audit:

- one scenario or adapter at a time;
- one validation command;
- no credentials or raw LLM responses;
- no live trading by default;
- no private account statements or holdings;
- clear distinction between synthetic, historical, and private data.

## Participation Milestones

| Milestone | Meaning |
| --- | --- |
| First external validation | A non-maintainer reproduces a documented command or submits a calibrated critique |
| First accepted benchmark row | A non-maintainer manifest passes schema validation and review |
| First external adapter PR | A non-maintainer contributes a data, model, risk, or execution adapter |
| First external methodology critique resolved | A reviewer concern leads to a code or documentation change |

Until these milestones exist, public language should say "early-stage research
prototype" rather than "community benchmark."
