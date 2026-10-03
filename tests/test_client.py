import httpx
import pytest
from real_indexer import RealAPIError, RealIndexerClient

@pytest.mark.asyncio
async def test_reads_market_tickers():
    transport = httpx.MockTransport(lambda _: httpx.Response(200, json={"data": [{"market_id": "btc", "symbol": "BTC-PERP", "mark_price": "1", "index_price": "1", "volume_24h": "2"}]}))
    async with RealIndexerClient(transport=transport) as client:
        page = await client.market_tickers()
        assert page.data[0].symbol == "BTC-PERP"

@pytest.mark.asyncio
async def test_raises_structured_error():
    transport = httpx.MockTransport(lambda _: httpx.Response(429, text="limited"))
    async with RealIndexerClient(transport=transport) as client:
        with pytest.raises(RealAPIError) as error: await client.health()
        assert error.value.status == 429
