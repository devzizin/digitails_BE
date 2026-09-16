import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class StorageConnection(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    name = models.CharField(max_length=255)

    endpoint_url = models.CharField(max_length=512, blank=True)
    bucket = models.CharField(max_length=255)
    region = models.CharField(max_length=100, blank=True)

    access_key = models.CharField(max_length=255)  # TODO: encrypted field
    secret_key = models.CharField(max_length=255)  # TODO: encrypted field

    is_active = models.BooleanField(default=True, db_index=True)
    is_default = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    class Meta:
        db_table = "storage_connections"

        constraints = [
            models.UniqueConstraint(
                fields=[],
                condition=Q(is_default=True, deleted_at__isnull=True),
                name="unique_default_storage_connection",
            ),
        ]

    def __str__(self):
        return self.name


class StorageFolder(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    name = models.CharField(max_length=255)

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
    )

    entity = models.ForeignKey(
        "entities.Entity",
        on_delete=models.CASCADE,
        related_name="storage_folders",
    )

    order = models.PositiveIntegerField(default=0)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    class Meta:
        db_table = "storage_folders"

        indexes = [
            models.Index(fields=["entity", "parent"]),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["entity", "parent", "name"],
                condition=Q(deleted_at__isnull=True),
                name="unique_folder_name_per_parent",
            ),
        ]

        ordering = ["order", "created_at"]

    def clean(self):
        if self.parent_id and self.parent_id == self.id:
            raise ValidationError("Folder cannot be parent of itself")

    def __str__(self):
        return self.name


class StorageFile(models.Model):
    """
    File metadata only -- actual bytes live in S3, referenced by
    `storage_key` on `connection`.
    """

    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    connection = models.ForeignKey(
        StorageConnection,
        on_delete=models.PROTECT,
        related_name="files",
    )

    entity = models.ForeignKey(
        "entities.Entity",
        on_delete=models.CASCADE,
        related_name="storage_files",
    )

    folder = models.ForeignKey(
        StorageFolder,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="files",
    )

    original_name = models.CharField(max_length=512)
    mime_type = models.CharField(max_length=255)
    size = models.BigIntegerField()
    checksum = models.CharField(max_length=128, null=True, blank=True)

    storage_key = models.CharField(max_length=1024, db_index=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    class Meta:
        db_table = "storage_files"

        indexes = [
            models.Index(fields=["entity", "folder"]),
            models.Index(fields=["connection"]),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["connection", "storage_key"],
                name="unique_storage_key_per_connection",
            ),
        ]

        ordering = ["-created_at"]

    def clean(self):
        if self.folder_id and self.folder.entity_id != self.entity_id:
            raise ValidationError("Folder must belong to the same entity as the file")

    def __str__(self):
        return self.original_name