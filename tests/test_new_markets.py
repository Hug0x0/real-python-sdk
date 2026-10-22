"""Regression coverage for dynamically discovered HYPE and SOL markets."""
import httpx
import pytest

from real_indexer import RealIndexerClient


@pytest.mark.asyncio
async def test_hype_and_sol_discovery_pagination_and_depth():
    markets = [
        ("HYPE-USDT", "0x7fa781f5e1d1da7165cf96e5a6898235f55f2d812dd429d3feed69ff776dfa70"),
        ("SOL-USDT", "0xca22f2b22f8c16be70d29e5cc8434bedb778c51d6cb224b64c3ee7d152567936"),
    ]
    cursors = []
    depth_ids = []

    def handler(request):
        if request.url.path == "/api/v1/markets/tickers":
            cursor = request.url.params.get("p[c]")
            cursors.append(cursor)
            assert len(cursors) <= 2
            assert cursor in (None, "sol-page")
            symbol, market_id = markets[0 if cursor is None else 1]
            return httpx.Response(200, json={
                "data": [{
                    "market_id": market_id,
                    "symbol": symbol,
                    "mark_price": "100.123456789012345678",
                    "index_price": "100.123456789012345678",
                    "volume_24h": "12.34",
                    "effective_mode": "ContinuousTrading",
                }],
                "pagination": {"next_cursor": "sol-page" if cursor is None else None},
            })
        market_id = request.url.path.split("/")[-2]
        assert request.url.path == f"/api/v1/markets/{market_id}/depth"
        assert market_id in [item[1] for item in markets]
        depth_ids.append(market_id)
        return httpx.Response(200, json={"data": {
            "market_id": market_id,
            "buys": [{"price_level": "100", "volume": "1"}],
            "sells": [{"price_level": "101", "volume": "2"}],
        }})

    async with RealIndexerClient(transport=httpx.MockTransport(handler)) as client:
        tickers = [ticker async for ticker in client.all_market_tickers()]
        assert [(ticker.symbol, ticker.market_id) for ticker in tickers] == markets
        for ticker in tickers:
            assert ticker.mark_price == "100.123456789012345678"
            depth = await client.market_depth(ticker.market_id)
            assert depth["market_id"] == ticker.market_id
            assert depth["buys"] and depth["sells"]
    assert cursors == [None, "sol-page"]
    assert depth_ids == [item[1] for item in markets]
