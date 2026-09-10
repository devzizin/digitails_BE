from apps.core.companies.constants import (
    COMPANY_DESCRIPTION,
    COMPANY_ENTITY_TYPE_CODE,
    COMPANY_LABEL,
    COMPANY_RESOURCE,
    MODULE_CODE,
)
from apps.core.companies.permissions import (
    COMPANY_CREATE,
    COMPANY_DELETE,
    COMPANY_LIST,
    COMPANY_READ,
    COMPANY_UPDATE,
)
from apps.core.permissions.constants import Actions

MODULE = {
    "code": MODULE_CODE,

    "label": COMPANY_LABEL,

    "description": COMPANY_DESCRIPTION,

    "anchors": [
        COMPANY_ENTITY_TYPE_CODE,
    ],

    "selector_path": (
        "apps.core.companies.selectors."
        "CompanySelector.list_companies"
    ),

    "permissions_required": {
        "read": COMPANY_READ,
    },

    "supports_company_rollup": True,

    "requires": [],

    "is_system": True,
}


ENTITY_TYPES = [
    {
        "code": COMPANY_ENTITY_TYPE_CODE,
        "module_code": MODULE_CODE,
        "label": COMPANY_LABEL,
        "description": COMPANY_DESCRIPTION,
        "is_system": True,
    }
]


PERMISSIONS = [
    {
        "code": COMPANY_LIST,
        "action": Actions.LIST,
        "resource_type": COMPANY_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "List companies",
    },
    {
        "code": COMPANY_CREATE,
        "action": Actions.CREATE,
        "resource_type": COMPANY_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Create company",
    },
    {
        "code": COMPANY_READ,
        "action": Actions.READ,
        "resource_type": COMPANY_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Read company",
    },
    {
        "code": COMPANY_UPDATE,
        "action": Actions.UPDATE,
        "resource_type": COMPANY_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Update company",
    },
    {
        "code": COMPANY_DELETE,
        "action": Actions.DELETE,
        "resource_type": COMPANY_RESOURCE,
        "module_code": MODULE_CODE,
        "description": "Delete company",
    },
]

