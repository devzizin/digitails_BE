from apps.core.entities.constants import ENTITY_LABEL, ENTITY_RESOURCE, MODULE_CODE
from apps.core.entities.permissions import (
    ENTITY_CREATE,
    ENTITY_DELETE,
    ENTITY_LIST,
    ENTITY_READ,
    ENTITY_UPDATE,
)
from apps.core.permissions.constants import Actions

# MODULE
MODULE = {
    "code": MODULE_CODE,

    "label": ENTITY_LABEL,

    "description": (
        "Universal platform entity graph module."
    ),

    "anchors": [],

    "selector_path": (
        "apps.core.entities.selectors."
        "list_entities"
    ),

    "permissions_required": {
        "read": ENTITY_READ,
    },

    "supports_company_rollup": True,

    "requires": [],

    "is_system": True,
}

# ENTITY TYPES
ENTITY_TYPES = []

# PERMISSIONS
PERMISSIONS = [
    {
        "code": ENTITY_LIST,
        "action": Actions.LIST,
        "resource_type": ENTITY_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "List entities",
    },
    {
        "code": ENTITY_CREATE,
        "action": Actions.CREATE,
        "resource_type": ENTITY_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Create entity",
    },
    {
        "code": ENTITY_READ,
        "action": Actions.READ,
        "resource_type": ENTITY_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Read entity",
    },
    {
        "code": ENTITY_UPDATE,
        "action": Actions.UPDATE,
        "resource_type": ENTITY_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Update entity",
    },
    {
        "code": ENTITY_DELETE,
        "action": Actions.DELETE,
        "resource_type": ENTITY_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Delete entity",
    },
]
