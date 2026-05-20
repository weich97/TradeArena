from tradearena.agents import MaxPositionRiskManager
from tradearena.core.domain import Decision, Order, PortfolioState, Side
from tradearena.data import SyntheticMarketDataProvider
from tradearena.memory import InMemoryResearchMemory
from tradearena.tools.calibration import ExecutionCalibrationConfig, summarize_execution_calibration
from tradearena.tools import RealisticOrderSimulator, RiskCalculator, SimpleOrderSimulator


def test_order_simulator_never_overspends_cash():
    snapshot = SyntheticMarketDataProvider(symbols=("SYN",), periods=1, seed=1).stream()[0]
    portfolio = PortfolioState(cash=100.0)
    simulator = SimpleOrderSimulator(commission_bps=10.0, slippage_bps=5.0)

    fills = simulator.execute(snapshot, [Order(symbol="SYN", side=Side.BUY, quantity=10_000)], portfolio)

    assert len(fills) == 1
    assert portfolio.cash >= -1e-9
    assert portfolio.equity() > 0


def test_risk_calculator_drawdown():
    risk = RiskCalculator()

    assert risk.max_drawdown([100.0, 120.0, 90.0, 110.0]) == -0.25


def test_drawdown_kill_switch_forces_derisk_after_rolling_loss():
    snapshot = SyntheticMarketDataProvider(symbols=("SYN",), periods=1, seed=1).stream()[0]
    memory = InMemoryResearchMemory()
    memory.record("step", {"equity": 100_000.0})
    memory.record("step", {"equity": 96_000.0})
    portfolio = PortfolioState(cash=90_000.0)
    portfolio.last_prices.update({symbol: bar.close for symbol, bar in snapshot.bars.items()})
    decision = Decision(
        symbol="SYN",
        side=Side.BUY,
        target_weight=0.30,
        confidence=0.90,
        rationale="LLM wants to add after losses",
    )
    risk = MaxPositionRiskManager(max_drawdown=0.05, drawdown_lookback=3, drawdown_de_risk_weight=0.0)

    approved = risk.approve(snapshot, [decision], portfolio, memory)

    assert approved[0].target_weight == 0.0
    assert approved[0].side == Side.HOLD
    assert approved[0].metadata["drawdown_kill_switch"] is True
    assert risk.last_report is not None
    assert risk.last_report.passed is False
    assert risk.last_report.violations[0].constraint == "drawdown_kill_switch"


def test_drawdown_kill_switch_stays_inactive_inside_limit():
    snapshot = SyntheticMarketDataProvider(symbols=("SYN",), periods=1, seed=1).stream()[0]
    memory = InMemoryResearchMemory()
    memory.record("step", {"equity": 100_000.0})
    portfolio = PortfolioState(cash=98_000.0)
    portfolio.last_prices.update({symbol: bar.close for symbol, bar in snapshot.bars.items()})
    decision = Decision(
        symbol="SYN",
        side=Side.BUY,
        target_weight=0.20,
        confidence=0.90,
        rationale="within drawdown budget",
    )
    risk = MaxPositionRiskManager(max_drawdown=0.05, drawdown_lookback=3)

    approved = risk.approve(snapshot, [decision], portfolio, memory)

    assert approved[0].target_weight == 0.20
    assert "drawdown_kill_switch" not in approved[0].metadata
    assert risk.last_report is not None
    assert risk.last_report.passed is True


def test_realistic_simulator_records_partial_fill_and_latency():
    snapshot = SyntheticMarketDataProvider(symbols=("SYN",), periods=2, seed=1).stream()[0]
    portfolio = PortfolioState(cash=1_000_000.0)
    simulator = RealisticOrderSimulator(participation_rate=0.000001, latency_steps=0)

    fills = simulator.execute(snapshot, [Order(symbol="SYN", side=Side.BUY, quantity=10_000)], portfolio)

    assert len(fills) == 1
    assert fills[0].fill_ratio < 1.0
    assert simulator.last_report is not None
    assert simulator.last_report.partial_fills == 1


def test_realistic_simulator_spread_bps_increases_crossing_cost():
    snapshot = SyntheticMarketDataProvider(symbols=("SYN",), periods=2, seed=3).stream()[0]
    orders = [Order(symbol="SYN", side=Side.BUY, quantity=10)]

    no_spread_portfolio = PortfolioState(cash=1_000_000.0)
    wide_spread_portfolio = PortfolioState(cash=1_000_000.0)
    no_spread = RealisticOrderSimulator(participation_rate=1.0, latency_steps=0, spread_bps=0.0)
    wide_spread = RealisticOrderSimulator(participation_rate=1.0, latency_steps=0, spread_bps=100.0)

    no_spread_fill = no_spread.execute(snapshot, orders, no_spread_portfolio)[0]
    wide_spread_fill = wide_spread.execute(snapshot, orders, wide_spread_portfolio)[0]

    assert wide_spread_fill.price > no_spread_fill.price
    assert wide_spread.last_report is not None
    assert wide_spread.last_report.metadata["spread_bps"] == 100.0
    assert wide_spread.last_report.total_slippage > no_spread.last_report.total_slippage


def test_execution_calibration_marks_ohlcv_limits(tmp_path):
    csv_path = tmp_path / "SYN_Hourly_1h.csv"
    csv_path.write_text(
        "\n".join(
            [
                "Date,Open,High,Low,Close,Volume",
                "2026-01-01T09:30:00,100,102,99,101,1000",
                "2026-01-01T10:30:00,101,103,100,102,2000",
            ]
        ),
        encoding="utf-8",
    )

    summary = summarize_execution_calibration(
        [csv_path],
        ExecutionCalibrationConfig(spread_bps=None, participation_rate=0.05, market_impact=0.15),
    )

    assert summary["data"]["symbol_count"] == 1
    assert summary["data"]["row_count"] == 2
    assert summary["diagnostics"]["spread_status"] == "assumed_zero_or_external"
    assert "OHLCV bars do not contain bid-ask quotes" in summary["diagnostics"]["identification_warning"]
