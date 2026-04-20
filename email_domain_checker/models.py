from django.db import models


class BlockedDomain(models.Model):
    SOURCE_SEEDED = "seeded"
    SOURCE_CUSTOM = "custom"
    SOURCE_CHOICES = [
        (SOURCE_SEEDED, "Seeded"),
        (SOURCE_CUSTOM, "Custom"),
    ]

    domain = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text="Lowercase domain name (e.g. example.com).",
    )
    is_exempt = models.BooleanField(
        default=False,
        db_index=True,
        help_text=(
            "If True, this domain is explicitly allowed even if it appears "
            "in the blocked list. Use this to override seeded entries."
        ),
    )
    source = models.CharField(
        max_length=50,
        choices=SOURCE_CHOICES,
        default=SOURCE_CUSTOM,
        help_text="How this entry was created.",
    )
    notes = models.TextField(
        blank=True,
        default="",
        help_text="Optional operator notes about this entry.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["domain"]
        verbose_name = "blocked domain"
        verbose_name_plural = "blocked domains"

    def __str__(self):
        label = self.domain
        if self.is_exempt:
            label += " (exempt)"
        return label

    def save(self, *args, **kwargs):
        self.domain = self.domain.strip().lower()
        super().save(*args, **kwargs)
