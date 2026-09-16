from uuid import UUID

from apps.blocks.storages.exceptions import StorageConnectionNotFound
from apps.blocks.storages.models import StorageConnection


def get_active_connection_by_uuid(connection_uuid: UUID) -> StorageConnection:
    connection = StorageConnection.objects.filter(
        uuid=connection_uuid,
        is_active=True,
        deleted_at__isnull=True,
    ).first()

    if not connection:
        raise StorageConnectionNotFound()

    return connection


def get_default_connection() -> StorageConnection | None:
    return StorageConnection.objects.filter(
        is_default=True,
        is_active=True,
        deleted_at__isnull=True,
    ).first()
