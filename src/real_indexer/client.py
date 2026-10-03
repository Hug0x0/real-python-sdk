from __future__ import annotations
from typing import Any, AsyncIterator
import httpx
from .models import MarketTicker, Page

URLS = {"mainnet": "https://indexer.api.real.xyz", "testnet": "https://indexer.api.testnet.real.xyz"}

class RealAPIError(RuntimeError):
    def __init__(self, status: int, body: str):
        super().__init__(f"REAL API returned {status}")
        self.status, self.body = status, body

class RealIndexerClient:
    def __init__(self, network: str = "mainnet", *, base_url: str | None = None, timeout: float = 15.0, transport: httpx.AsyncBaseTransport | None = None):
        if network not in URLS and base_url is None: raise ValueError("network must be mainnet or testnet")
        self._client = httpx.AsyncClient(base_url=(base_url or URLS[network]).rstrip("/"), timeout=timeout, transport=transport, headers={"accept": "application/json"})

    async def __aenter__(self): return self
    async def __aexit__(self, *_: object): await self.close()
    async def close(self): await self._client.aclose()
    async def _get(self, path: str, params: dict[str, Any] | None = None, *, unwrap: bool = True) -> Any:
        response = await self._client.get(path, params={k: v for k, v in (params or {}).items() if v is not None})
        if not response.is_success: raise RealAPIError(response.status_code, response.text)
        payload = response.json()
        return payload.get("data", payload) if unwrap and isinstance(payload, dict) else payload

    async def health(self) -> dict[str, Any]: return await self._get("/health")
    async def market_tickers(self, *, cursor: str | None = None, limit: int = 100) -> Page[MarketTicker]:
        payload = await self._get("/api/v1/markets/tickers", {"p[c]": cursor, "p[s]": limit}, unwrap=False)
        if isinstance(payload, list): return Page([MarketTicker.from_dict(item) for item in payload])
        if isinstance(payload.get("data"), dict):
            payload = payload["data"]
        pagination = payload.get("pagination") or {}
        next_cursor = pagination.get("next_cursor", payload.get("next_cursor"))
        return Page([MarketTicker.from_dict(item) for item in payload.get("data", [])], next_cursor)
    async def all_market_tickers(self) -> AsyncIterator[MarketTicker]:
        cursor = None
        while True:
            page = await self.market_tickers(cursor=cursor)
            for item in page.data: yield item
            cursor = page.next_cursor
            if not cursor: break
    async def market_depth(self, market_id: str) -> dict[str, Any]: return await self._get(f"/api/v1/markets/{market_id}/depth")
    async def trades(self, **filters: Any) -> list[dict[str, Any]]: return await self._get("/api/v1/trades", filters)
    async def liquidations(self, **filters: Any) -> list[dict[str, Any]]: return await self._get("/api/v1/liquidations", filters)
    async def funding_payments(self, *, market_id: str | None = None, account_id: str | None = None, limit: int = 100) -> list[dict[str, Any]]: return await self._get("/api/v1/funding-payments", {"f[market_ids]": market_id, "f[account_ids]": account_id, "p[s]": limit})
