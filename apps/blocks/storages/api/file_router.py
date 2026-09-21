from uuid import UUID

from ninja import File, Form, Router
from ninja.files import UploadedFile

from apps.blocks.storages.permissions import (
    STORAGE_FILE_CREATE,
    STORAGE_FILE_DELETE,
    STORAGE_FILE_LIST,
    STORAGE_FILE_READ,
    STORAGE_FILE_UPDATE,
)
from apps.blocks.storages.api.schemas import (
    DownloadUrlOut,
    ErrorSchema,
    FileMoveIn,
    FileRenameIn,
    StorageFileOut,
)
from apps.blocks.storages.exceptions import StorageFolderEntityMismatch
from apps.blocks.storages.selectors.file_selectors import (
    get_file_by_uuid,
    get_files_for_entity,
    get_files_for_folder,
    get_live_file_by_uuid,
)
from apps.blocks.storages.selectors.folder_selectors import get_folder_by_uuid
from apps.blocks.storages.services.file_service import FileService
from apps.core.entities.selectors.entity_selector import get_entity_by_id
from apps.core.permissions.decorators import permission_required
from apps.core.users.auth import TokenAuth


router = Router(tags=["Storage Files"], auth=TokenAuth())


@router.post(
    "/upload",
    response={201: StorageFileOut, 404: ErrorSchema, 422: ErrorSchema},
    summary="Upload file",
)
def upload_file(
    request,
    file: UploadedFile = File(...),
    entity_id: UUID = Form(...),
    folder_uuid: UUID | None = Form(None),
):
    entity = get_entity_by_id(entity_id)

    folder = None
    if folder_uuid:
        folder = get_folder_by_uuid(folder_uuid)

    storage_file = FileService.upload_file(
        file=file,
        entity=entity,
        folder=folder,
        created_by=request.user,
    )
    return 201, storage_file


@router.get(
    "/{file_uuid}",
    response={200: StorageFileOut, 404: ErrorSchema},
    summary="Get file metadata",
)
def get_file(request, file_uuid: UUID):
    return 200, get_live_file_by_uuid(file_uuid)


@router.get(
    "",
    response={200: list[StorageFileOut]},
    summary="List files",
)
def list_files(request, entity_id: UUID, folder_uuid: UUID | None = None):
    if folder_uuid is not None:
        folder = get_folder_by_uuid(folder_uuid)

        if folder.entity_id != entity_id:
            raise StorageFolderEntityMismatch()

        return get_files_for_folder(folder.id, entity_id)

    return get_files_for_entity(entity_id)


@router.get(
    "/{file_uuid}/download",
    response={200: DownloadUrlOut, 404: ErrorSchema},
    summary="Get download URL",
)
def get_download_url(request, file_uuid: UUID):
    file = get_live_file_by_uuid(file_uuid)
    url = FileService.generate_download_url(file)
    return 200, {"url": url}


@router.patch(
    "/{file_uuid}",
    response={200: StorageFileOut, 404: ErrorSchema, 422: ErrorSchema},
    summary="Rename file",
)
def rename_file(request, file_uuid: UUID, payload: FileRenameIn):
    file = get_live_file_by_uuid(file_uuid)
    file = FileService.rename_file(file=file, name=payload.name)
    return 200, file


@router.post(
    "/{file_uuid}/move",
    response={200: StorageFileOut, 404: ErrorSchema, 422: ErrorSchema},
    summary="Move file",
)
def move_file(request, file_uuid: UUID, payload: FileMoveIn):
    file = get_live_file_by_uuid(file_uuid)

    new_folder = None
    if payload.folder_uuid:
        new_folder = get_folder_by_uuid(payload.folder_uuid)

    file = FileService.move_file(file=file, new_folder=new_folder)
    return 200, file


@router.delete(
    "/{file_uuid}",
    response={204: None, 404: ErrorSchema},
    summary="Soft delete file",
)
def delete_file(request, file_uuid: UUID):
    file = get_live_file_by_uuid(file_uuid)
    FileService.delete_file(file=file)
    return 204, None


@router.post(
    "/{file_uuid}/restore",
    response={200: StorageFileOut, 404: ErrorSchema},
    summary="Restore file",
)
def restore_file(request, file_uuid: UUID):
    file = get_file_by_uuid(file_uuid)

    if not file:
        return 404, {"detail": "File not found."}

    file = FileService.restore_file(file=file)
    return 200, file
