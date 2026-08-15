from __future__ import annotations

from datetime import date, datetime
from typing import Annotated, Optional
from uuid import UUID

from ninja import FilterLookup, FilterSchema, Schema
from pydantic import ConfigDict, Field


class AssetTypeOut(Schema):
    model_config = ConfigDict(from_attributes=True)

    uuid: UUID
    code: str
    label: str
    description: str
    icon: str
    is_system: bool


class TagOut(Schema):
    model_config = ConfigDict(from_attributes=True)

    uuid: UUID
    name: str


class AssetOut(Schema):
    model_config = ConfigDict(from_attributes=True)

    uuid: UUID
    asset_type: AssetTypeOut
    name: str
    code: str
    url: str
    description: str
    status: str
    launched_at: Optional[date] = None
    archived_at: Optional[datetime] = None
    tags: list[TagOut]
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def resolve_tags(obj):
        return obj.tags.all()


class CreateAssetSchema(Schema):
    asset_type_uuid: UUID
    name: str
    code: str | None = None
    url: str | None = None
    description: str | None = None
    status: str | None = None
    launched_at: date | None = None
    tag_uuids: list[UUID] | None = None


class UpdateAssetSchema(Schema):
    asset_type_uuid: UUID | None = None
    name: str | None = None
    code: str | None = None
    url: str | None = None
    description: str | None = None
    status: str | None = None
    launched_at: date | None = None
    tag_uuids: list[UUID] | None = None


class AssetFilterSchema(FilterSchema):
    name: Annotated[
        str | None,
        FilterLookup("name__icontains"),
    ] = Field(default=None, description="Search assets by name.")

    status: Annotated[
        str | None,
        FilterLookup("status"),
    ] = Field(default=None, description="Filter by status.")

    asset_type: Annotated[
        UUID | None,
        FilterLookup("asset_type__uuid"),
    ] = Field(default=None, description="Filter by asset type uuid.")


class ErrorSchema(Schema):
    detail: str