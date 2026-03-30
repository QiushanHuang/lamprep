# Repository Guidelines

## Project Structure & Module Organization

This repository is a Python package for `lamprep`, a version-pinned LAMMPS input generator. Source code lives under `src/lamprep/`. Keep core models in `src/lamprep/specs.py`, CLI wiring in `src/lamprep/cli.py`, and versioned registry data under `src/lamprep/manual_registry/`. Put human-facing design and planning docs in `docs/superpowers/specs/` and `docs/superpowers/plans/`. Keep test plans in `docs/test-plans/`. Automated tests live in `tests/unit/` and `tests/integration/`.

## Build, Test, and Development Commands

- `python3 -m venv .venv` creates the local virtual environment.
- `./.venv/bin/pip install -e ".[dev]"` installs the package and dev dependencies in editable mode.
- `./.venv/bin/pytest -q` runs the full suite.
- `./.venv/bin/pytest -q tests/unit/test_manual_registry.py` runs a focused unit slice.
- `./.venv/bin/python -m lamprep` performs a quick CLI smoke check.

Use the repo-local `.venv`; do not rely on system Python packages.

## Coding Style & Naming Conventions

Use Python 3.11+ style with 4-space indentation, explicit type hints, and small focused modules. Prefer `dataclass` models for structured data and keep public APIs narrow. Use snake_case for functions, variables, modules, and test names. Class names use CapWords. There is no formatter configured yet, so keep code PEP 8 aligned and avoid unnecessary abstraction.

## Testing Guidelines

Tests use `pytest`. Add unit tests for each new module and extend `tests/integration/scenarios_v1.json` plus integration tests when behavior crosses module boundaries. Test files should be named `test_<area>.py`, and test functions should start with `test_`. New logic should include at least one failing test first, then the minimal implementation to make it pass.

## Commit & Pull Request Guidelines

Recent history uses short imperative commits such as `feat: add versioned manual registry loader` and `fix: make manual registries immutable`. Follow that pattern: `feat:`, `fix:`, `docs:`, or `test:` plus a concise summary. PRs should explain what changed, why, and how it was verified. Link the relevant issue or plan when available, and include the exact test commands you ran.

## Agent-Specific Instructions

Do not develop directly on `main`. Use an isolated git worktree and feature branch, then verify the branch and path before editing. Avoid exposing extra public API beyond what the plan or spec requires. Generated files such as `.venv/`, `.pytest_cache/`, and `*.egg-info/` should not be committed.
