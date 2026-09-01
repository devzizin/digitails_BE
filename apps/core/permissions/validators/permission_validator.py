"""
Canonical RBAC permission validators.

IMPORTANT:
These rules MUST stay stable after production launch.

RBAC rules:
- namespace = logical application boundary
- resource = singular snake_case
- action = lowercase singular verb
- level = lowercase singular
- separator = dot

Examples:
- permission: core.company.read
- permission: business.assets.vehicle.update
- resource template: core.company.admin
- app template: business.assets.viewer
- root template: tenant.admin
"""

import re

from apps.core.permissions.exceptions import (
    InvalidAction,
    InvalidNamespace,
    InvalidPermissionCode,
    InvalidResource,
    InvalidTemplateCode,
    InvalidTemplateLevel,
)
# from apps.core.permissions.resource_scope_registry import ResourceScopeRegistry


class PermissionValidators:
    """
    Canonical RBAC validators.

    Responsible ONLY for:
    - permissions
    - templates
    - RBAC hierarchy
    - actions
    - levels
    """

    VALID_ACTIONS = {
        "list",
        "create",
        "read",
        "update",
        "delete",
        "assign",
        "manage",
        "export",
        "activate",
        "deactivate",
        "change_status",
    }

    VALID_TEMPLATE_LEVELS = {
        "admin",
        "manager",
        "editor",
        "viewer",
        "contributor",
        "restricted",
        "assignee",
    }

    ROOT_TEMPLATE_NAMESPACES = {
        "tenant",
        "platform",
    }

    MAX_PERMISSION_CODE_LENGTH = 100
    MAX_TEMPLATE_CODE_LENGTH = 100

    RESOURCE_REGEX = re.compile(r"^[a-z][a-z0-9_]*$")
    NAMESPACE_REGEX = re.compile(r"^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)*$")

    @classmethod
    def validate_action(
        cls,
        action: str,
    ) -> None:

        if not action:
            raise InvalidAction(action)

        if action != action.lower():
            raise InvalidAction(action)

        if action not in cls.VALID_ACTIONS:
            raise InvalidAction(action)

    @classmethod
    def validate_resource(
        cls,
        resource: str,
    ) -> None:
        """
        Validate RBAC resource segment.

        Valid:
            company
            custom_field
            leave_request

        Invalid:
            core.company
            Company
            company-profile
        """

        if not resource:
            raise InvalidResource(resource)

        if "." in resource:
            raise InvalidResource(resource)

        if not cls.RESOURCE_REGEX.match(resource):
            raise InvalidResource(resource)

    @classmethod
    def validate_namespace(
        cls,
        namespace: str,
    ) -> None:
        """
        Validate RBAC namespace.

        Valid:
            core
            business.assets

        Invalid:
            business-assets
            Core
        """

        if not namespace:
            raise InvalidNamespace(namespace)

        if not cls.NAMESPACE_REGEX.match(namespace):
            raise InvalidNamespace(namespace)

    @classmethod
    def validate_template_level(
        cls,
        level: str,
    ) -> None:

        if not level:
            raise InvalidTemplateLevel(level)

        if level != level.lower():
            raise InvalidTemplateLevel(level)

        if level not in cls.VALID_TEMPLATE_LEVELS:
            raise InvalidTemplateLevel(level)

    @classmethod
    def split_permission_code(
        cls,
        code: str,
    ) -> tuple[str, str, str]:
        """
        Split permission code.

        Example:
            core.company.read
            -> ("core", "company", "read")
        """

        if not code:
            raise InvalidPermissionCode(code)

        if len(code) > cls.MAX_PERMISSION_CODE_LENGTH:
            raise InvalidPermissionCode(code)

        parts = code.split(".")

        if len(parts) < 3:
            raise InvalidPermissionCode(code)

        namespace = ".".join(parts[:-2])
        resource = parts[-2]
        action = parts[-1]

        return namespace, resource, action

    @classmethod
    def split_template_code(
        cls,
        code: str,
    ) -> tuple[str, str | None, str]:
        """
        Split template code.

        Resource template:
            core.company.admin

        App/root template:
            core.admin
            tenant.admin
        """

        if not code:
            raise InvalidTemplateCode(code)

        if len(code) > cls.MAX_TEMPLATE_CODE_LENGTH:
            raise InvalidTemplateCode(code)

        parts = code.split(".")

        if len(parts) < 2:
            raise InvalidTemplateCode(code)

        level = parts[-1]

        if len(parts) == 2:
            namespace = parts[0]
            return namespace, None, level

        namespace = ".".join(parts[:-2])
        resource = parts[-2]

        return namespace, resource, level

    @classmethod
    def validate_permission_code(
        cls,
        code: str,
    ) -> None:
        """
        Validate permission code.

        Format:
            namespace.resource.action
        """

        namespace, resource, action = cls.split_permission_code(code)

        cls.validate_namespace(namespace)
        cls.validate_resource(resource)
        cls.validate_action(action)


    @classmethod
    def validate_template_code(
        cls,
        code: str,
    ) -> None:
        """
        Validate role/template code.
        """
        namespace, resource, level = cls.split_template_code(code)

        cls.validate_template_level(level)
        cls.validate_namespace(namespace)

        if resource is not None:
            cls.validate_resource(resource)

    # @classmethod
    # def validate_resource_template_code(
    #     cls,
    #     code: str,
    # ) -> None:
    #     """
    #     Validate resource-level template.
    #     """

    #     namespace, resource, level = cls.split_template_code(code)

    #     if resource is None:
    #         raise InvalidTemplateCode(code)

    #     cls.validate_namespace(namespace)
    #     cls.validate_resource(resource)
    #     cls.validate_template_level(level)

    # @classmethod
    # def validate_app_level_code(
    #     cls,
    #     code: str,
    # ) -> None:
    #     """
    #     Validate app-level/root template.
    #     """

    #     namespace, resource, level = cls.split_template_code(code)

    #     if resource is not None:
    #         raise InvalidTemplateCode(code)

    #     cls.validate_namespace(namespace)
    #     cls.validate_template_level(level)



    # @classmethod
    # def validate_template_permissions(
    #     cls,
    #     *,
    #     template_code: str,
    #     permission_codes: list[str],
    # ) -> None:
    #     """
    #     Validate template permission consistency.
    #     """

    #     cls.validate_template_code(template_code)

    #     if not permission_codes:
    #         return

    #     namespace, resource, _level = cls.split_template_code(template_code)

    #     if resource is None:
    #         return

    #     template_prefix = f"{namespace}.{resource}."

    #     for permission_code in permission_codes:
    #         cls.validate_permission_code(permission_code)

    #         if not permission_code.startswith(template_prefix):
    #             raise InvalidTemplatePermissions(
    #                 template_code,
    #                 permission_code,
    #             )

    # @classmethod
    # def validate_app_levels(
    #     cls,
    #     app_levels: dict[str, list[str]],
    # ) -> None:
    #     """
    #     Validate APP_LEVELS hierarchy.
    #     """

    #     if not app_levels:
    #         return

    #     if not isinstance(app_levels, dict):
    #         raise InvalidTemplateCode(str(app_levels))

    #     for (
    #         app_template_code,
    #         template_codes,
    #     ) in app_levels.items():

    #         cls.validate_app_level_code(app_template_code)

    #         if not isinstance(
    #             template_codes,
    #             list,
    #         ):
    #             raise InvalidTemplatePermissions(
    #                 app_template_code,
    #                 str(template_codes),
    #             )

    #         (
    #             app_namespace,
    #             _app_resource,
    #             _app_level,
    #         ) = cls.split_template_code(app_template_code)

    #         for template_code in template_codes:

    #             cls.validate_template_code(template_code)

    #             (
    #                 template_namespace,
    #                 _resource,
    #                 _level,
    #             ) = cls.split_template_code(template_code)

    #             if app_namespace == "tenant":
    #                 continue

    #             if app_namespace == "platform":

    #                 if template_namespace != "platform":
    #                     raise InvalidTemplatePermissions(
    #                         app_template_code,
    #                         template_code,
    #                     )

    #                 continue

    #             if template_namespace != app_namespace:
    #                 raise InvalidTemplatePermissions(
    #                     app_template_code,
    #                     template_code,
    #                 )

    # @classmethod
    # def validate_role_entity(
    #     cls,
    #     *,
    #     template_code: str,
    #     entity_type_code: str,
    # ) -> None:
    #     """
    #     Validate role template applicability
    #     to entity type.

    #     Example:

    #         core.company.admin
    #             -> core.company

    #         core.organisation.viewer
    #             -> core.organisation
    #     """

    #     namespace, resource, _ = cls.split_template_code(
    #         template_code,
    #     )

    #     if resource is None:
    #         return

    #     allowed_entity_types = ResourceScopeRegistry.get_allowed_entity_types(
    #         resource=resource,
    #     )

    #     if allowed_entity_types:

    #         if entity_type_code not in allowed_entity_types:
    #             raise InvalidRoleResource(
    #                 role_code=template_code,
    #                 entity_type_code=entity_type_code,
    #             )

    #         return

    #     expected = f"{namespace}.{resource}"

    #     if expected != entity_type_code:
    #         raise InvalidRoleResource(
    #             role_code=template_code,
    #             entity_type_code=entity_type_code,
    #         )
