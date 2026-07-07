# AGENTS.md

## Cursor Cloud specific instructions

FastAPI is a Python library (not a long-running product service). Development tooling is
driven by [`uv`](https://docs.astral.sh/uv/); the pinned interpreter is Python 3.11
(see `.python-version`). The startup update script installs `uv` (to `~/.local/bin`) and
runs `uv sync --extra all`, which installs the `dev` dependency group plus all optional
extras (`fastapi-cli`, `pydantic-extra-types`, etc.). The `all` extra is required — without
it `mypy`/`ty` fail with import-not-found errors for the optional packages.

Run everything through `uv run` so the correct virtualenv/interpreter is used. If `uv` is
not on `PATH` in a fresh shell, it lives at `~/.local/bin/uv` (also added to `~/.bashrc`).

Common commands (see `scripts/`):
- Lint (mypy + ty + ruff check + ruff format check): `uv run bash scripts/lint.sh`
- Tests (pytest, parallel via xdist): `uv run bash scripts/test.sh`
- Tests with coverage: `uv run bash scripts/test-cov.sh`
- Autofix format/lint: `uv run bash scripts/format.sh`

Notes:
- `scripts/test.sh` sets `PYTHONPATH=./docs_src` so the tutorial example apps import
  correctly; run tests via that script rather than bare `pytest`.
- To run/demo an app, point the FastAPI CLI at any tutorial module, e.g.
  `uv run fastapi dev docs_src/first_steps/tutorial001_py310.py` (serves the app plus
  interactive docs at `/docs`).
