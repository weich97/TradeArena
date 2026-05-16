# TradeArena Plugin Interfaces

The core interfaces live in `src/trading_agent_os/core/interfaces.py`.

Recommended extension categories:

- `MarketDataProvider`: streams `MarketSnapshot` objects.
- `AnalystAgent`: converts observations into `Signal` objects.
- `StrategyAgent`: converts signals into target-weight `Decision` objects.
- `RiskManagerAgent`: clips, blocks, or annotates strategy decisions.
- `ExecutionAgent`: converts approved decisions into `Order` objects.
- `OrderSimulator`: fills orders, mutates `PortfolioState`, and may expose an `ExecutionReport`.
- `MemoryStore`: records events, theses, journals, and failure cases.
- `Evaluator`: computes metrics from a `Trajectory`.

Risk managers are encouraged to expose `last_report: RiskReport | None`. Execution simulators are encouraged to expose `last_report: ExecutionReport | None`. The runner automatically serializes these reports into trajectories when present.

The framework intentionally keeps interfaces narrow. A new LLM agent, FinRL policy, broker adapter, or risk model should be able to enter the system by implementing only the protocol it owns.
