from apps.blocks.storages.exceptions import StorageInvalidStorageKey


def validate_storage_key(key: str) -> str:
    if not key or not key.strip():
        raise StorageInvalidStorageKey()

    normalized = key.replace("\\", "/").strip()

    if "\x00" in normalized:
        raise StorageInvalidStorageKey()

    if normalized.startswith("/") or ".." in normalized.split("/"):
        raise StorageInvalidStorageKey()

    return normalized
