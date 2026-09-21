from django.db import transaction

from apps.blocks.storages.models import StorageConnection


class ConnectionService:
    @staticmethod
    @transaction.atomic
    def create_connection(
        *,
        name: str,
        endpoint_url: str,
        bucket: str,
        region: str,
        access_key: str,
        secret_key: str,
        is_default: bool = False,
        created_by=None,
    ) -> StorageConnection:
        if is_default:
            # Clear any existing default first -- avoids relying on the
            # DB constraint alone to enforce single-default-per-tenant
            # (the constraint still exists as a backstop).
            StorageConnection.objects.filter(
                is_default=True,
                deleted_at__isnull=True,
            ).update(is_default=False)

        connection = StorageConnection(
            name=name,
            endpoint_url=endpoint_url,
            bucket=bucket,
            region=region,
            access_key=access_key,
            secret_key=secret_key,
            is_default=is_default,
            created_by=created_by,
        )
        connection.full_clean()
        connection.save()
        return connection

    @staticmethod
    @transaction.atomic
    def set_default(*, connection: StorageConnection) -> StorageConnection:
        StorageConnection.objects.filter(
            is_default=True,
            deleted_at__isnull=True,
        ).exclude(pk=connection.pk).update(is_default=False)

        connection.is_default = True
        connection.save(update_fields=["is_default", "updated_at"])
        return connection
