from enum import Enum

from django.db import models


class DriveFileHealthStatus(str, Enum):
    OK = "ok"
    MISSING_IN_STORAGE = "missing_in_storage"
    SOFT_DELETED = "soft_deleted"
    NOT_FOUND = "not_found"
    ORPHAN = "orphan"


class StorageProvider(models.TextChoices):
    S3 = "s3", "S3"
    MINIO = "minio", "MinIO"
    ONEDRIVE = "onedrive", "OneDrive"
    GDRIVE = "gdrive", "Google Drive"
    DROPBOX = "dropbox", "Dropbox"


class DriveActivityAction(models.TextChoices):
    FILE_UPLOADED = "file_uploaded", "File uploaded"
    FILE_DELETED = "file_deleted", "File deleted"
    FILE_RESTORED = "file_restored", "File restored"
    FILE_MOVED = "file_moved", "File moved"
    FILE_COPIED = "file_copied", "File copied"
    FOLDER_CREATED = "folder_created", "Folder created"
    FOLDER_RENAMED = "folder_renamed", "Folder renamed"
    FOLDER_MOVED = "folder_moved", "Folder moved"
    FOLDER_DELETED = "folder_deleted", "Folder deleted"
    FOLDER_RESTORED = "folder_restored", "Folder restored"
    FOLDER_STARRED = "folder_starred", "Folder starred"
    FOLDER_UNSTARRED = "folder_unstarred", "Folder unstarred"
    FILE_STARRED = "file_starred", "File starred"
    FILE_UNSTARRED = "file_unstarred", "File unstarred"
    FOLDER_BOUND = "folder_bound", "Folder bound"
    FOLDER_UNBOUND = "folder_unbound", "Folder unbound"


class DriveActivityTargetKind(models.TextChoices):
    FOLDER = "folder", "Folder"
    FILE = "file", "File"
