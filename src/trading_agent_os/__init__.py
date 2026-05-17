"""Trading Agent OS: pluggable AI trading agent research framework."""

from trading_agent_os.core.domain import (
    Bar,
    Decision,
    AgentProtocolTrace,
    Fill,
    MarketSnapshot,
    Order,
    PortfolioState,
    ReproducibilityState,
    RiskAttribution,
    RiskBudget,
    RiskCheck,
    RiskReport,
    RiskViolation,
    Signal,
)
from trading_agent_os.core.registry import PluginRegistry
from trading_agent_os.core.runner import TradingAgentOS
from trading_agent_os.planning import FinancialGoal, Holding, InvestorProfile, RetailPlanningAgent

__all__ = [
    "Bar",
    "AgentProtocolTrace",
    "Decision",
    "Fill",
    "FinancialGoal",
    "Holding",
    "InvestorProfile",
    "MarketSnapshot",
    "Order",
    "PluginRegistry",
    "PortfolioState",
    "ReproducibilityState",
    "RiskAttribution",
    "RiskBudget",
    "RiskCheck",
    "RiskReport",
    "RiskViolation",
    "RetailPlanningAgent",
    "Signal",
    "TradingAgentOS",
]
