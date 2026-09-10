from apps.core.tenants.constants import TENANT_RESOURCE, CORE_NAMESPACE
from apps.core.permissions.utils.permission_builder import PermissionBuilder
from apps.core.permissions.constants import Actions, Levels


TENANT_LIST = PermissionBuilder.build_permission_code(
    resource=TENANT_RESOURCE,
    namespace=CORE_NAMESPACE,
    action=Actions.LIST,
)

TENANT_CREATE = PermissionBuilder.build_permission_code(
    resource=TENANT_RESOURCE,
    namespace=CORE_NAMESPACE,
    action=Actions.CREATE,
)

TENANT_READ = PermissionBuilder.build_permission_code(
    resource=TENANT_RESOURCE,
    namespace=CORE_NAMESPACE,
    action=Actions.READ,
)

TENANT_UPDATE = PermissionBuilder.build_permission_code(
    resource=TENANT_RESOURCE,
    namespace=CORE_NAMESPACE,
    action=Actions.UPDATE,
)

TENANT_DELETE = PermissionBuilder.build_permission_code(
    resource=TENANT_RESOURCE,
    namespace=CORE_NAMESPACE,
    action=Actions.DELETE,
)

TENANT_ACTIVATE = PermissionBuilder.build_permission_code(
    resource=TENANT_RESOURCE,
    namespace=CORE_NAMESPACE,
    action=Actions.ACTIVATE,
)

TENANT_DEACTIVATE = PermissionBuilder.build_permission_code(
    resource=TENANT_RESOURCE,
    namespace=CORE_NAMESPACE,
    action=Actions.DEACTIVATE,
)

