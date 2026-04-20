# django-email-domain-checker

## Project conventions

- **Package manager**: Use `uv` for all dependency management (venv creation, package install, etc.)
- **Virtual environment**: `.venv/` in project root, created with `uv venv .venv`
- **Install**: `uv pip install -e ".[dev]"`
- **Python**: 3.10+
- **Django**: 4.2+
- **App name**: `email_domain_checker`

## Running tests

```bash
source .venv/bin/activate
tox run
```

Individual environments:

```bash
tox run -e pytest   # tests
tox run -e mypy     # type checking
tox run -e ruff     # linting
```

## Project structure

- `email_domain_checker/` — reusable Django app
  - `models.py` — `BlockedDomain` model (source of truth for domain validation)
  - `validators.py` — `EmailDomainChecker` class and `validate_email_domain` callable
  - `fields.py` — `CheckedEmailField` drop-in replacement for `models.EmailField`
  - `admin.py` — Django admin registration for `BlockedDomain`
  - `seed_domains.py` — reference domain list (~1240 domains) used by the seed migration
  - `migrations/` — schema and data migrations (0002 seeds the reference domains)
- `tests/` — test suite using pytest-django

## Key design decisions

- Domains are stored in a database model (`BlockedDomain`), not hard-coded in Python
- The seed domain list is loaded via a data migration (`0002_seed_domains`) that runs during `migrate`
- The `is_exempt` flag allows overriding seeded entries without deleting them
- The validator does a simple exact-match DB lookup (no regex chunking)
- No external API dependencies in v1 (Block-Disposable-Email API is out of scope)
