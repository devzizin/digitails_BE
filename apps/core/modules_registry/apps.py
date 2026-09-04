from django.apps import AppConfig

class ModulesRegistryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core.modules_registry"
    verbose_name = "Modules Registry"
    label = "modules_registry"
    