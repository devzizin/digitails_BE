from apps.core.modules_registry.modules_registry_public.models import PlatformModule


class PlatformModuleService:

    @staticmethod
    def register_module(
        *,
        code: str,
        label: str,
        description: str = "",
        icon: str = "",
        anchors=None,
        supports_company_rollup: bool = False,
        requires=None,
        selector_path: str = "",
        permissions_required=None,
        is_system: bool = False,
    ) -> PlatformModule:

        module = PlatformModule.objects.filter(
            code=code,
        ).first()

        if not module:

            return PlatformModule.objects.create(
                code=code,
                label=label,
                description=description,
                icon=icon,
                anchors=anchors or [],
                supports_company_rollup=(
                    supports_company_rollup
                ),
                requires=requires or [],
                selector_path=selector_path,
                permissions_required=(
                    permissions_required or {}
                ),
                is_system=is_system,
                is_enabled=True,
            )

        # ==========================================
        # MUTABLE FIELDS
        # ==========================================

        module.label = label
        module.description = description
        module.icon = icon

        module.anchors = anchors or []

        module.supports_company_rollup = (
            supports_company_rollup
        )

        module.requires = requires or []

        module.selector_path = selector_path

        module.permissions_required = (
            permissions_required or {}
        )

        module.is_system = is_system

        module.is_enabled = True

        module.save(
            update_fields=[
                "label",
                "description",
                "icon",
                "anchors",
                "supports_company_rollup",
                "requires",
                "selector_path",
                "permissions_required",
                "is_system",
                "is_enabled",
                "updated_at",
            ]
        )

        return module
