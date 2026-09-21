from datetime import datetime
from uuid import UUID

from ninja import Schema


class ErrorSchema(Schema):
    detail: str


class MessageOut(Schema):
    detail: str


# --- Connections ---


class StorageConnectionIn(Schema):
    name: str
    endpoint_url: str = ""
    bucket: str
    region: str = ""
    access_key: str
    secret_key: str
    is_default: bool = False


class StorageConnectionOut(Schema):
    """access_key/secret_key are intentionally excluded -- never echo
    secrets back in an API response."""

    uuid: UUID
    name: str
    endpoint_url: str
    bucket: str
    region: str
    is_active: bool
    is_default: bool
    created_at: datetime


# --- Folders ---


class FolderCreateIn(Schema):
    entity_id: UUID
    name: str
    parent_uuid: UUID | None = None


class FolderRenameIn(Schema):
    name: str


class FolderMoveIn(Schema):
    parent_uuid: UUID | None = None


class StorageFolderOut(Schema):
    uuid: UUID
    name: str
    parent_uuid: UUID | None = None
    entity_id: UUID
    order: int
    created_at: datetime

    @staticmethod
    def resolve_parent_uuid(obj):
        return obj.parent.uuid if obj.parent_id else None


# --- Files ---


class FileRenameIn(Schema):
    name: str


class FileMoveIn(Schema):
    folder_uuid: UUID | None = None


class DownloadUrlOut(Schema):
    url: str


class StorageFileOut(Schema):
    uuid: UUID
    original_name: str
    mime_type: str
    size: int
    folder_uuid: UUID | None = None
    entity_id: UUID
    created_at: datetime

    @staticmethod
    def resolve_folder_uuid(obj):
        return obj.folder.uuid if obj.folder_id else None
