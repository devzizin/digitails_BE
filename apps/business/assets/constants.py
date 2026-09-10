'''
core permission architecture constants.

IMPORTANT:
These constants are stable architecture identifiers.
'''

# =====================================================
# MODULE
# =====================================================

MODULE_CODE = "assets"

#======================================================
# NAMESPACE
# =====================================================

BUSINESS_NAMESPACE = "bussiness"

#======================================================
# RESOURCE
# =====================================================

ASSET_RESOURCE = "asset"

ASSET_TYPE_RESOURCE = "asset_type"

#=====================================================
# ENTITY TYPE
# =====================================================

ASSET_ENTITY_TYPE_CODE = f"{BUSINESS_NAMESPACE}.{ASSET_RESOURCE}"

ASSET_TYPE_ENTITY_TYPE_CODE = f"{BUSINESS_NAMESPACE}.{ASSET_TYPE_RESOURCE}"

#=====================================================
# DISPLAY
# =====================================================

ASSET_LABEL = "Assets"

ASSET_DESCRIPTION = "Provides asset management " "and asset lifecycle operations."

ASSET_TYPE_LABEL = "Asset Types"

ASSET_TYPE_DESCRIPTION = (
    "Provides reusable asset templates " "and module configuration."
)