"""Tool plugins for simulation, features, risk, optimization, and backtesting."""

from trading_agent_os.tools.backtester import BacktestResult, Backtester
from trading_agent_os.tools.features import RollingFeatureStore
from trading_agent_os.tools.optimizer import EqualRiskBudgetOptimizer
from trading_agent_os.tools.risk import RiskCalculator
from trading_agent_os.tools.simulator import RealisticOrderSimulator, SimpleOrderSimulator

__all__ = [
    "BacktestResult",
    "Backtester",
    "EqualRiskBudgetOptimizer",
    "RiskCalculator",
    "RollingFeatureStore",
    "RealisticOrderSimulator",
    "SimpleOrderSimulator",
]
