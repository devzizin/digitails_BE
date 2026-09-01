from apps.business.assets.constants import ASSET_RESOURCE, BUSINESS_NAMESPACE
from apps.core.permissions.utils.permission_builder import PermissionBuilder
from apps.core.permissions.constants import Actions, Levels


ASSET_LIST = PermissionBuilder.build_permission_code(
    resource=ASSET_RESOURCE,
    namespace=BUSINESS_NAMESPACE,
    action=Actions.LIST,
)

ASSET_CREATE = PermissionBuilder.build_permission_code(
    resource=ASSET_RESOURCE,
    namespace=BUSINESS_NAMESPACE,
    action=Actions.CREATE,
)

ASSET_READ = PermissionBuilder.build_permission_code(
    resource=ASSET_RESOURCE,
    namespace=BUSINESS_NAMESPACE,
    action=Actions.READ,
)

ASSET_UPDATE = PermissionBuilder.build_permission_code(
    resource=ASSET_RESOURCE,
    namespace=BUSINESS_NAMESPACE,
    action=Actions.UPDATE,
)

ASSET_DELETE = PermissionBuilder.build_permission_code(
    resource=ASSET_RESOURCE,
    namespace=BUSINESS_NAMESPACE,
    action=Actions.DELETE,
)

ASSET_ADMIN_TEMPLATE = PermissionBuilder.build_template_code(
    resource=ASSET_RESOURCE,
    namespace=BUSINESS_NAMESPACE,
    level=Levels.ADMIN,
)

ASSET_VIEWER_TEMPLATE = PermissionBuilder.build_template_code(
    resource=ASSET_RESOURCE,
    namespace=BUSINESS_NAMESPACE,
    level=Levels.VIEWER,
)

