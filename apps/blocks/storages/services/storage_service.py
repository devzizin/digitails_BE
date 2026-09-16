from typing import BinaryIO

from apps.blocks.storages.adapters.factory import StorageAdapterFactory
from apps.blocks.storages.constants import DEFAULT_DOWNLOAD_URL_EXPIRES
from apps.blocks.storages.models import StorageConnection


class StorageService:
    """
    Thin wrapper around the storage adapter (obtained via the factory).

    Domain services (FileService) call this instead of touching
    StorageAdapterFactory/adapters directly -- keeps "which provider,
    which adapter instance" as an internal detail of this one class.
    """

    @staticmethod
    def upload(*, connection: StorageConnection, file: BinaryIO, key: str, mime_type: str) -> None:
        adapter = StorageAdapterFactory.get(connection)
        adapter.upload(file=file, key=key, mime_type=mime_type)

    @staticmethod
    def generate_download_url(
        *,
        connection: StorageConnection,
        key: str,
        expires: int = DEFAULT_DOWNLOAD_URL_EXPIRES,
    ) -> str:
        adapter = StorageAdapterFactory.get(connection)
        return adapter.generate_download_url(key=key, expires=expires)

    @staticmethod
    def delete(*, connection: StorageConnection, key: str) -> None:
        adapter = StorageAdapterFactory.get(connection)
        adapter.delete(key=key)

    @staticmethod
    def copy(*, connection: StorageConnection, source_key: str, destination_key: str) -> None:
        adapter = StorageAdapterFactory.get(connection)
        adapter.copy(source_key=source_key, destination_key=destination_key)

    @staticmethod
    def exists(*, connection: StorageConnection, key: str) -> bool:
        adapter = StorageAdapterFactory.get(connection)
        return adapter.exists(key=key)
