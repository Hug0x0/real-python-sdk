# Contributing to the REAL Python SDK

Thanks for helping improve access to public REAL indexer data. Contributions can include bug reports, documentation, tests, or small API improvements.

## Before you start

- Use English in documentation, comments, issues, pull requests, and user-facing messages.
- Search existing [issues](https://github.com/Hug0x0/real-python-sdk/issues) and [pull requests](https://github.com/Hug0x0/real-python-sdk/pulls) for related work.
- For a substantial change, describe the problem and proposed approach in an issue first.
- Keep this SDK focused on public, read-only indexer operations.

## Local setup

Follow the [README installation steps](README.md#quick-start). When contributing through a fork, clone your fork instead of the upstream repository, then create a focused branch:

```sh
git switch -c fix/describe-the-change
```

Install development dependencies and run the checks:

```sh
python -m pip install -e '.[dev]' build
python -m pytest
python -m build
```

## Project layout

| Path | Purpose |
| --- | --- |
| `src/real_indexer/` | Public client, response models, and helpers |
| `tests/` | Mocked HTTP tests |
| `examples/` | Runnable examples that access the live API |
| `docs/` | API and usage documentation |
| `.github/workflows/ci.yml` | Automated test and build checks |

## Implementation guidelines

Preserve existing public method names and behavior unless a breaking change is explicitly discussed. Prefer additive model changes and tolerate newly added API fields. Keep decimal strings intact rather than silently converting them to floating-point values.

For behavior changes, add a mocked regression test covering the relevant response shape, query encoding, or error path. Tests must not depend on the live API, credentials, or account secrets. Use `httpx.MockTransport` to control responses.

Update the API reference and usage examples when public behavior changes. Keep the existing code style and avoid unrelated formatting changes.

## Pull request checklist

- Explain the problem and resulting behavior.
- Link a related issue when one exists.
- Include appropriate regression coverage for behavior changes.
- Run the checks above and report their results.
- Keep changes focused and commits small; use messages such as `fix: preserve ticker pagination` or `docs: explain custom endpoints`.
- Do not include generated builds, virtual environments, dependency directories, credentials, or private account data.

If an API change also affects the [REAL TypeScript SDK](https://github.com/Hug0x0/real-typescript-sdk), mention the corresponding work or link a related issue there. The two clients have separate releases and do not currently expose identical APIs.

## Reporting a bug

Include your SDK revision, Python version, operating system, a minimal reproduction, and expected versus actual behavior. Redact sensitive values from logs and response bodies. For parsing issues, a small sanitized JSON fixture is especially useful.
