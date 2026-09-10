from apps.business.assets.constants import (
    ASSET_DESCRIPTION,
    ASSET_ENTITY_TYPE_CODE,
    ASSET_LABEL,
    ASSET_RESOURCE,
    ASSET_TYPE_DESCRIPTION,
    ASSET_TYPE_ENTITY_TYPE_CODE,
    ASSET_TYPE_LABEL,
    ASSET_TYPE_RESOURCE,
    MODULE_CODE,
)
from apps.business.assets.permissions import (
    ASSET_CREATE,
    ASSET_DELETE,
    ASSET_LIST,
    ASSET_READ,
    ASSET_UPDATE,
    ASSET_TYPE_CREATE,
    ASSET_TYPE_DELETE,
    ASSET_TYPE_LIST,
    ASSET_TYPE_READ,
    ASSET_TYPE_UPDATE,
)
from apps.core.permissions.constants import Actions

# =====================================================
# MODULE
# =====================================================

MODULE = {
    "code": MODULE_CODE,
    "label": ASSET_LABEL,
    "description": ASSET_DESCRIPTION,
    "anchors": [
        ASSET_ENTITY_TYPE_CODE,
        ASSET_TYPE_ENTITY_TYPE_CODE,
    ],
    "selector_path": "apps.business.assets.selectors." "AssetSelector.list_assets",
    "permissions_required": {
        "read": ASSET_READ,
    },
    "supports_company_rollup": True,
    "requires": [
        "addresses",
    ],
    "is_system": True,
}

# =====================================================
# ENTITY TYPES
# =====================================================

ENTITY_TYPES = [
    {
        "code": ASSET_ENTITY_TYPE_CODE,
        "module_code": MODULE_CODE,
        "label": ASSET_LABEL,
        "description": ASSET_DESCRIPTION,
        "is_system": True,
    },
    {
        "code": ASSET_TYPE_ENTITY_TYPE_CODE,
        "module_code": MODULE_CODE,
        "label": ASSET_TYPE_LABEL,
        "description": ASSET_TYPE_DESCRIPTION,
        "is_system": True,
    },
]

# =====================================================
# PERMISSIONS
# =====================================================

PERMISSIONS = [
    {
        "code": ASSET_LIST,
        "action": Actions.LIST,
        "resource_type": ASSET_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "List assets",
    },
    {
        "code": ASSET_CREATE,
        "action": Actions.CREATE,
        "resource_type": ASSET_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Create asset",
    },
    {
        "code": ASSET_READ,
        "action": Actions.READ,
        "resource_type": ASSET_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Read asset",
    },
    {
        "code": ASSET_UPDATE,
        "action": Actions.UPDATE,
        "resource_type": ASSET_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Update asset",
    },
    {
        "code": ASSET_DELETE,
        "action": Actions.DELETE,
        "resource_type": ASSET_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Delete asset",
    },
    {
        "code": ASSET_TYPE_LIST,
        "action": Actions.LIST,
        "resource_type": ASSET_TYPE_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "List asset types",
    },
    {
        "code": ASSET_TYPE_CREATE,
        "action": Actions.CREATE,
        "resource_type": ASSET_TYPE_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Create asset type",
    },
    {
        "code": ASSET_TYPE_READ,
        "action": Actions.READ,
        "resource_type": ASSET_TYPE_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Read asset type",
    },
    {
        "code": ASSET_TYPE_UPDATE,
        "action": Actions.UPDATE,
        "resource_type": ASSET_TYPE_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Update asset type",
    },
    {
        "code": ASSET_TYPE_DELETE,
        "action": Actions.DELETE,
        "resource_type": ASSET_TYPE_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Delete asset type",
    },
]