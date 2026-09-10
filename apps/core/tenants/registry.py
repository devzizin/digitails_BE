from apps.core.permissions.constants import Actions
from apps.core.tenants.constants import (
    MODULE_CODE,
    TENANT_DESCRIPTION,
    TENANT_LABEL,
    TENANT_RESOURCE,
)
from apps.core.tenants.permissions import (
    TENANT_ACTIVATE,
    TENANT_CREATE,
    TENANT_DEACTIVATE,
    TENANT_LIST,
    TENANT_READ,
    TENANT_UPDATE,
)

# =====================================================
# MODULE
# =====================================================

MODULE = {
    "code": MODULE_CODE,

    "label": TENANT_LABEL,

    "description": TENANT_DESCRIPTION,

    "anchors": [],

    "selector_path": (
        "apps.core.tenants.selectors."
        "list_tenants"
    ),

    "permissions_required": {
        "read": TENANT_READ,
    },

    "supports_company_rollup": False,

    "requires": [],

    "is_system": True,
}

# =====================================================
# ENTITY TYPES
# =====================================================

ENTITY_TYPES = []

# =====================================================
# PERMISSIONS
# =====================================================

PERMISSIONS = [
    {
        "code": TENANT_LIST,
        "action": Actions.LIST,
        "resource_type": TENANT_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "List tenants",
    },
    {
        "code": TENANT_CREATE,
        "action": Actions.CREATE,
        "resource_type": TENANT_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Create tenant",
    },
    {
        "code": TENANT_READ,
        "action": Actions.READ,
        "resource_type": TENANT_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Read tenant",
    },
    {
        "code": TENANT_UPDATE,
        "action": Actions.UPDATE,
        "resource_type": TENANT_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Update tenant",
    },
    {
        "code": TENANT_ACTIVATE,
        "action": Actions.ACTIVATE,
        "resource_type": TENANT_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Activate tenant",
    },
    {
        "code": TENANT_DEACTIVATE,
        "action": Actions.DEACTIVATE,
        "resource_type": TENANT_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Deactivate tenant",
    },
]
