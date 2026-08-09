import uuid

from django.contrib.postgres.indexes import GinIndex
from django.db import models


class AssetType(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, db_index=True)

    code = models.CharField(max_length=100, unique=True)
    label = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)
    is_system = models.BooleanField(default=False)

    class Meta:
        db_table = "asset_types"
        ordering = ["label"]

    def __str__(self):
        return self.label


class Tag(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, db_index=True)

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "asset_tags"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Asset(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        PENDING = "pending", "Pending setup"
        ARCHIVED = "archived", "Archived"

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, db_index=True)

    asset_type = models.ForeignKey(AssetType, on_delete=models.PROTECT, related_name="assets")
    owner = models.ForeignKey(
        "users.CompanyUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="owned_assets",
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="assets")

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, blank=True)
    url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

    launched_at = models.DateField(null=True, blank=True)
    archived_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "assets"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["asset_type", "status"], name="asset_type_status_idx"),
            models.Index(fields=["owner", "status"], name="asset_owner_status_idx"),
            GinIndex(fields=["name"], name="asset_name_trgm_idx", opclasses=["gin_trgm_ops"]),
        ]

    def __str__(self):
        return self.name