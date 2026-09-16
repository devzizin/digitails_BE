from django.db import transaction
from django.utils import timezone

from apps.blocks.storages.models import StorageFolder


class FolderService:
    @staticmethod
    @transaction.atomic
    def create_folder(*, name: str, entity, parent: StorageFolder | None = None, created_by=None) -> StorageFolder:
        folder = StorageFolder(
            name=name,
            entity=entity,
            parent=parent,
            created_by=created_by,
        )
        # full_clean() is required here -- StorageFolder.clean() is not
        # called automatically by .save(). Skipping this call means the
        # self-parent check silently stops being enforced.
        folder.full_clean()
        folder.save()
        return folder

    @staticmethod
    @transaction.atomic
    def rename_folder(*, folder: StorageFolder, name: str) -> StorageFolder:
        folder.name = name
        folder.full_clean()
        folder.save(update_fields=["name", "updated_at"])
        return folder

    @staticmethod
    @transaction.atomic
    def move_folder(*, folder: StorageFolder, new_parent: StorageFolder | None) -> StorageFolder:
        folder.parent = new_parent
        folder.full_clean()
        folder.save(update_fields=["parent", "updated_at"])
        return folder

    @staticmethod
    @transaction.atomic
    def delete_folder(*, folder: StorageFolder) -> None:
        folder.deleted_at = timezone.now()
        folder.save(update_fields=["deleted_at", "updated_at"])

    @staticmethod
    @transaction.atomic
    def restore_folder(*, folder: StorageFolder) -> StorageFolder:
        folder.deleted_at = None
        folder.save(update_fields=["deleted_at", "updated_at"])
        return folder
