from apps.core.entities.constants import ENTITY_RESOURCE, CORE_NAMESPACE
from apps.core.permissions.utils.permission_builder import PermissionBuilder
from apps.core.permissions.constants import Actions, Levels


ENTITY_LIST = PermissionBuilder.build_permission_code(
    resource=ENTITY_RESOURCE,
    namespace=CORE_NAMESPACE,
    action=Actions.LIST,
)

ENTITY_CREATE = PermissionBuilder.build_permission_code(
    resource=ENTITY_RESOURCE,
    namespace=CORE_NAMESPACE,
    action=Actions.CREATE,
)

ENTITY_READ = PermissionBuilder.build_permission_code(
    resource=ENTITY_RESOURCE,
    namespace=CORE_NAMESPACE,
    action=Actions.READ,
)

ENTITY_UPDATE = PermissionBuilder.build_permission_code(
    resource=ENTITY_RESOURCE,
    namespace=CORE_NAMESPACE,
    action=Actions.UPDATE,
)   


ENTITY_DELETE = PermissionBuilder.build_permission_code(
    resource=ENTITY_RESOURCE,
    namespace=CORE_NAMESPACE,
    action=Actions.DELETE,
)

