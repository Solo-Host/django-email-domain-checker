# django-email-domain-checker

A Django package that validates email addresses against a model-backed registry of blocked domains. Inspired by [django-disposable-email-checker](https://github.com/jheld/DisposableEmailChecker), but stores domains in the database instead of hard-coded Python lists.

## Features

- **Model-backed domain registry** — blocked domains live in the database, not code
- **~1,240 seeded domains** — reference list loaded automatically via data migration
- **Exemption support** — mark any domain as exempt to override blocking
- **Django admin integration** — manage domains through the admin interface
- **Drop-in field** — `CheckedEmailField` replaces `models.EmailField` with domain validation
- **Standalone validator** — use `validate_email_domain` anywhere you need it

## Installation

```bash
uv pip install django-email-domain-checker
```

Add `"email_domain_checker"` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    "email_domain_checker",
]
```

Run migrations to create the `BlockedDomain` table and seed the default domain list:

```bash
python manage.py migrate email_domain_checker
```

## Usage

### Model field

```python
from django.db import models
from email_domain_checker.fields import CheckedEmailField

class MyModel(models.Model):
    email = CheckedEmailField()
```

### Standalone validator

```python
from django.core.exceptions import ValidationError
from email_domain_checker.validators import validate_email_domain

try:
    validate_email_domain("user@example.com")
except ValidationError:
    print("Blocked!")
```

### Custom error message

Set a global default message in settings:

```python
EMAIL_DOMAIN_CHECKER_MESSAGE = "This email provider is not allowed."
```

Or pass it directly:

```python
from email_domain_checker.validators import EmailDomainChecker

checker = EmailDomainChecker(message="Please use a permanent email address.")
checker("user@mailinator.com")  # raises ValidationError
```

## Managing domains

### Django admin

The `BlockedDomain` model is registered in the Django admin with search, filtering, and inline editing of the exemption flag.

### Programmatic management

```python
from email_domain_checker.models import BlockedDomain

# Add a new blocked domain
BlockedDomain.objects.create(domain="sketchy-provider.com")

# Exempt a seeded domain (allow it through validation)
domain = BlockedDomain.objects.get(domain="mailinator.com")
domain.is_exempt = True
domain.save()

# Remove a domain entirely
BlockedDomain.objects.filter(domain="sketchy-provider.com").delete()
```

### Management command (bulk add)

```python
from email_domain_checker.models import BlockedDomain

new_domains = ["bad1.com", "bad2.com", "bad3.com"]
BlockedDomain.objects.bulk_create(
    [BlockedDomain(domain=d) for d in new_domains],
    ignore_conflicts=True,
)
```

## Model reference

### `BlockedDomain`

| Field | Type | Description |
|-------|------|-------------|
| `domain` | `CharField(255)` | Lowercase domain, unique, indexed |
| `is_exempt` | `BooleanField` | If `True`, domain passes validation even if listed |
| `source` | `CharField(50)` | `"seeded"` (from migration) or `"custom"` (manually added) |
| `notes` | `TextField` | Optional operator notes |
| `created_at` | `DateTimeField` | Auto-set on creation |
| `updated_at` | `DateTimeField` | Auto-set on save |

## Validation logic

1. **Invalid email format** → skipped (Django's built-in email validator handles this)
2. **Domain exists with `is_exempt=True`** → allowed
3. **Domain exists with `is_exempt=False`** → rejected with `ValidationError`
4. **Domain not in registry** → allowed

## Development

```bash
git clone <repo-url>
cd django-email-domain-checker
uv venv .venv
source .venv/bin/activate
uv pip install -e ".[dev]"
pytest
```

## License

MIT
