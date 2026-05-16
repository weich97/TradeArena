from __future__ import annotations

from dataclasses import dataclass

from trading_agent_os.core.runner import TradingAgentOS
from trading_agent_os.core.trajectory import Trajectory


@dataclass(frozen=True)
class BacktestResult:
    trajectory: Trajectory
    metrics: dict[str, float | int | str]


@dataclass
class Backtester:
    name: str = "backtester"

    def run(self, system: TradingAgentOS) -> BacktestResult:
        trajectory, metrics = system.run()
        return BacktestResult(trajectory=trajectory, metrics=metrics)
