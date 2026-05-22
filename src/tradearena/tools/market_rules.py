from __future__ import annotations

from dataclasses import dataclass, field
from math import floor, isfinite
from typing import Any

from tradearena.core.domain import Side


@dataclass(frozen=True)
class MarketRulePackage:
    """Venue rule preset for paper-order feasibility checks."""

    name: str
    lot_size: int = 1
    t_plus_one: bool = False
    price_limit_pct: float | None = None
    fee_bps: float = 0.0
    funding_bps: float = 0.0
    stamp_duty_bps: float = 0.0
    initial_margin_rate: float = 0.0
    contract_multiplier: float = 1.0
    liquidity_participation_rate: float = 1.0
    almgren_chriss_eta: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class MarketRuleState:
    """State needed to audit one proposed order against market rules."""

    price: float
    previous_close: float | None = None
    volume: float | None = None
    settled_position: float = 0.0
    same_day_buy_quantity: float = 0.0
    available_cash: float = 0.0
    suspended: bool = False
    circuit_halt: bool = False
    in_roll_window: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class MarketRuleDecision:
    symbol: str
    side: Side
    requested_quantity: float
    approved_quantity: float
    status: str
    reasons: tuple[str, ...]
    estimated_fee: float
    estimated_funding: float
    estimated_market_impact: float
    estimated_margin_required: float
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def blocked(self) -> bool:
        return self.status == "blocked"

    @property
    def clipped(self) -> bool:
        return self.status == "clipped"


def ashare_rule_package() -> MarketRulePackage:
    return MarketRulePackage(
        name="ashare_t_plus_one_price_limit_board_lot",
        lot_size=100,
        t_plus_one=True,
        price_limit_pct=0.10,
        metadata={"market": "CN", "session": "cash_equity"},
    )


def hong_kong_rule_package(*, lot_size: int = 100, stamp_duty_bps: float = 13.0) -> MarketRulePackage:
    return MarketRulePackage(
        name="hong_kong_board_lot_stamp_duty",
        lot_size=lot_size,
        stamp_duty_bps=stamp_duty_bps,
        metadata={"market": "HK", "session": "cash_equity"},
    )


def crypto_rule_package(*, fee_bps: float = 8.0, funding_bps: float = 1.0) -> MarketRulePackage:
    return MarketRulePackage(
        name="crypto_fee_tier_funding",
        fee_bps=fee_bps,
        funding_bps=funding_bps,
        liquidity_participation_rate=0.10,
        metadata={"market": "crypto", "session": "24x7"},
    )


def futures_rule_package(
    *,
    initial_margin_rate: float = 0.08,
    contract_multiplier: float = 1.0,
) -> MarketRulePackage:
    return MarketRulePackage(
        name="futures_margin_roll",
        initial_margin_rate=initial_margin_rate,
        contract_multiplier=contract_multiplier,
        metadata={"market": "futures"},
    )


def liquidity_halt_rule_package(*, participation_rate: float = 0.01, eta: float = 0.20) -> MarketRulePackage:
    return MarketRulePackage(
        name="suspension_circuit_liquidity_halt",
        liquidity_participation_rate=participation_rate,
        almgren_chriss_eta=eta,
        metadata={"stress": "liquidity_halt"},
    )


def review_market_rule_order(
    *,
    symbol: str,
    side: Side | str,
    quantity: float,
    state: MarketRuleState,
    package: MarketRulePackage,
) -> MarketRuleDecision:
    parsed_side = Side(side)
    requested = max(0.0, float(quantity))
    approved = requested
    reasons: list[str] = []

    if requested <= 0.0 or not isfinite(requested):
        return _decision(symbol, parsed_side, requested, 0.0, "blocked", ["invalid_quantity"], state, package)
    if state.suspended:
        return _decision(symbol, parsed_side, requested, 0.0, "blocked", ["suspension"], state, package)
    if state.circuit_halt:
        return _decision(symbol, parsed_side, requested, 0.0, "blocked", ["circuit_halt"], state, package)

    price_limit_reason = _price_limit_reason(parsed_side, state, package)
    if price_limit_reason:
        return _decision(symbol, parsed_side, requested, 0.0, "blocked", [price_limit_reason], state, package)

    if package.t_plus_one and parsed_side == Side.SELL:
        sellable = max(0.0, state.settled_position - state.same_day_buy_quantity)
        if approved > sellable:
            approved = sellable
            reasons.append("t_plus_one_sellable_clip")

    lot_rounded = _round_lot(approved, package.lot_size)
    if lot_rounded < approved:
        approved = lot_rounded
        reasons.append(f"lot_size_{package.lot_size}")

    if package.liquidity_participation_rate < 1.0 and state.volume is not None:
        capacity = max(0.0, float(state.volume) * package.liquidity_participation_rate)
        if approved > capacity:
            approved = _round_lot(capacity, package.lot_size)
            reasons.append("liquidity_participation_clip")

    if package.initial_margin_rate > 0.0 and parsed_side == Side.BUY:
        margin = approved * state.price * package.contract_multiplier * package.initial_margin_rate
        if margin > state.available_cash:
            return _decision(symbol, parsed_side, requested, 0.0, "blocked", [*reasons, "futures_margin_shortfall"], state, package)

    if approved <= 0.0:
        return _decision(symbol, parsed_side, requested, 0.0, "blocked", reasons or ["no_approved_quantity"], state, package)

    status = "clipped" if approved < requested or reasons else "approved"
    if state.in_roll_window and package.name == "futures_margin_roll":
        reasons.append("futures_roll_window")
        status = "clipped" if status == "approved" else status
    return _decision(symbol, parsed_side, requested, approved, status, reasons, state, package)


def _decision(
    symbol: str,
    side: Side,
    requested: float,
    approved: float,
    status: str,
    reasons: list[str],
    state: MarketRuleState,
    package: MarketRulePackage,
) -> MarketRuleDecision:
    notional = approved * state.price * package.contract_multiplier
    fee = notional * max(0.0, package.fee_bps + package.stamp_duty_bps) / 10_000.0
    funding = notional * max(0.0, package.funding_bps) / 10_000.0
    participation = approved / max(1.0, float(state.volume or 0.0))
    impact = package.almgren_chriss_eta * participation * notional
    margin = notional * max(0.0, package.initial_margin_rate)
    return MarketRuleDecision(
        symbol=symbol,
        side=side,
        requested_quantity=requested,
        approved_quantity=approved,
        status=status,
        reasons=tuple(reason for reason in reasons if reason),
        estimated_fee=fee,
        estimated_funding=funding,
        estimated_market_impact=impact,
        estimated_margin_required=margin,
        metadata={
            "package": package.name,
            "lot_size": package.lot_size,
            "price": state.price,
            "volume": state.volume,
            "participation": participation if approved else 0.0,
            **package.metadata,
        },
    )


def _price_limit_reason(side: Side, state: MarketRuleState, package: MarketRulePackage) -> str:
    if package.price_limit_pct is None or state.previous_close is None or state.previous_close <= 0:
        return ""
    upper = state.previous_close * (1.0 + package.price_limit_pct)
    lower = state.previous_close * (1.0 - package.price_limit_pct)
    tolerance = max(1e-9, state.previous_close * 1e-8)
    if side == Side.BUY and state.price >= upper - tolerance:
        return "limit_up_buy_block"
    if side == Side.SELL and state.price <= lower + tolerance:
        return "limit_down_sell_block"
    return ""


def _round_lot(quantity: float, lot_size: int) -> float:
    lot = max(1, int(lot_size))
    return float(floor(max(0.0, quantity) / lot) * lot)
