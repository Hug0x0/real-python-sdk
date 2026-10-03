<div align="center">

# REAL Python SDK

**Public REAL market data, accessible from Python.**

[![CI](https://github.com/Hug0x0/real-python-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/Hug0x0/real-python-sdk/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)

[Quick start](#quick-start) · [API reference](docs/API.md) · [Usage guide](docs/USAGE.md) · [Contributing](CONTRIBUTING.md)

</div>

---

A community-maintained client for the public REAL indexer API. Query market data, inspect order-book depth, and retrieve trades, liquidations, and funding payments with a small API.

> **Scope:** Read-only indexer access. This SDK does not sign transactions, submit orders, or manage private keys. It is not affiliated with Real Markets.

## Why use it?

- An async client built on `httpx`, with context-managed connections.
- Dataclass models for market tickers and pages.
- Injectable HTTP transports for offline testing.
- Mainnet, testnet, and custom indexer URLs.
- Configurable request timeouts and structured HTTP errors.

## Quick start

Requires Python 3.10 or newer.

### 1. Install from source

These instructions use the repository directly and do not depend on an npm or PyPI release. The distribution name is `real-community-indexer`; the Python import is `real_indexer`.

```sh
git clone https://github.com/Hug0x0/real-python-sdk.git
cd real-python-sdk
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

On Windows PowerShell, activate the environment with `.venv\Scripts\Activate.ps1` instead.

### 2. Read market tickers

Save this as `quickstart.py` in the repository root and run it with `python quickstart.py`:

```python
import asyncio
from real_indexer import RealIndexerClient

async def main():
    async with RealIndexerClient(network="mainnet") as client:
        page = await client.market_tickers(limit=20)
        for ticker in page.data:
            print(ticker.symbol, ticker.mark_price)

asyncio.run(main())
```

This example makes a live request to mainnet. No API key is required by the client.

### 3. Try the included example

```sh
python examples/market-tickers.py
```

## Documentation

| Guide | What you will find |
| --- | --- |
| [API reference](docs/API.md) | Constructor options, methods, return types, and query mapping |
| [Usage guide](docs/USAGE.md) | Networks, pagination, error handling, and offline testing |
| [Contributing](CONTRIBUTING.md) | Local setup, validation, and pull request expectations |

## Development

After the installation steps above:

```sh
python -m pip install -e '.[dev]' build
python -m pytest
python -m build
```

Tests use mocked HTTP responses; they do not need network access or credentials. CI runs tests and builds on pushes and pull requests. Passing mocked tests does not guarantee compatibility with every live API response.

## Current scope

This is an early `0.1.0` client with a small test suite. Response types describe the expected API shape; they are not runtime schema validation. Decimal values such as prices and funding rates are represented as strings. See the API reference before converting them for calculations.

There is no built-in retry policy, rate limiter, WebSocket transport, or trading support.

## Contributing

Bug reports, documentation improvements, and focused pull requests are welcome. Start with [CONTRIBUTING.md](CONTRIBUTING.md), or [open an issue](https://github.com/Hug0x0/real-python-sdk/issues).

Use English for documentation, issues, pull requests, code comments, and user-facing messages so contributors can collaborate consistently.

## Related projects

- [REAL TypeScript SDK](https://github.com/Hug0x0/real-typescript-sdk)
- [Original shared repository](https://github.com/Hug0x0/real-community-sdks)

The language-specific history was extracted from the original shared repository. Extraction preserved the relevant commits and changed their commit IDs.

## License

[MIT](LICENSE).
