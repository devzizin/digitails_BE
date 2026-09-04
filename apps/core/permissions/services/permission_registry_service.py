from apps.core.permissions.models import (
    Permission,
    RoleTemplate,
    RoleTemplatePermission,
)
from apps.core.permissions.validators.permission_validator import PermissionValidators


class PermissionRegistryService:

    @staticmethod
    def register_permission(
        *,
        code: str,
        action: str,
        resource_type: str,
        module_code: str,
        description: str = "",
    ) -> Permission:

        # VALIDATION
        PermissionValidators.validate_permission_code(code)
        PermissionValidators.validate_action(action)
        PermissionValidators.validate_resource(resource_type)
        _, resource, parsed_action = PermissionValidators.split_permission_code(code)

        # CONSISTENCY CHECKS
        if resource != resource_type:
            raise RuntimeError(
                f"Permission resource mismatch: "
                f"code='{code}' "
                f"resource='{resource}' "
                f"resource_type='{resource_type}'"
            )

        if parsed_action != action:
            raise RuntimeError(
                f"Permission action mismatch: "
                f"code='{code}' "
                f"parsed_action='{parsed_action}' "
                f"action='{action}'"
            )

        obj, _ = Permission.objects.update_or_create(
            code=code,
            defaults={
                "action": action,
                "resource_type": resource_type,
                "module_code": module_code,
                "description": description,
                "is_system": True,
            },
        )

        return obj

    @staticmethod
    def sync_template(
        *,
        code,
        label,
        description=None,
        permission_codes=None,
        is_system=False,
    ):

        PermissionValidators.validate_resource_template_code(code)
        PermissionValidators.validate_template_permissions(
            template_code=code,
            permission_codes=permission_codes or [],
        )

        if not isinstance(label, str) or not label.strip():
            raise RuntimeError(f"Invalid role template label " f"for '{code}'")

        role, _ = RoleTemplate.objects.get_or_create(
            code=code,
            defaults={
                "label": label,
                "description": description or "",
                "is_system": is_system,
            },
        )

        role.label = label
        role.description = description or ""
        role.is_system = is_system
        role.save()

        if permission_codes is not None:

            permissions_map = {
                p.code: p for p in Permission.objects.filter(code__in=permission_codes)
            }

            found_codes = set(permissions_map.keys())
            missing = set(permission_codes) - found_codes
            if missing:
                raise RuntimeError(
                    f"Permissions not found " f"for role '{code}': " f"{missing}"
                )

            permissions = [
                permissions_map[permission_code] for permission_code in permission_codes
            ]

            RoleTemplatePermission.objects.filter(role_template=role).delete()

            RoleTemplatePermission.objects.bulk_create(
                [
                    RoleTemplatePermission(
                        role_template=role,
                        permission=p,
                    )
                    for p in permissions
                ]
            )

        return role
