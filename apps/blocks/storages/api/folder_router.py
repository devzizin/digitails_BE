from uuid import UUID

from ninja import Router

from apps.blocks.storages.permissions import (
    STORAGE_FOLDER_CREATE,
    STORAGE_FOLDER_DELETE,
    STORAGE_FOLDER_LIST,
    STORAGE_FOLDER_UPDATE,
)
from apps.blocks.storages.api.schemas import (
    ErrorSchema,
    FolderCreateIn,
    FolderMoveIn,
    FolderRenameIn,
    StorageFolderOut,
)
from apps.blocks.storages.selectors.folder_selectors import (
    get_deleted_folder_by_uuid,
    get_folder_by_uuid,
    get_folders_for_entity,
)
from apps.blocks.storages.services.folder_service import FolderService
from apps.core.entities.selectors import get_live_entity_by_id
from apps.core.permissions.decorators import permission_required
from apps.core.users.auth import TokenAuth


router = Router(tags=["Storage Folders"], auth=TokenAuth())


@router.post(
    "",
    response={201: StorageFolderOut, 404: ErrorSchema, 422: ErrorSchema},
    summary="Create folder",
)
def create_folder(request, payload: FolderCreateIn):
    entity = get_live_entity_by_id(payload.entity_id)

    parent = None
    if payload.parent_uuid:
        parent = get_folder_by_uuid(payload.parent_uuid)

    folder = FolderService.create_folder(
        name=payload.name,
        entity=entity,
        parent=parent,
        created_by=request.user,
    )
    return 201, folder


@router.get(
    "",
    response={200: list[StorageFolderOut]},
    summary="List folders for an entity",
)
def list_folders(request, entity_id: UUID, parent_uuid: UUID | None = None):
    parent_id = get_folder_by_uuid(parent_uuid).id if parent_uuid else None
    return get_folders_for_entity(entity_id, parent_id=parent_id)


@router.patch(
    "/{folder_uuid}",
    response={200: StorageFolderOut, 404: ErrorSchema, 422: ErrorSchema},
    summary="Rename folder",
)
def rename_folder(request, folder_uuid: UUID, payload: FolderRenameIn):
    folder = get_folder_by_uuid(folder_uuid)
    folder = FolderService.rename_folder(folder=folder, name=payload.name)
    return 200, folder


@router.post(
    "/{folder_uuid}/move",
    response={200: StorageFolderOut, 404: ErrorSchema, 422: ErrorSchema},
    summary="Move folder",
)
def move_folder(request, folder_uuid: UUID, payload: FolderMoveIn):
    folder = get_folder_by_uuid(folder_uuid)

    new_parent = None
    if payload.parent_uuid:
        new_parent = get_folder_by_uuid(payload.parent_uuid)

    folder = FolderService.move_folder(folder=folder, new_parent=new_parent)
    return 200, folder


@router.delete(
    "/{folder_uuid}",
    response={204: None, 404: ErrorSchema},
    summary="Delete folder",
)
def delete_folder(request, folder_uuid: UUID):
    folder = get_folder_by_uuid(folder_uuid)
    FolderService.delete_folder(folder=folder)
    return 204, None


@router.post(
    "/{folder_uuid}/restore",
    response={200: StorageFolderOut, 404: ErrorSchema},
    summary="Restore deleted folder",
)
def restore_folder(request, folder_uuid: UUID):
    folder = get_deleted_folder_by_uuid(folder_uuid)
    folder = FolderService.restore_folder(folder=folder)
    return 200, folder
