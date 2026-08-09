from django.apps import AppConfig


class CompaniesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core.companies"
    label = "companies"
    verbose_name = "Core Companies"
