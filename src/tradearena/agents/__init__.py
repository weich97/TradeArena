"""Baseline trading agents."""

from tradearena.agents.analysts import MacroNewsAnalyst, MomentumAnalyst
from tradearena.agents.execution import TargetWeightExecutionAgent
from tradearena.agents.llm import ChatCompletionsLLMAnalyst, DeepSeekLLMAnalyst
from tradearena.agents.portfolio import EqualWeightPortfolioManager
from tradearena.agents.risk import MaxPositionRiskManager, NoRiskManager
from tradearena.agents.rl import DeterministicRLAllocationStrategy
from tradearena.agents.strategy import (
    BuyAndHoldStrategy,
    MeanVarianceStrategy,
    MeanReversionStrategy,
    MemoryAwareSignalWeightedStrategy,
    NaiveMomentumStrategy,
    RiskParityStrategy,
    SignalWeightedStrategy,
)

__all__ = [
    "BuyAndHoldStrategy",
    "ChatCompletionsLLMAnalyst",
    "DeepSeekLLMAnalyst",
    "DeterministicRLAllocationStrategy",
    "EqualWeightPortfolioManager",
    "MacroNewsAnalyst",
    "MaxPositionRiskManager",
    "MeanVarianceStrategy",
    "MeanReversionStrategy",
    "MemoryAwareSignalWeightedStrategy",
    "MomentumAnalyst",
    "NaiveMomentumStrategy",
    "NoRiskManager",
    "RiskParityStrategy",
    "SignalWeightedStrategy",
    "TargetWeightExecutionAgent",
]
