from apps.core.companies.constants import COMPANY_RESOURCE, CORE_NAMESPACE
from apps.core.permissions.constants import Actions, Levels
from apps.core.permissions.utils.permission_builder import PermissionBuilder



# =====================================================
# PERMISSIONS
# =====================================================

COMPANY_LIST = (
    PermissionBuilder.build_permission_code(
        namespace=CORE_NAMESPACE,
        resource=COMPANY_RESOURCE,
        action=Actions.LIST,
    )
)

COMPANY_CREATE = (
    PermissionBuilder.build_permission_code(
        namespace=CORE_NAMESPACE,
        resource=COMPANY_RESOURCE,
        action=Actions.CREATE,
    )
)

COMPANY_READ = (
    PermissionBuilder.build_permission_code(
        namespace=CORE_NAMESPACE,
        resource=COMPANY_RESOURCE,
        action=Actions.READ,
    )
)

COMPANY_UPDATE = (
    PermissionBuilder.build_permission_code(
        namespace=CORE_NAMESPACE,
        resource=COMPANY_RESOURCE,
        action=Actions.UPDATE,
    )
)

COMPANY_DELETE = (
    PermissionBuilder.build_permission_code(
        namespace=CORE_NAMESPACE,
        resource=COMPANY_RESOURCE,
        action=Actions.DELETE,
    )
)

# =====================================================
# ROLE TEMPLATES
# =====================================================

COMPANY_ADMIN_TEMPLATE = (
    PermissionBuilder.build_template_code(
        namespace=CORE_NAMESPACE,
        resource=COMPANY_RESOURCE,
        level=Levels.ADMIN,
    )
)

COMPANY_VIEWER_TEMPLATE = (
    PermissionBuilder.build_template_code(
        namespace=CORE_NAMESPACE,
        resource=COMPANY_RESOURCE,
        level=Levels.VIEWER,
    )
)

# =====================================================
# APP LEVELS
# =====================================================

COMPANY_APP_ADMIN = (
    PermissionBuilder.build_template_code(
        namespace=CORE_NAMESPACE,
        level=Levels.ADMIN,
    )
)

COMPANY_APP_VIEWER = (
    PermissionBuilder.build_template_code(
        namespace=CORE_NAMESPACE,
        level=Levels.VIEWER,
    )
)
