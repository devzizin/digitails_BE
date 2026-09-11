# =====================================================
# MODULE
# =====================================================

MODULE_CODE = "storage"

# =====================================================
# NAMESPACE
# =====================================================

BLOCKS_NAMESPACE = "blocks"

# =====================================================
# RESOURCES
# =====================================================

STORAGE_RESOURCE = "storages"
CONNECTION_RESOURCE = "connection"

# Stable Search source/navigation identifiers. Storage files and folders are
# child resources scoped by an Entity; they are not Entity types themselves.
STORAGE_FILE_SEARCH_SOURCE_TYPE = "blocks.storage_file"
STORAGE_FOLDER_SEARCH_SOURCE_TYPE = "blocks.storage_folder"

# =====================================================
# DISPLAY
# =====================================================

STORAGE_LABEL = "Storage"

STORAGE_DESCRIPTION = (
    "Permission-scoped file storage for platform entities."
)

# =====================================================
# MODULE FOLDERS
# =====================================================

ASSETS_NODE_NAME = "Assets"

SYNC_METADATA_KEY = "sync"

SYNC_DIRECTION_PULL = "pull"
SYNC_DIRECTION_PUSH = "push"
SYNC_DIRECTION_BIDIRECTIONAL = "bidirectional"

SYNC_DIRECTIONS = frozenset(
    {
        SYNC_DIRECTION_PULL,
        SYNC_DIRECTION_PUSH,
        SYNC_DIRECTION_BIDIRECTIONAL,
    },
)

STORAGE_MODULE_CODE = "storage"

# Max upload size (bytes). Override via STORAGE_MAX_UPLOAD_BYTES env / settings.
STORAGE_MAX_UPLOAD_BYTES = 100 * 1024 * 1024  # 100 MiB

# Presigned download URL lifetime (seconds).
STORAGE_DOWNLOAD_URL_EXPIRES_SECONDS = 3600

STORAGE_BLOCKED_EXTENSIONS = frozenset(
    {
        ".exe",
        ".bat",
        ".cmd",
        ".com",
        ".msi",
        ".scr",
        ".pif",
        ".sh",
        ".bash",
        ".ps1",
        ".vbs",
        ".js",
        ".jar",
        ".php",
        ".phtml",
        ".htaccess",
        ".dll",
        ".dmg",
        ".app",
    },
)

STORAGE_BLOCKED_MIME_PREFIXES = (
    "application/x-msdownload",
    "application/x-msdos-program",
    "application/x-executable",
    "application/javascript",
    "application/x-php",
    "text/javascript",
    "text/x-php",
)