from django.db import transaction
from django.utils import timezone

from apps.core.assets.exceptions import AssetCodeAlreadyExists
from apps.core.assets.models import Asset
from apps.core.assets.selectors.asset_selector import AssetSelector


class AssetService:

    @staticmethod
    @transaction.atomic
    def create_asset(
        *,
        asset_type_uuid,
        name: str,
        code: str = "",
        url: str = "",
        description: str = "",
        status: str = Asset.Status.ACTIVE,
        launched_at=None,
        owner=None,
        tag_uuids: list | None = None,
    ) -> Asset:
        asset_type = AssetSelector.get_asset_type_by_uuid(asset_type_uuid)

        if code and Asset.objects.filter(code=code).exists():
            raise AssetCodeAlreadyExists()

        asset = Asset.objects.create(
            asset_type=asset_type,
            owner=owner,
            name=name,
            code=code,
            url=url,
            description=description,
            status=status,
            launched_at=launched_at,
        )

        if tag_uuids:
            tags = AssetSelector.get_tags_by_uuids(tag_uuids)
            asset.tags.set(tags)

        return asset

    @staticmethod
    @transaction.atomic
    def update_asset(asset: Asset, **data) -> Asset:
        allowed_fields = {
            "name",
            "code",
            "url",
            "description",
            "status",
            "launched_at",
        }

        updated_fields = []

        for field, value in data.items():
            if field not in allowed_fields:
                continue
            if value is None:
                continue
            if isinstance(value, str):
                value = value.strip()

            setattr(asset, field, value)
            updated_fields.append(field)

        if (
            "status" in updated_fields
            and asset.status == Asset.Status.ARCHIVED
            and not asset.archived_at
        ):
            asset.archived_at = timezone.now()
            updated_fields.append("archived_at")

        if updated_fields:
            asset.save(update_fields=updated_fields)

        asset_type_uuid = data.get("asset_type_uuid")
        if asset_type_uuid:
            asset.asset_type = AssetSelector.get_asset_type_by_uuid(asset_type_uuid)
            asset.save(update_fields=["asset_type"])

        tag_uuids = data.get("tag_uuids")
        if tag_uuids is not None:
            tags = AssetSelector.get_tags_by_uuids(tag_uuids)
            asset.tags.set(tags)

        return asset

    @staticmethod
    @transaction.atomic
    def delete_asset(asset: Asset) -> None:
        asset.delete()