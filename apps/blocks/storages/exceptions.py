"""
ASSUMPTION: HttpError-based exception hierarchy, mirroring AlpiVolt's
convention. Adjust the base class if Svitup uses a different pattern.
"""

from ninja.errors import HttpError


class StorageError(HttpError):
    status_code = 400
    message = "Storage error."

    def __init__(self):
        super().__init__(self.status_code, self.message)


class StorageConnectionRequired(StorageError):
    status_code = 422
    message = "No storage connection configured for this tenant."


class StorageConnectionNotFound(StorageError):
    status_code = 404
    message = "Storage connection not found."


class StorageConnectionUnavailable(StorageError):
    status_code = 503
    message = "Storage connection is currently unavailable."


class StorageFolderNotFound(StorageError):
    status_code = 404
    message = "Folder not found."


class StorageFileNotFound(StorageError):
    status_code = 404
    message = "File not found."


class StorageInvalidFile(StorageError):
    status_code = 422
    message = "Invalid file."


class StorageInvalidStorageKey(StorageError):
    status_code = 422
    message = "Invalid storage key."


class StorageFileTypeNotAllowed(StorageError):
    status_code = 422
    message = "File type not allowed."


class StorageFolderEntityMismatch(StorageError):
    status_code = 422
    message = "Folder does not belong to the same entity as the file."
