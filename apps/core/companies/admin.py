from django.contrib import admin

from apps.core.companies.models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tenant",
        "name",
        "address_text",
        "phone",
        "email",
        "website",
        "identification_number",
        "is_verified",
        "deleted_at",
    )
    list_filter = ("is_verified",)
    search_fields = ("name", "identification_number")