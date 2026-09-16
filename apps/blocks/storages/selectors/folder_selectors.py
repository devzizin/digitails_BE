from uuid import UUID

from apps.blocks.storages.exceptions import StorageFolderNotFound
from apps.blocks.storages.models import StorageFolder


def get_folder_by_uuid(folder_uuid: UUID) -> StorageFolder:
    folder = StorageFolder.objects.filter(
        uuid=folder_uuid,
        deleted_at__isnull=True,
    ).first()

    if not folder:
        raise StorageFolderNotFound()

    return folder


def get_deleted_folder_by_uuid(folder_uuid: UUID) -> StorageFolder:
    folder = StorageFolder.objects.filter(
        uuid=folder_uuid,
        deleted_at__isnull=False,
    ).first()

    if not folder:
        raise StorageFolderNotFound()

    return folder


def get_folders_for_entity(entity_id, parent_id=None):
    return StorageFolder.objects.filter(
        entity_id=entity_id,
        parent_id=parent_id,
        deleted_at__isnull=True,
    )
