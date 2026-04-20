import pytest
from django.test import TestCase

from email_domain_checker.models import BlockedDomain
from email_domain_checker.seed_domains import SEED_DOMAINS


class BlockedDomainModelTests(TestCase):
    def test_domain_normalized_on_save(self):
        entry = BlockedDomain.objects.create(domain="  MY-TEST-DOMAIN.COM  ")
        entry.refresh_from_db()
        assert entry.domain == "my-test-domain.com"

    def test_unique_domain_constraint(self):
        BlockedDomain.objects.create(domain="duplicate.com")
        with pytest.raises(Exception, match="UNIQUE constraint"):
            BlockedDomain.objects.create(domain="duplicate.com")

    def test_str_representation(self):
        entry = BlockedDomain(domain="test.com", is_exempt=False)
        assert str(entry) == "test.com"

    def test_str_representation_exempt(self):
        entry = BlockedDomain(domain="test.com", is_exempt=True)
        assert str(entry) == "test.com (exempt)"

    def test_default_values(self):
        entry = BlockedDomain.objects.create(domain="defaults.com")
        assert entry.is_exempt is False
        assert entry.source == "custom"
        assert entry.notes == ""

    def test_exempt_flag(self):
        entry = BlockedDomain.objects.create(
            domain="allowed.com", is_exempt=True
        )
        assert entry.is_exempt is True


class SeedMigrationTests(TestCase):
    def test_seeded_domains_exist(self):
        """Seed migration should have populated the table."""
        count = BlockedDomain.objects.filter(source="seeded").count()
        assert count == len(SEED_DOMAINS)

    def test_seeded_domain_sample_exists(self):
        """Spot-check a few known seeded domains."""
        for domain in ("0-mail.com", "mailinator.com", "guerrillamail.com"):
            if domain in SEED_DOMAINS:
                assert BlockedDomain.objects.filter(domain=domain).exists(), (
                    f"{domain} should be seeded"
                )

    def test_seed_is_idempotent(self):
        """Running seed again should not create duplicates."""
        import importlib

        migration_module = importlib.import_module(
            "email_domain_checker.migrations.0002_seed_domains"
        )
        from django.apps import apps

        initial_count = BlockedDomain.objects.count()
        migration_module.seed_blocked_domains(apps, None)
        assert BlockedDomain.objects.count() == initial_count
