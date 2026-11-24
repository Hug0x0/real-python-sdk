from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

T = TypeVar("T")
@dataclass(frozen=True)
class Page(Generic[T]):
    data: list[T]
    next_cursor: str | None = None

@dataclass(frozen=True)
class MarketTicker:
    market_id: str
    symbol: str
    mark_price: str
    index_price: str
    volume_24h: str
    turnover_24h: str | None = None
    open_interest: str | None = None
    open_interest_value: str | None = None
    perp_next_funding_rate: str | None = None
    perp_next_funding_time_ms: int | None = None
    #: Price of the most recent fill.
    last_traded_price: str | None = None
    #: Last traded price 24h ago.
    prev_price_24h: str | None = None
    #: Fractional 24h change: last_traded_price / prev_price_24h - 1 ("-0.05" = -5%).
    price_change_24h: str | None = None
    high_price_24h: str | None = None
    low_price_24h: str | None = None
    #: Fractional change of 24h volume versus the previous 24h ("0.25" = +25%).
    volume_change_24h: str | None = None
    updated_at_ms: int | None = None

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "MarketTicker":
        allowed = cls.__dataclass_fields__.keys()
        return cls(**{key: value.get(key) for key in allowed})
