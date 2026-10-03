# REAL Community Python SDK

Community-maintained Python client for the public REAL indexer API.

Read-only access to market tickers, market depth, trades, liquidations, funding payments, and health, with pagination helpers and configurable mainnet, testnet, or custom API URLs.

## Development

Requires Python 3.10 or newer. Run from the repository root:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m pytest
python -m pip install build
python -m build
```

## Example

After completing the development setup:

```sh
python examples/market-tickers.py
```

See [the example](examples/market-tickers.py), [supported operations](docs/API.md), and [contribution guidelines](CONTRIBUTING.md).

## Related projects

- [Typescript SDK](https://github.com/Hug0x0/real-community-typescript)
- [Original shared repository](https://github.com/Hug0x0/real-community-sdks)

This repository retains the Python package history extracted from the original shared repository. Commit IDs changed during extraction.

Trading and key management remain the responsibility of the official Rust SDK. This project is community-built and is not affiliated with Real Markets.

## License

[MIT](LICENSE)
