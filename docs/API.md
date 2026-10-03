# Supported read operations

The client exposes health, markets or market tickers, market depth, trades, liquidations, and funding payments. Pagination helpers are included for ticker collection.

The API accepts a custom base URL for local testing and future REAL deployments. Mainnet and testnet defaults match the canonical endpoints published by the official Rust SDK.

This package intentionally contains no signing or private-key code. Use the official REAL Rust SDK for account creation, deposits, order submission, cancellation, and margin changes.
