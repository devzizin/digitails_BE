from apps.core.permissions.constants import Actions
from apps.core.users.constants import (
    MODULE_CODE,
    USER_DESCRIPTION,
    USER_LABEL,
    USER_RESOURCE,
)
from apps.core.users.permissions import (
    USER_ACTIVATE,
    USER_CREATE,
    USER_DEACTIVATE,
    USER_DELETE,
    USER_LIST,
    USER_MANAGE,
    USER_READ,
    USER_UPDATE,
)

MODULE = {
    "code": MODULE_CODE,
    "label": USER_LABEL,
    "description": USER_DESCRIPTION,
    "anchors": [],
    "selector_path": "apps.core.users.selectors.UserSelector.get_users",
    "permissions_required": {
        "read": USER_READ,
    },
    "supports_company_rollup": False,
    "requires": [],
    "is_system": True,
}


# =====================================================
# USERS HAVE NO ENTITY TYPE
# =====================================================

ENTITY_TYPES = []


PERMISSIONS = [
    {
        "code": USER_LIST,
        "action": Actions.LIST,
        "resource_type": USER_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "List users",
    },
    {
        "code": USER_READ,
        "action": Actions.READ,
        "resource_type": USER_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Read user",
    },
    {
        "code": USER_CREATE,
        "action": Actions.CREATE,
        "resource_type": USER_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Create user invitations",
    },
    {
        "code": USER_UPDATE,
        "action": Actions.UPDATE,
        "resource_type": USER_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Update user",
    },
    {
        "code": USER_DELETE,
        "action": Actions.DELETE,
        "resource_type": USER_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Delete user",
    },
    {
        "code": USER_MANAGE,
        "action": Actions.MANAGE,
        "resource_type": USER_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Manage user access and permissions",
    },
    {
        "code": USER_ACTIVATE,
        "action": Actions.ACTIVATE,
        "resource_type": USER_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Activate user",
    },
    {
        "code": USER_DEACTIVATE,
        "action": Actions.DEACTIVATE,
        "resource_type": USER_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Deactivate user",
    },
]

