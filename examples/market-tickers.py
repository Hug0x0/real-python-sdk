import asyncio
from real_indexer import RealIndexerClient

async def main():
    async with RealIndexerClient() as real:
        async for ticker in real.all_market_tickers():
            print(ticker.symbol, ticker.perp_next_funding_rate)

asyncio.run(main())
