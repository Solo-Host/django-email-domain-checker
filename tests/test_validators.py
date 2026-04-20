import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase

from email_domain_checker.models import BlockedDomain
from email_domain_checker.validators import EmailDomainChecker, validate_email_domain


class ValidatorTests(TestCase):
    def test_blocks_seeded_disposable_domain(self):
        """An email at a seeded blocked domain should be rejected."""
        with pytest.raises(ValidationError):
            validate_email_domain("user@0-mail.com")

    def test_allows_legitimate_domain(self):
        """An email at a non-blocked domain should pass."""
        validate_email_domain("user@google.com")

    def test_blocks_custom_added_domain(self):
        """A manually added blocked domain should be rejected."""
        BlockedDomain.objects.create(domain="custom-blocked.com")
        with pytest.raises(ValidationError):
            validate_email_domain("user@custom-blocked.com")

    def test_exempt_domain_allowed(self):
        """A domain marked as exempt should pass validation."""
        entry = BlockedDomain.objects.get(domain="0-mail.com")
        entry.is_exempt = True
        entry.save()
        validate_email_domain("user@0-mail.com")

    def test_invalid_email_skipped(self):
        """Invalid emails should not raise (Django's email validator handles that)."""
        validate_email_domain("not-an-email")

    def test_case_insensitive_domain_check(self):
        """Domain comparison should be case-insensitive."""
        with pytest.raises(ValidationError):
            validate_email_domain("user@0-MAIL.COM")

    def test_custom_message(self):
        """Custom error message should be used when provided."""
        checker = EmailDomainChecker(message="No disposable emails!")
        with pytest.raises(ValidationError, match="No disposable emails!"):
            checker("user@0-mail.com")

    def test_custom_code(self):
        """Custom error code should be used when provided."""
        checker = EmailDomainChecker(code="blocked")
        with pytest.raises(ValidationError) as exc_info:
            checker("user@0-mail.com")
        assert exc_info.value.code == "blocked"

    def test_settings_message_override(self):
        """EMAIL_DOMAIN_CHECKER_MESSAGE setting should override default."""
        with self.settings(EMAIL_DOMAIN_CHECKER_MESSAGE="Custom setting msg"):
            checker = EmailDomainChecker()
            with pytest.raises(ValidationError, match="Custom setting msg"):
                checker("user@0-mail.com")


class CheckedEmailFieldTests(TestCase):
    def test_field_validates_blocked_domain(self):
        """CheckedEmailField should reject blocked domains."""
        from email_domain_checker.fields import CheckedEmailField

        field = CheckedEmailField()
        with pytest.raises(ValidationError):
            field.clean("user@0-mail.com", None)

    def test_field_allows_legitimate_domain(self):
        """CheckedEmailField should allow legitimate domains."""
        from email_domain_checker.fields import CheckedEmailField

        field = CheckedEmailField()
        result = field.clean("user@google.com", None)
        assert result == "user@google.com"
