from apps.core.permissions.validators.permission_validator import PermissionValidators



class PermissionBuilder:

    @classmethod
    def build_permission_code(
        cls,
        *,
        namespace: str,
        resource: str,
        action: str,
    ) -> str:
        PermissionValidators.validate_namespace(namespace)
        PermissionValidators.validate_resource(resource)
        PermissionValidators.validate_action(action)

        code = f"{namespace}.{resource}.{action}"

        PermissionValidators.validate_permission_code(code)

        return code

    @classmethod
    def build_template_code(
        cls,
        *,
        namespace: str,
        level: str,
        resource: str | None = None,
    ) -> str:
        PermissionValidators.validate_namespace(namespace)
        PermissionValidators.validate_template_level(level)

        if resource:
            PermissionValidators.validate_resource(resource)
            code = f"{namespace}.{resource}.{level}"
        else:
            code = f"{namespace}.{level}"

        PermissionValidators.validate_template_code(code)

        return code