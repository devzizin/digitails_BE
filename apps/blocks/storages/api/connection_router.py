"""
ASSUMPTIONS to adjust before this runs:
- `TokenAuth` -- swap for whatever ninja auth class Svitup actually uses
  (something built on the AuthToken model, per earlier notes).
- `permission_required` -- swap import path/signature for the real
  decorator once it exists in apps/core/permissions.
- `default_paginate` -- swap for Svitup's pagination helper (or drop and
  use ninja's built-in `paginate` if there isn't a custom one yet).
"""

from uuid import UUID

from ninja import Router

from apps.blocks.storages.permissions import (
    STORAGE_CONNECTION_CREATE,
    STORAGE_CONNECTION_LIST,
)
from apps.blocks.storages.api.schemas import (
    ErrorSchema,
    StorageConnectionIn,
    StorageConnectionOut,
)
from apps.blocks.storages.models import StorageConnection
from apps.blocks.storages.selectors.connection_selectors import (
    get_active_connection_by_uuid,
    get_default_connection,
)
from apps.blocks.storages.services.connection_service import ConnectionService
from apps.core.permissions.decorators import permission_required
from apps.core.users.auth import TokenAuth


router = Router(tags=["Storage Connections"], auth=TokenAuth())


@router.post(
    "",
    response={201: StorageConnectionOut},
    summary="Create S3 connection",
)
# @permission_required(STORAGE_CONNECTION_CREATE)
def create_connection(request, payload: StorageConnectionIn):
    connection = ConnectionService.create_connection(
        name=payload.name,
        endpoint_url=payload.endpoint_url,
        bucket=payload.bucket,
        region=payload.region,
        access_key=payload.access_key,
        secret_key=payload.secret_key,
        is_default=payload.is_default,
        created_by=request.user,
    )
    return 201, connection


@router.get(
    "",
    response={200: list[StorageConnectionOut]},
    summary="List storage connections",
)
# @permission_required(STORAGE_CONNECTION_LIST)
def list_connections(request):
    return StorageConnection.objects.filter(
        is_active=True,
        deleted_at__isnull=True,
    )


@router.get(
    "/default",
    response={200: StorageConnectionOut, 404: ErrorSchema},
    summary="Get default storage connection",
)
# @permission_required(STORAGE_CONNECTION_LIST)
def get_default_connection_view(request):
    connection = get_default_connection()
    if not connection:
        return 404, {"detail": "Default connection not found."}
    return 200, connection


@router.patch(
    "/{connection_uuid}/default",
    response={200: StorageConnectionOut, 404: ErrorSchema},
    summary="Set default storage connection",
)
# @permission_required(STORAGE_CONNECTION_CREATE)
def set_default_connection(request, connection_uuid: UUID):
    connection = get_active_connection_by_uuid(connection_uuid)
    connection = ConnectionService.set_default(connection=connection)
    return 200, connection
