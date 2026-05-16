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

__all__ = [
    "Bar",
    "AgentProtocolTrace",
    "Decision",
    "Fill",
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
    "Signal",
    "TradingAgentOS",
]
