# Narrative Positioning

TradeArena should be described as an early-stage research prototype for agent
reliability in financial decision systems, not only as a trading benchmark.
Trading remains the main experimental domain because it exposes a compact chain
from observation to intent, risk control, execution, and realized state.

## Core Narrative

Use three phrases consistently:

- Agent Reliability: whether autonomous financial agents remain stable,
  calibrated, and inspectable under stress.
- Risk-aware AI Systems: whether structured risk reports can act as external
  constraints and feedback for model behavior.
- Intent-to-Execution Audit: how proposed actions change as they pass through
  risk gates, order conversion, execution frictions, fills, and portfolio state.

## Scope

TradeArena currently implements paper-only financial-agent experiments. It can
support:

- LLM-assisted financial-agent evaluation;
- AI portfolio-manager prototypes;
- multi-agent finance systems that aggregate analyst, planner, memory, and
  execution modules;
- deterministic and classical baselines used as controls.

It should not be described as a live trading bot, a profitability engine, or a
broker-grade simulator. Claims should stay tied to reproducible paper
trajectories, redacted manifests, and explicit execution assumptions.

## Preferred One-Liner

TradeArena is an early-stage research prototype for auditing how autonomous
financial agents move from intent to risk-aware executable actions.
