from apps.core.permissions.services.permission_registry_service import (
    PermissionRegistryService,
)


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

            ArchitectureValidators.validate_registry_manifest(manifest)

            # ENTITY TYPES
            if include_entity_types:
                cls._bootstrap_entity_types(manifest.entity_types)

            # MODULE
            cls._bootstrap_module(manifest.module)

            # PERMISSIONS
            cls._bootstrap_permissions(manifest.permissions)

            # ROLE TEMPLATES
            cls._bootstrap_role_templates(manifest.role_templates)

            # APP LEVELS
            cls._bootstrap_app_levels(manifest.app_levels)

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

    # ROLE TEMPLATES
    @staticmethod
    def _bootstrap_role_templates(
        role_templates,
    ):

        for item in role_templates:
            PermissionRegistryService.sync_template(
                code=item["code"],
                label=item["label"],
                description=item.get("description"),
                permission_codes=item.get(
                    "permissions",
                    [],
                ),
                is_system=item.get(
                    "is_system",
                    False,
                ),
            )

    # APP LEVELS
    @staticmethod
    def _bootstrap_app_levels(
        app_levels,
    ):

        for app_level_code, template_codes in app_levels.items():
            print(
                "APP LEVEL:",
                app_level_code,
                "=>",
                template_codes,
            )
