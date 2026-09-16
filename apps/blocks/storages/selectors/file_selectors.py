from uuid import UUID

from apps.blocks.storages.exceptions import StorageFileNotFound
from apps.blocks.storages.models import StorageFile


def get_file_by_uuid(file_uuid: UUID) -> StorageFile | None:
    """Returns None (not raising) -- used by restore flows that need to
    look up files regardless of soft-delete state."""
    return StorageFile.objects.filter(uuid=file_uuid).first()


def get_live_file_by_uuid(file_uuid: UUID) -> StorageFile:
    file = StorageFile.objects.filter(
        uuid=file_uuid,
        deleted_at__isnull=True,
    ).first()

    if not file:
        raise StorageFileNotFound()

    return file


def get_files_for_folder(folder_id, entity_id):
    return StorageFile.objects.filter(
        folder_id=folder_id,
        entity_id=entity_id,
        deleted_at__isnull=True,
    )


def get_files_for_entity(entity_id):
    return StorageFile.objects.filter(
        entity_id=entity_id,
        deleted_at__isnull=True,
    )
