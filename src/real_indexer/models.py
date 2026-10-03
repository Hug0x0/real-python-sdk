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
    open_interest_value: str | None = None
    perp_next_funding_rate: str | None = None
    perp_next_funding_time_ms: int | None = None

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "MarketTicker":
        allowed = cls.__dataclass_fields__.keys()
        return cls(**{key: value.get(key) for key in allowed})
