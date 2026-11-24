"""Regression coverage for dynamically discovered markets, including the newer XRP, XAUT, BNB, ZEC, LIT, NEAR, XMR and ENA markets."""
import httpx
import pytest

from real_indexer import RealIndexerClient


@pytest.mark.asyncio
@pytest.mark.parametrize("markets", [
    [
        ("HYPE-USDT", "0x7fa781f5e1d1da7165cf96e5a6898235f55f2d812dd429d3feed69ff776dfa70"),
        ("SOL-USDT", "0xca22f2b22f8c16be70d29e5cc8434bedb778c51d6cb224b64c3ee7d152567936"),
    ],
    [
        ("XRP-USDT", "0xc314a4bc10a6937259f74d480ced63f55add6de39b13b983eea74bbb319c6d98"),
        ("XAUT-USDT", "0x16e576efa4a6f5e27380390c100196c91f89abc5e07307d0e342ed0e61823cd6"),
    ],
    [
        ("BNB-USDT", "0x8a7c11d4d1aa1383658eda14cca21be864fe21c911277d4fb2caeb0364f53e68"),
        ("ZEC-USDT", "0x0255d21d230632a4963ae67ba6e543f9d2a80b1d5a3069fd84da525124bfcd66"),
    ],
    [
        ("LIT-USDT", "0xd77974a7c47965d7cdbb7f13b238aecab4fa6d2d9995317fe05136d03c778114"),
        ("NEAR-USDT", "0x0bcb88ff6a2c7b394e2579bd0ef659d6344143f9d3e0dd8fb64e86300bc2f010"),
    ],
    [
        ("XMR-USDT", "0x8def23de67380cb320decaa86398baad39e7744d07373a4f88e039fd827f4635"),
        ("ENA-USDT", "0xe6bcdc29b032c00b3614c6d9236f601fb5a15670f1c9aa7aeab8ddee86fdba38"),
    ],
], ids=["hype-sol", "xrp-xaut", "bnb-zec", "lit-near", "xmr-ena"])
async def test_market_discovery_pagination_and_depth(markets):
    cursors = []
    depth_ids = []

    def handler(request):
        if request.url.path == "/api/v1/markets/tickers":
            cursor = request.url.params.get("p[c]")
            cursors.append(cursor)
            assert len(cursors) <= 2
            assert cursor in (None, "next-page")
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
                "pagination": {"next_cursor": "next-page" if cursor is None else None},
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
    assert cursors == [None, "next-page"]
    assert depth_ids == [item[1] for item in markets]
