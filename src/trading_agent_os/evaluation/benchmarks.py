from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from trading_agent_os.core.runner import TradingAgentOS


@dataclass(frozen=True)
class BenchmarkCase:
    name: str
    build_system: Callable[[], TradingAgentOS]
    description: str = ""


@dataclass
class BenchmarkRunner:
    cases: list[BenchmarkCase]

    def run(self) -> dict[str, dict[str, float | int | str]]:
        results: dict[str, dict[str, float | int | str]] = {}
        for case in self.cases:
            _, metrics = case.build_system().run()
            results[case.name] = metrics
        return results
