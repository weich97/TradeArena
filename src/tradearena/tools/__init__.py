"""Tool plugins for simulation, features, risk, optimization, and backtesting."""

from tradearena.tools.backtester import Backtester, BacktestResult
from tradearena.tools.broker_export import AlpacaPaperExportAdapter, AlpacaPaperOrder
from tradearena.tools.calibration import (
    ExecutionCalibrationConfig,
    discover_ohlcv_files,
    summarize_execution_calibration,
    write_calibration_json,
    write_calibration_markdown,
)
from tradearena.tools.features import RollingFeatureStore
from tradearena.tools.futures import FuturesContractMetadata, FuturesRollRiskEngine
from tradearena.tools.market_rules import (
    MarketRuleDecision,
    MarketRulePackage,
    MarketRuleState,
    ashare_rule_package,
    crypto_rule_package,
    futures_rule_package,
    hong_kong_rule_package,
    liquidity_halt_rule_package,
    review_market_rule_order,
)
from tradearena.tools.optimizer import EqualRiskBudgetOptimizer
from tradearena.tools.risk import RiskCalculator
from tradearena.tools.simulator import (
    CalibratedOrderSimulator,
    FillReplayOrderSimulator,
    QuoteReplayOrderSimulator,
    RealisticOrderSimulator,
    SimpleOrderSimulator,
    load_replay_fills_csv,
)

__all__ = [
    "AlpacaPaperExportAdapter",
    "AlpacaPaperOrder",
    "BacktestResult",
    "Backtester",
    "CalibratedOrderSimulator",
    "ExecutionCalibrationConfig",
    "EqualRiskBudgetOptimizer",
    "FillReplayOrderSimulator",
    "FuturesContractMetadata",
    "FuturesRollRiskEngine",
    "MarketRuleDecision",
    "MarketRulePackage",
    "MarketRuleState",
    "QuoteReplayOrderSimulator",
    "RiskCalculator",
    "RollingFeatureStore",
    "RealisticOrderSimulator",
    "SimpleOrderSimulator",
    "discover_ohlcv_files",
    "load_replay_fills_csv",
    "summarize_execution_calibration",
    "write_calibration_json",
    "write_calibration_markdown",
    "ashare_rule_package",
    "crypto_rule_package",
    "futures_rule_package",
    "hong_kong_rule_package",
    "liquidity_halt_rule_package",
    "review_market_rule_order",
]
