# Python API reference

[README](../README.md) · [Usage guide](USAGE.md)

This reference describes the current implementation. Client request methods are asynchronous and perform HTTP GET requests. Public exports are `RealIndexerClient`, `RealAPIError`, `MarketTicker`, and `Page`.

## Client configuration

```python
client = RealIndexerClient(network="mainnet", timeout=15.0)
```

| Argument | Default | Purpose |
| --- | --- | --- |
| `network` | `"mainnet"` | `"mainnet"` or `"testnet"` |
| `base_url` | `None` | Override the indexer URL |
| `timeout` | `15.0` | HTTPX timeout setting in seconds |
| `transport` | `None` | Inject an `httpx.AsyncBaseTransport` |

All arguments except `network` are keyword-only. Configured URLs are `https://indexer.api.real.xyz` for mainnet and `https://indexer.api.testnet.real.xyz` for testnet. A custom `base_url` takes precedence. An unknown network raises `ValueError` unless a custom URL is supplied.

Use `async with RealIndexerClient() as client` to close connections automatically. If you manage the instance yourself, call `await client.close()` when finished. HTTPX timeouts apply to network operations, not an overall deadline for a complete pagination loop.

## Methods

| Method | Result after awaiting | Path |
| --- | --- | --- |
| `health()` | `dict[str, Any]` | `/health` |
| `market_tickers(*, cursor=None, limit=100)` | `Page[MarketTicker]` | `/api/v1/markets/tickers` |
| `market_depth(market_id)` | `dict[str, Any]` | `/api/v1/markets/{market_id}/depth` |
| `trades(**filters)` | `list[dict[str, Any]]` annotation | `/api/v1/trades` |
| `liquidations(**filters)` | `list[dict[str, Any]]` annotation | `/api/v1/liquidations` |
| `funding_payments(*, market_id=None, account_id=None, limit=100)` | `list[dict[str, Any]]` annotation | `/api/v1/funding-payments` |

`all_market_tickers()` is an async iterator, consumed with `async for`, rather than an awaitable list. It requests ticker pages using the default limit of 100 and stops when the parsed page has no next cursor.

Unlike the TypeScript SDK, this client currently has no `markets()` method. Market depth uses an untyped dictionary. Market IDs are inserted directly into the URL path; use valid IDs returned by the indexer.

### Query mapping

| SDK argument | HTTP parameter |
| --- | --- |
| `cursor` in `market_tickers` | `p[c]` |
| `limit` in tickers or funding payments | `p[s]` |
| `market_id` in funding payments | `f[market_ids]` |
| `account_id` in funding payments | `f[account_ids]` |

`trades` and `liquidations` forward keyword keys literally. For these methods, use `**{"p[s]": 20}` to request a page size; `limit=20` would send a literal `limit` parameter. Values set to `None` are omitted. There is no local validation of page sizes or filters.

## Models and response handling

`Page[T]` is a frozen dataclass with `data: list[T]` and `next_cursor: str | None = None`.

`MarketTicker` is a frozen dataclass containing:

- `market_id`, `symbol`, `mark_price`, `index_price`, and `volume_24h`.
- Optional `open_interest_value`, `perp_next_funding_rate`, and `perp_next_funding_time_ms`.

See [src/real_indexer/models.py](../src/real_indexer/models.py) for exact annotations. Unknown ticker fields are discarded. Missing fields become `None` during parsing, including fields whose annotations say `str`; these dataclasses do not enforce a schema at runtime.

Prices and rates remain strings. For precise calculations, consider Python's `decimal.Decimal` instead of converting directly to `float`. Time fields ending in `_ms` represent milliseconds.

### Pagination limitation

The request layer removes one top-level `data` envelope before ticker parsing. A response shaped as `{"data": [...], "next_cursor": "..."}` therefore loses its cursor. A nested page such as `{"data": {"data": [...], "next_cursor": "..."}}` preserves the cursor. Do not assume `all_market_tickers()` retrieved every page without checking the response shape of your indexer.

Other methods return decoded JSON after this same unwrapping step. Their annotations do not normalize a nested page object into a list, and do not provide access to discarded outer pagination metadata.

## Errors

Non-success HTTP responses raise `RealAPIError`, with `status: int` and `body: str`. HTTPX transport and timeout exceptions, JSON decoding failures, and unexpected response-shape errors propagate to callers. The SDK does not retry automatically.
