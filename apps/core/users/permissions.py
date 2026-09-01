from apps.core.users.constants import USER_RESOURCE, CORE_NAMESPACE
from apps.core.permissions.utils.permission_builder import PermissionBuilder
from apps.core.permissions.constants import Actions, Levels


USER_LIST = PermissionBuilder.build_permission_code(
    resource=USER_RESOURCE,
    namespace=CORE_NAMESPACE,
    action=Actions.LIST,
)

USER_CREATE = PermissionBuilder.build_permission_code(
    resource=USER_RESOURCE,
    namespace=CORE_NAMESPACE,
    action=Actions.CREATE,
)  

USER_READ = PermissionBuilder.build_permission_code(
    resource=USER_RESOURCE,
    namespace=CORE_NAMESPACE,
    action=Actions.READ,
)

USER_UPDATE = PermissionBuilder.build_permission_code(
    resource=USER_RESOURCE,
    namespace=CORE_NAMESPACE,
    action=Actions.UPDATE, 
)

USER_DELETE = PermissionBuilder.build_permission_code(
    resource=USER_RESOURCE,
    namespace=CORE_NAMESPACE,
    action=Actions.DELETE,
)

USER_ASSIGN = PermissionBuilder.build_permission_code(
    resource=USER_RESOURCE,
    namespace=CORE_NAMESPACE,
    action=Actions.ASSIGN,
)

USER_MANAGE = PermissionBuilder.build_permission_code(
    resource=USER_RESOURCE,
    namespace=CORE_NAMESPACE,
    action=Actions.MANAGE,
)

USER_ADMIN_TEMPLATE = PermissionBuilder.build_template_code(
    resource=USER_RESOURCE,
    namespace=CORE_NAMESPACE,
    level=Levels.ADMIN,
)

USER_VIEWER_TEMPLATE = PermissionBuilder.build_template_code(
    resource=USER_RESOURCE,
    namespace=CORE_NAMESPACE,
    level=Levels.VIEWER,
)

