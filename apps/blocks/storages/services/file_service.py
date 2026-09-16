import uuid as uuid_lib

from django.db import transaction
from django.utils import timezone

from apps.blocks.storages.exceptions import StorageFolderEntityMismatch
from apps.blocks.storages.models import StorageFile, StorageFolder
from apps.blocks.storages.security.file_checksum import compute_stream_sha256
from apps.blocks.storages.security.mime_sniffer import (
    read_upload_head,
    validate_upload_content,
)
from apps.blocks.storages.security.upload_validation import validate_storage_filename
from apps.blocks.storages.services.connection_resolver import StorageConnectionResolver
from apps.blocks.storages.services.storage_service import StorageService


def _build_storage_key(*, entity, filename: str) -> str:
    # uuid4-prefixed key -- avoids same-name collisions across uploads
    # without needing a DB lookup first. Original (human) name is kept
    # separately in StorageFile.original_name.
    return f"entities/{entity.uuid}/{uuid_lib.uuid4().hex}_{filename}"


class FileService:
    @staticmethod
    @transaction.atomic
    def upload_file(
        *,
        file,
        entity,
        folder: StorageFolder | None = None,
        created_by=None,
    ) -> StorageFile:
        if folder and folder.entity_id != entity.id:
            raise StorageFolderEntityMismatch()

        filename = validate_storage_filename(file.name)

        head = read_upload_head(file)
        declared_mime = getattr(file, "content_type", "") or "application/octet-stream"
        mime_type = validate_upload_content(head=head, declared_mime=declared_mime)

        checksum = compute_stream_sha256(file)

        connection = StorageConnectionResolver.resolve()
        key = _build_storage_key(entity=entity, filename=filename)

        StorageService.upload(connection=connection, file=file, key=key, mime_type=mime_type)

        storage_file = StorageFile(
            connection=connection,
            entity=entity,
            folder=folder,
            original_name=filename,
            mime_type=mime_type,
            size=getattr(file, "size", 0),
            checksum=checksum,
            storage_key=key,
            created_by=created_by,
        )
        # full_clean() enforces StorageFile.clean() (folder/entity match) --
        # required here for the same reason noted in FolderService.
        storage_file.full_clean()
        storage_file.save()
        return storage_file

    @staticmethod
    def generate_download_url(file: StorageFile) -> str:
        return StorageService.generate_download_url(
            connection=file.connection,
            key=file.storage_key,
        )

    @staticmethod
    @transaction.atomic
    def rename_file(*, file: StorageFile, name: str) -> StorageFile:
        file.original_name = validate_storage_filename(name)
        file.full_clean()
        file.save(update_fields=["original_name", "updated_at"])
        return file

    @staticmethod
    @transaction.atomic
    def move_file(*, file: StorageFile, new_folder: StorageFolder | None) -> StorageFile:
        if new_folder and new_folder.entity_id != file.entity_id:
            raise StorageFolderEntityMismatch()
        file.folder = new_folder
        file.full_clean()
        file.save(update_fields=["folder", "updated_at"])
        return file

    @staticmethod
    @transaction.atomic
    def delete_file(*, file: StorageFile) -> None:
        # Soft delete only -- bytes stay in S3. Add a cleanup job later
        # if you want hard-deleted files actually purged from the bucket.
        file.deleted_at = timezone.now()
        file.save(update_fields=["deleted_at", "updated_at"])

    @staticmethod
    @transaction.atomic
    def restore_file(*, file: StorageFile) -> StorageFile:
        file.deleted_at = None
        file.save(update_fields=["deleted_at", "updated_at"])
        return file
