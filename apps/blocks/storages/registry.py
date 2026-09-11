from apps.blocks.storages.constants import (
    CONNECTION_RESOURCE,
    DRIVE_DESCRIPTION,
    DRIVE_LABEL,
    DRIVE_RESOURCE,
    MODULE_CODE,
)
from apps.blocks.storages.permissions import (
    DRIVE_CONNECTION_CREATE,
    DRIVE_CONNECTION_LIST,
    DRIVE_CREATE,
    DRIVE_DELETE,
    DRIVE_LIST,
    DRIVE_READ,
    DRIVE_UPDATE,
)
from apps.core.permissions.constants import Actions

# =====================================================
# MODULE
# =====================================================

MODULE = {
    "code": MODULE_CODE,
    "label": DRIVE_LABEL,
    "description": DRIVE_DESCRIPTION,
    "anchors": [],
    "selector_path": (
        "apps.blocks.drive.selectors.accessibility_selectors."
        "DriveAccessibilitySelector.list_accessible_organisations"
    ),
    "permissions_required": {
        "read": DRIVE_READ,
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
        "code": DRIVE_LIST,
        "action": Actions.LIST,
        "resource_type": DRIVE_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "List drive files and folders",
    },
    {
        "code": DRIVE_CREATE,
        "action": Actions.CREATE,
        "resource_type": DRIVE_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Upload files and create folders",
    },
    {
        "code": DRIVE_READ,
        "action": Actions.READ,
        "resource_type": DRIVE_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Read drive files and folders",
    },
    {
        "code": DRIVE_UPDATE,
        "action": Actions.UPDATE,
        "resource_type": DRIVE_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Move, copy, and restore drive items",
    },
    {
        "code": DRIVE_DELETE,
        "action": Actions.DELETE,
        "resource_type": DRIVE_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Delete drive files and folders",
    },
    {
        "code": DRIVE_CONNECTION_LIST,
        "action": Actions.LIST,
        "resource_type": CONNECTION_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "List storage connections",
    },
    {
        "code": DRIVE_CONNECTION_CREATE,
        "action": Actions.CREATE,
        "resource_type": CONNECTION_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Create storage connections",
    },
]
