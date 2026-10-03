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

@pytest.mark.asyncio
async def test_maps_pagination_fields():
    def handler(request: httpx.Request):
        assert request.url.params["p[s]"] == "25"
        assert request.url.params["p[c]"] == "next"
        return httpx.Response(200, json={"data": []})
    async with RealIndexerClient(transport=httpx.MockTransport(handler)) as client:
        await client.market_tickers(limit=25, cursor="next")


@pytest.mark.asyncio
@pytest.mark.parametrize("envelope", ["pagination", "flat", "nested", "nested_pagination", "bare", "null_pagination"])
async def test_ticker_response_envelopes(envelope):
    rows = [{"market_id": "btc", "symbol": "BTC-PERP", "mark_price": "1", "index_price": "1", "volume_24h": "2"}]
    payloads = {
        "pagination": {"data": rows, "pagination": {"next_cursor": "next"}},
        "flat": {"data": rows, "next_cursor": "next"},
        "nested": {"data": {"data": rows, "next_cursor": "next"}},
        "nested_pagination": {"data": {"data": rows, "pagination": {"next_cursor": "next"}}},
        "bare": rows,
        "null_pagination": {"data": rows, "pagination": None},
    }
    transport = httpx.MockTransport(lambda _: httpx.Response(200, json=payloads[envelope]))
    async with RealIndexerClient(transport=transport) as client:
        page = await client.market_tickers()
    assert [ticker.symbol for ticker in page.data] == ["BTC-PERP"]
    assert page.next_cursor == (None if envelope in {"bare", "null_pagination"} else "next")


@pytest.mark.asyncio
async def test_all_market_tickers_follows_real_api_cursor_until_empty_page():
    cursors = []

    def handler(request):
        cursor = request.url.params.get("p[c]")
        cursors.append(cursor)
        assert request.url.params["p[s]"] == "100"
        assert len(cursors) <= 3
        if cursor == "end":
            return httpx.Response(200, json={"data": [], "pagination": {"next_cursor": None}})
        symbol, next_cursor = ("BTC-PERP", "second") if cursor is None else ("ETH-PERP", "end")
        return httpx.Response(200, json={
            "data": [{"market_id": symbol, "symbol": symbol, "mark_price": "1", "index_price": "1", "volume_24h": "2"}],
            "pagination": {"next_cursor": next_cursor},
        })

    async with RealIndexerClient(transport=httpx.MockTransport(handler)) as client:
        symbols = [ticker.symbol async for ticker in client.all_market_tickers()]
    assert symbols == ["BTC-PERP", "ETH-PERP"]
    assert cursors == [None, "second", "end"]


@pytest.mark.asyncio
async def test_trade_response_still_unwraps_data():
    rows = [{"id": "trade-1"}]
    transport = httpx.MockTransport(lambda _: httpx.Response(200, json={
        "data": rows, "pagination": {"next_cursor": "next"},
    }))
    async with RealIndexerClient(transport=transport) as client:
        assert await client.trades() == rows
