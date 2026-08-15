from uuid import UUID

from apps.business.assets.exceptions import AssetNotFound, AssetTypeNotFound, TagNotFound
from apps.business.assets.models import Asset, AssetType, Tag


class AssetSelector:

    @staticmethod
    def get_asset_by_uuid(asset_uuid: UUID) -> Asset:
        asset = (
            Asset.objects.select_related("asset_type", "owner")
            .prefetch_related("tags")
            .filter(uuid=asset_uuid)
            .first()
        )

        if not asset:
            raise AssetNotFound()

        return asset

    @staticmethod
    def get_assets(filters=None):
        queryset = (
            Asset.objects.select_related("asset_type", "owner")
            .prefetch_related("tags")
            .all()
        )

        if filters:
            queryset = filters.filter(queryset)

        return queryset

    @staticmethod
    def get_asset_type_by_uuid(asset_type_uuid: UUID) -> AssetType:
        asset_type = AssetType.objects.filter(uuid=asset_type_uuid).first()

        if not asset_type:
            raise AssetTypeNotFound()

        return asset_type

    @staticmethod
    def list_asset_types():
        return AssetType.objects.all()

    @staticmethod
    def get_tags_by_uuids(tag_uuids: list[UUID]):
        tags = Tag.objects.filter(uuid__in=tag_uuids)

        found_uuids = set(tags.values_list("uuid", flat=True))
        missing = set(tag_uuids) - found_uuids

        if missing:
            raise TagNotFound()

        return tags

    @staticmethod
    def list_tags():
        return Tag.objects.all()