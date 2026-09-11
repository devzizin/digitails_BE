from apps.blocks.storages.constants import (
    BLOCKS_NAMESPACE,
    CONNECTION_RESOURCE,
    STORAGE_RESOURCE,
)
from apps.core.permissions.constants import Actions, Levels
from apps.core.permissions.utils.permission_builder import PermissionBuilder

# =====================================================
# STORAGE PERMISSIONS
# =====================================================

STORAGE_LIST = PermissionBuilder.build_permission_code(
    namespace=BLOCKS_NAMESPACE,
    resource=STORAGE_RESOURCE,
    action=Actions.LIST,
)

STORAGE_CREATE = PermissionBuilder.build_permission_code(
    namespace=BLOCKS_NAMESPACE,
    resource=STORAGE_RESOURCE,
    action=Actions.CREATE,
)

STORAGE_READ = PermissionBuilder.build_permission_code(
    namespace=BLOCKS_NAMESPACE,
    resource=STORAGE_RESOURCE,
    action=Actions.READ,
)

STORAGE_UPDATE = PermissionBuilder.build_permission_code(
    namespace=BLOCKS_NAMESPACE,
    resource=STORAGE_RESOURCE,
    action=Actions.UPDATE,
)

STORAGE_DELETE = PermissionBuilder.build_permission_code(
    namespace=BLOCKS_NAMESPACE,
    resource=STORAGE_RESOURCE,
    action=Actions.DELETE,
)

# =====================================================
# CONNECTION PERMISSIONS (admin-only)
# =====================================================

STORAGE_CONNECTION_LIST = PermissionBuilder.build_permission_code(
    namespace=BLOCKS_NAMESPACE,
    resource=CONNECTION_RESOURCE,
    action=Actions.LIST,
)

STORAGE_CONNECTION_CREATE = PermissionBuilder.build_permission_code(
    namespace=BLOCKS_NAMESPACE,
    resource=CONNECTION_RESOURCE,
    action=Actions.CREATE,
)
