# Copilot Instructions for django-email-domain-checker

## Quick Start

This is a reusable Django package for validating email addresses against a
model-backed blocked-domain registry. Use `uv` for dependency management and
`tox` as the canonical local validation entry point. This repository currently
targets Python 3.13 only.

```bash
uv sync --extra dev
```

`uv.lock` is committed. Update it when dependency metadata changes, and keep CI
compatible with `uv sync --frozen --extra dev`.

## Build, Test, and Lint Commands

### Setup and Packaging
```bash
# Install the development toolchain
uv sync --extra dev

# Build wheel and sdist artifacts
uv run python -m build
```

### Tox Entry Points
```bash
# Run the default locally available tox environments
uv run tox

# Run one environment explicitly
uv run tox -e py313
uv run tox -e lint
uv run tox -e mypy
uv run tox -e security

# Run a single test file or test function through tox
uv run tox -e py313 -- tests/test_models.py
uv run tox -e py313 -- tests/test_validators.py::test_checked_email_field_rejects_blocked_domain
```

### Direct Commands
```bash
# Run the full pytest suite
uv run pytest

# Run Ruff linting
uv run ruff check email_domain_checker tests

# Run mypy with the repository config
uv run mypy email_domain_checker tests

# Run security tooling directly
uv run bandit -q -r email_domain_checker -x email_domain_checker/migrations
uv run pip-audit
```

`tox` is the canonical entry point for local and CI checks. The configured
environments are `py313`, `lint`, `mypy`, and `security`, with optional `ruff`,
`bandit`, and `pip-audit` aliases for focused runs.

## High-Level Architecture

### Core Components

**Model and admin** (`email_domain_checker/models.py`, `email_domain_checker/admin.py`)
- `BlockedDomain` is the source of truth for whether a domain is blocked or
  explicitly exempted
- Django admin exposes the registry for operator-managed updates

**Validation surface** (`email_domain_checker/validators.py`, `email_domain_checker/fields.py`)
- `EmailDomainChecker` and `validate_email_domain` perform exact-match domain
  checks against the model-backed registry
- `CheckedEmailField` is the drop-in model field for host projects

**Seed data and migrations** (`email_domain_checker/seed_domains.py`, `email_domain_checker/migrations/`)
- The seeded disposable-domain reference list ships with the package
- The data migration loads that list during `migrate`

## Key Conventions

### Code Style
- Use `from __future__ import annotations` when forward references are needed
- Ruff is the linting tool; line length is 120 characters
- Keep migration-generated noise out of security and type-check commands

### Validation Behavior
- Domains live in the database, not hard-coded Python structures
- `is_exempt` overrides a seeded blocked domain without deleting the row
- Validation is intentionally a simple exact-match lookup; do not add regex or
  third-party API coupling unless the package requirements change

### Versioning and Release Flow
- `pyproject.toml` and `email_domain_checker/__init__.py` must stay in sync for the package version
- Keep the editable package metadata in `uv.lock` aligned when a release bump changes that version
- Normal feature work should not bump the version manually
- Releases go through `.github/workflows/release.yml`, which updates both
  version files plus the committed `uv.lock` metadata in its release bump PR,
  then creates the tag and GitHub Release after merge
- The release flow is GitHub-only for now; do not add PyPI publishing steps

## Important Notes

- Tests use `tests.settings`
- `uv.lock` should stay in sync with dependency metadata changes
- Keep workflow path filters aligned with this repo's package path
