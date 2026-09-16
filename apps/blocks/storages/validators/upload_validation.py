from pathlib import PurePath

from apps.blocks.storages.constants import (
    STORAGE_BLOCKED_EXTENSIONS,
    STORAGE_BLOCKED_MIME_PREFIXES,
)
from apps.blocks.storages.exceptions import StorageFileTypeNotAllowed, StorageInvalidFile


def normalize_upload_filename(filename: str) -> str:
    if not filename or not filename.strip():
        raise StorageInvalidFile()

    normalized = filename.replace("\\", "/").strip()

    if "\x00" in normalized:
        raise StorageInvalidFile()

    if "/" in normalized or ".." in normalized:
        raise StorageInvalidFile()

    if not normalized or normalized in {".", ".."}:
        raise StorageInvalidFile()

    return normalized


def validate_storage_filename(filename: str) -> str:
    name = normalize_upload_filename(filename)
    extension = PurePath(name).suffix.lower()

    if extension in STORAGE_BLOCKED_EXTENSIONS:
        raise StorageFileTypeNotAllowed()

    return name


def validate_upload_mime_type(*, mime_type: str) -> None:
    mime_lower = (mime_type or "").lower()

    for blocked_prefix in STORAGE_BLOCKED_MIME_PREFIXES:
        if mime_lower == blocked_prefix or mime_lower.startswith(blocked_prefix):
            raise StorageFileTypeNotAllowed()
