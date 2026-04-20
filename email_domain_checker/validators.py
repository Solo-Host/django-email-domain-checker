from django.conf import settings
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _


@deconstructible
class EmailDomainChecker:
    """
    Validate that an email address is not from a blocked domain.

    Looks up the domain part of the email against the BlockedDomain model.
    Domains marked as exempt are always allowed.

    Note: This performs exact domain matching. Subdomains are not checked
    against parent domains (e.g., foo.mailinator.com is NOT blocked by
    mailinator.com). This matches the behavior of the reference project.
    """

    message = _("Blocked email provider.")
    code = "invalid"

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        elif getattr(settings, "EMAIL_DOMAIN_CHECKER_MESSAGE", None):
            self.message = settings.EMAIL_DOMAIN_CHECKER_MESSAGE
        if code is not None:
            self.code = code

    def __call__(self, value):
        value = force_str(value)

        try:
            validators.validate_email(value)
        except ValidationError:
            return

        _user_part, domain_part = value.rsplit("@", 1)
        domain_part = domain_part.lower()

        from .models import BlockedDomain

        if BlockedDomain.objects.filter(domain=domain_part, is_exempt=False).exists():
            raise ValidationError(self.message, code=self.code)

    def __eq__(self, other):
        return (
            isinstance(other, EmailDomainChecker)
            and self.message == other.message
            and self.code == other.code
        )


validate_email_domain = EmailDomainChecker()
