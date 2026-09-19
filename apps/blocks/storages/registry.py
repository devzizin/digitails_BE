from apps.blocks.storages.constants import (
    CONNECTION_RESOURCE,
    STORAGE_DESCRIPTION,
    STORAGE_LABEL,
    STORAGE_RESOURCE,
    MODULE_CODE,
)
from apps.blocks.storages.permissions import (
    STORAGE_CONNECTION_CREATE,
    STORAGE_CONNECTION_LIST,
    STORAGE_CREATE,
    STORAGE_DELETE,
    STORAGE_LIST,
    STORAGE_READ,
    STORAGE_UPDATE,
)
from apps.core.permissions.constants import Actions

# =====================================================
# MODULE
# =====================================================

MODULE = {
    "code": MODULE_CODE,
    "label": STORAGE_LABEL,
    "description": STORAGE_DESCRIPTION,
    "anchors": [],
    "selector_path": (
        "apps.blocks.storage.selectors.file_selectors.get_list_file_by_entity_type"
    ),
    "permissions_required": {
        "read": STORAGE_READ,
    },
    "supports_company_rollup": True,
    "requires": [],
    "is_system": True,
}

# =====================================================
# PERMISSIONS
# =====================================================

PERMISSIONS = [
    {
        "code": STORAGE_LIST,
        "action": Actions.LIST,
        "resource_type": STORAGE_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "List storage items",
    },
    {
        "code": STORAGE_CREATE,
        "action": Actions.CREATE,
        "resource_type": STORAGE_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Upload files and create folders",
    },
    {
        "code": STORAGE_READ,
        "action": Actions.READ,
        "resource_type": STORAGE_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Read storage files and folders",
    },
    {
        "code": STORAGE_UPDATE,
        "action": Actions.UPDATE,
        "resource_type": STORAGE_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Move, copy, and restore storage items",
    },
    {
        "code": STORAGE_DELETE,
        "action": Actions.DELETE,
        "resource_type": STORAGE_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Delete storage files and folders",
    },
    {
        "code": STORAGE_CONNECTION_LIST,
        "action": Actions.LIST,
        "resource_type": CONNECTION_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "List storage connections",
    },
    {
        "code": STORAGE_CONNECTION_CREATE,
        "action": Actions.CREATE,
        "resource_type": CONNECTION_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Create storage connections",
    },
]
