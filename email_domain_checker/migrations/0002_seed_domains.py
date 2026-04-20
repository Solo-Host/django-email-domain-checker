from django.db import migrations

from email_domain_checker.seed_domains import SEED_DOMAINS


def seed_blocked_domains(apps, schema_editor):
    BlockedDomain = apps.get_model("email_domain_checker", "BlockedDomain")
    existing = set(
        BlockedDomain.objects.values_list("domain", flat=True)
    )
    # Normalize domains defensively since bulk_create bypasses save()
    new_domains = [
        BlockedDomain(domain=domain.strip().lower(), source="seeded")
        for domain in SEED_DOMAINS
        if domain.strip().lower() not in existing
    ]
    if new_domains:
        BlockedDomain.objects.bulk_create(new_domains, ignore_conflicts=True)


def remove_seeded_domains(apps, schema_editor):
    BlockedDomain = apps.get_model("email_domain_checker", "BlockedDomain")
    BlockedDomain.objects.filter(source="seeded").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("email_domain_checker", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_blocked_domains, remove_seeded_domains),
    ]
