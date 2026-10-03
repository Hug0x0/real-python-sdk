# Contributing

Use this repository for Python SDK issues and pull requests. See the README for local setup.

1. Open an issue describing a bug or proposed change, or choose an existing issue.
2. Fork the repository and create a focused branch.
3. Add mocked tests for changes to response parsing, query parameters, or error behavior. Tests must not require live API access or credentials.
4. Run the test suite and build commands in the README.
5. Submit a pull request explaining the change and how it was tested. Keep commits small and meaningful.

The public REAL API can evolve. Prefer additive model changes and tolerate newly added response fields. Never commit credentials or account secrets.

If an API change also affects the [Typescript SDK](https://github.com/Hug0x0/real-typescript-sdk), link the related issue or describe the corresponding change there.
