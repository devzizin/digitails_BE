from apps.business.assets.constants import (
    ASSET_RESOURCE,
    ASSET_TYPE_RESOURCE,
    BUSINESS_NAMESPACE,
)
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
ASSET_TYPE_LIST = PermissionBuilder.build_permission_code(
    namespace=BUSINESS_NAMESPACE,
    resource=ASSET_TYPE_RESOURCE,
    action=Actions.LIST,
)

ASSET_TYPE_CREATE = PermissionBuilder.build_permission_code(
    namespace=BUSINESS_NAMESPACE,
    resource=ASSET_TYPE_RESOURCE,
    action=Actions.CREATE,
)

ASSET_TYPE_READ = PermissionBuilder.build_permission_code(
    namespace=BUSINESS_NAMESPACE,
    resource=ASSET_TYPE_RESOURCE,
    action=Actions.READ,
)

ASSET_TYPE_UPDATE = PermissionBuilder.build_permission_code(
    namespace=BUSINESS_NAMESPACE,
    resource=ASSET_TYPE_RESOURCE,
    action=Actions.UPDATE,
)

ASSET_TYPE_DELETE = PermissionBuilder.build_permission_code(
    namespace=BUSINESS_NAMESPACE,
    resource=ASSET_TYPE_RESOURCE,
    action=Actions.DELETE,
)
