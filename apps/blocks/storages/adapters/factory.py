from apps.blocks.storages.enums import StorageProvider
from apps.blocks.storages.services.connection_service import DriveConnectionService
from apps.blocks.storages.storage.onedrive import OneDriveAdapter
from apps.blocks.storages.storage.s3 import S3Adapter

ADAPTERS = {
    StorageProvider.S3: S3Adapter,
    StorageProvider.MINIO: S3Adapter,
    StorageProvider.ONEDRIVE: OneDriveAdapter,
}


class StorageAdapterFactory:

    @staticmethod
    def get(connection):
        if connection.provider == StorageProvider.ONEDRIVE:
            connection = DriveConnectionService.ensure_onedrive_access_token(connection)

        provider = connection.provider

        try:
            adapter_cls = ADAPTERS[provider]
            return adapter_cls(connection=connection)

        except KeyError:
            raise ValueError(f"No adapter for provider: {provider}")
