"""Baseline trading agents."""

from trading_agent_os.agents.analysts import MacroNewsAnalyst, MomentumAnalyst
from trading_agent_os.agents.execution import TargetWeightExecutionAgent
from trading_agent_os.agents.llm import ChatCompletionsLLMAnalyst, DeepSeekLLMAnalyst
from trading_agent_os.agents.portfolio import EqualWeightPortfolioManager
from trading_agent_os.agents.risk import MaxPositionRiskManager, NoRiskManager
from trading_agent_os.agents.strategy import (
    BuyAndHoldStrategy,
    MeanVarianceStrategy,
    MemoryAwareSignalWeightedStrategy,
    SignalWeightedStrategy,
)

__all__ = [
    "BuyAndHoldStrategy",
    "ChatCompletionsLLMAnalyst",
    "DeepSeekLLMAnalyst",
    "EqualWeightPortfolioManager",
    "MacroNewsAnalyst",
    "MaxPositionRiskManager",
    "MeanVarianceStrategy",
    "MemoryAwareSignalWeightedStrategy",
    "MomentumAnalyst",
    "NoRiskManager",
    "SignalWeightedStrategy",
    "TargetWeightExecutionAgent",
]
