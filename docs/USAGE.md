# Python usage guide

[README](../README.md) · [API reference](API.md)

Install the repository with `python -m pip install -e .` in your virtual environment first. Run request snippets inside an async function, as shown in the README.

## Select a network

```python
from real_indexer import RealIndexerClient

async def read_testnet():
    async with RealIndexerClient(network="testnet", timeout=5.0) as client:
        return await client.health()
```

To connect to your own indexer, pass `base_url="http://localhost:8080"`. The address is an example, not a service provided by the SDK.

## Read ticker pages

```python
async with RealIndexerClient() as client:
    page = await client.market_tickers(limit=20)
    for ticker in page.data:
        print(ticker.symbol, ticker.mark_price)
    if page.next_cursor:
        next_page = await client.market_tickers(cursor=page.next_cursor, limit=20)
```

For automatic iteration:

```python
async with RealIndexerClient() as client:
    async for ticker in client.all_market_tickers():
        print(ticker.symbol)
```

Read the [pagination limitation](API.md#pagination-limitation) before relying on complete results. Cursor preservation depends on the response envelope. The iterator does not detect repeated cursors; use `break` to stop early when appropriate.

## Filter requests

```python
async with RealIndexerClient() as client:
    payments = await client.funding_payments(market_id="your-market-id", limit=20)
    trades = await client.trades(**{"p[s]": 20})
```

Replace the placeholder with an actual market ID. For `trades` and `liquidations`, raw keyword keys are sent unchanged; friendly pagination arguments are only mapped by the methods documented in the API reference.

## Handle failures

```python
import httpx
from real_indexer import RealAPIError, RealIndexerClient

async def read_health():
    try:
        async with RealIndexerClient() as client:
            return await client.health()
    except RealAPIError as error:
        print(f"Indexer returned HTTP {error.status}")
        raise
    except httpx.TimeoutException:
        print("Indexer request timed out")
        raise
```

Inspect `error.body` when diagnosing an HTTP failure, but sanitize it before sharing logs. Configure application-specific backoff if needed. The SDK does not retry or rate-limit requests.

## Test without the network

```python
import asyncio
import httpx
from real_indexer import RealIndexerClient

async def main():
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json={
        "data": [{
            "market_id": "demo",
            "symbol": "DEMO-PERP",
            "mark_price": "1.25",
            "index_price": "1.25",
            "volume_24h": "10",
        }]
    }))
    async with RealIndexerClient(transport=transport) as client:
        page = await client.market_tickers()
        assert page.data[0].symbol == "DEMO-PERP"

asyncio.run(main())
```

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| `ModuleNotFoundError: real_indexer` | Activate the environment and run `python -m pip install -e .`. |
| Unsupported syntax or runtime | Use Python 3.10 or newer. |
| Unclosed connections | Use `async with` or call `await client.close()`. |
| Only one ticker page returned | Check the documented response-envelope limitation. |
| Unexpected return type | Non-ticker responses are returned after one envelope is removed; annotations do not validate JSON. |
| HTTP 429 | Slow requests and implement bounded backoff in your application. |
| An event loop is already running | In a notebook, use `await main()` instead of `asyncio.run(main())`. |
