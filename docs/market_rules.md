# Market Rules And Stress Presets

TradeArena's default simulator is market-agnostic. Market-specific realism
should be added as explicit rule plugins or scenario presets so reviewers can
see which assumptions are active.

## Market Rule Packages

| Market | Rules to encode | Why it matters |
| --- | --- | --- |
| US equities | regular-hours calendar, corporate actions, short-sale assumptions, NBBO-derived spread calibration | avoids mixing daily OHLCV backtests with undocumented execution assumptions |
| A-share | T+1 sale constraint, board-specific price limits, trading halts, lot sizes | many strategies that pass US-style assumptions become infeasible |
| Hong Kong equities | board lots, trading sessions, lunch break, stamp duty, short-sale eligibility | portfolio weights must translate into tradable quantities |
| Crypto | 24/7 sessions, venue fee tiers, funding or borrow costs, spread shocks | liquidity and fees can change faster than daily bars show |
| Futures | contract rolls, expiry, margin, tick size, session breaks | continuous prices can hide roll and margin risk |

TradeArena now exposes these as testable rule-package helpers in
[`src/tradearena/tools/market_rules.py`](../src/tradearena/tools/market_rules.py).
They are intentionally separate from the default simulator so a benchmark row
can state exactly which venue rule layer was active.

| Helper | Encoded checks |
| --- | --- |
| `ashare_rule_package()` | T+1 sellability, 100-share board lots, limit-up buy block, limit-down sell block |
| `hong_kong_rule_package()` | board-lot rounding and stamp-duty cost estimate |
| `crypto_rule_package()` | fee tier, funding cost, and participation-limited liquidity |
| `futures_rule_package()` | initial margin requirement and roll-window flag |
| `liquidity_halt_rule_package()` | participation clipping and Almgren-Chriss-style temporary impact estimate |

Minimal usage:

```python
from tradearena.core.domain import Side
from tradearena.tools import MarketRuleState, ashare_rule_package, review_market_rule_order

decision = review_market_rule_order(
    symbol="600519.SS",
    side=Side.SELL,
    quantity=200,
    state=MarketRuleState(
        price=100.0,
        previous_close=99.0,
        settled_position=100,
        same_day_buy_quantity=100,
    ),
    package=ashare_rule_package(),
)
assert decision.blocked
```

The output is a `MarketRuleDecision` with `status`, `reasons`, approved
quantity, fee/funding estimates, margin requirement, and market-impact
estimate. This makes market infeasibility auditable instead of hiding it inside
portfolio PnL.

## Risk Preset Ideas

| Preset | Checks |
| --- | --- |
| retail | max single-name weight, cash-only buys, no shorting, turnover cap |
| hedge-fund style | gross/net exposure, leverage, VaR proxy, sector concentration |
| regulatory stress | drawdown stop, participation cap, liquidity halt, price-limit block |
| crisis | widening spread, low volume, delayed fills, rejected orders |

Risk presets should emit normal `RiskReport` records so they remain comparable
with the default `MaxPositionRiskManager`.

## Adversarial Scenarios

Adversarial tests are useful for LLM agents because the failure is often in
their stated plan, not only in the realized return.

Examples:

- false risk report that claims a healthy portfolio violated limits;
- sudden liquidity drought with pending orders already queued;
- flash crash followed by partial rebound;
- halt or limit-up/limit-down period where target weights cannot be reached;
- correlated selloff where single-name narratives hide portfolio exposure.

Each scenario should publish:

- the market path or fixture generator;
- execution and risk settings;
- expected qualitative behavior;
- metrics that detect unsafe behavior;
- one command to reproduce the artifact.

## Calibration Boundary

OHLCV data can support range, volume, and participation diagnostics. It cannot
identify quoted spread, queue position, broker latency, or realized shortfall by
itself. Use [`docs/execution_model.md`](execution_model.md) before claiming a
simulator preset is calibrated to real execution.
