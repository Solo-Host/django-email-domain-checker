from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import validate_email_domain


class CheckedEmailField(models.EmailField):
    """
    An EmailField that also validates the domain against the blocked-domain
    registry. Drop-in replacement for ``models.EmailField``.
    """

    default_validators = [validators.validate_email, validate_email_domain]
    description = _("Email address (checked against blocked domains)")
