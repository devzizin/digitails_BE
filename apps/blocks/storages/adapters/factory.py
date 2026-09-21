from apps.blocks.storages.enums import StorageProvider
from apps.blocks.storages.services.connection_resolver import StorageConnectionResolver
from apps.blocks.storages.adapters.s3 import S3Adapter

ADAPTERS = {
    StorageProvider.S3: S3Adapter,
    StorageProvider.MINIO: S3Adapter,
}


# class StorageAdapterFactory:

#     @staticmethod
#     def get(connection):
#         if connection.provider == StorageProvider.ONEDRIVE:
#             connection = StorageConnectionResolver.resolve(connection)

#         provider = connection.provider

#         try:
#             adapter_cls = ADAPTERS[provider]
#             return adapter_cls(connection=connection)

#         except KeyError:
#             raise ValueError(f"No adapter for provider: {provider}")





class StorageAdapterFactory:
    @staticmethod
    def get(connection: StorageConnection) -> S3Adapter:
        return S3Adapter(connection=connection)
