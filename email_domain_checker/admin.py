from django.contrib import admin

from .models import BlockedDomain


@admin.register(BlockedDomain)
class BlockedDomainAdmin(admin.ModelAdmin):
    list_display = ("domain", "is_exempt", "source", "updated_at")
    list_filter = ("is_exempt", "source")
    search_fields = ("domain",)
    list_editable = ("is_exempt",)
    readonly_fields = ("created_at", "updated_at")
