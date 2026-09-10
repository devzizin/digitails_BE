from apps.core.permissions.services.permission_registry_service import (
    PermissionRegistryService,
)
from apps.core.modules_registry.loader import RegistryLoader
from apps.core.entities.services.entity_service import EntityTypeService


class RegistryBootstrapService:
    """
    Registry bootstrap pipeline.
    """

    @classmethod
    def bootstrap(
        cls,
        *,
        include_entity_types: bool = True,
    ):
        manifests = RegistryLoader.load()
        for manifest in manifests:

            # ENTITY TYPES
            if include_entity_types:
                cls._bootstrap_entity_types(manifest.entity_types)

            # MODULE
            cls._bootstrap_module(manifest.module)

            # PERMISSIONS
            cls._bootstrap_permissions(manifest.permissions)


    @staticmethod
    def _bootstrap_entity_types(
        entity_types,
    ):

        for item in entity_types:
            EntityTypeService.register_entity_type(**item)

    # MODULE
    @staticmethod
    def _bootstrap_module(
        module,
    ):

        if not module:
            return

        PlatformModuleService.register_module(**module)

    # PERMISSIONS
    @staticmethod
    def _bootstrap_permissions(
        permissions,
    ):

        for item in permissions:
            PermissionRegistryService.register_permission(**item)

 