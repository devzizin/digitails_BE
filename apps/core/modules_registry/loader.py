from importlib import import_module
from types import ModuleType

from django.apps import apps

from apps.core.modules_registry.manifest import RegistryManifest


class RegistryLoader:

    @classmethod
    def load(cls) -> list[RegistryManifest]:
        manifests: list[RegistryManifest] = []

        for app_config in apps.get_app_configs():
            module_path = f"{app_config.name}.registry"

            try:
                module = import_module(module_path)

            except ModuleNotFoundError as exc:
                # Ignore ONLY missing registry.py
                if exc.name == module_path:
                    continue
                raise

            manifests.append(
                cls._build_manifest(
                    app_label=app_config.label,
                    module_path=module_path,
                    module=module,
                )
            )

        return manifests

    @staticmethod
    def _build_manifest(
        *,
        app_label: str,
        module_path: str,
        module: ModuleType,
    ) -> RegistryManifest:

        return RegistryManifest(
            app_label=app_label,
            module_path=module_path,

            entity_types=getattr(module, "ENTITY_TYPES", []),
            permissions=getattr(module, "PERMISSIONS", []),
            # role_templates=getattr(module, "ROLE_TEMPLATES", []),
            # app_levels=getattr(module, "APP_LEVELS", {}),
            module=getattr(module, "MODULE", None),
        )
