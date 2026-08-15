from uuid import UUID

from ninja import Query, Router
from ninja_jwt.authentication import JWTAuth

from apps.core.assets.api import schemas
from apps.core.assets.selectors.asset_selector import AssetSelector
from apps.core.assets.services.asset_service import AssetService

router = Router(tags=["Assets"])


@router.get(
    "",
    auth=JWTAuth(),
    response={200: list[schemas.AssetOut]},
)
def list_assets(request, filters: schemas.AssetFilterSchema = Query(...)):
    return AssetSelector.get_assets(filters=filters)


@router.get(
    "/{asset_uuid}",
    auth=JWTAuth(),
    response={200: schemas.AssetOut, 404: schemas.ErrorSchema},
)
def get_asset(request, asset_uuid: UUID):
    return AssetSelector.get_asset_by_uuid(asset_uuid)


@router.post(
    "",
    auth=JWTAuth(),
    response={200: schemas.AssetOut, 400: schemas.ErrorSchema},
)
def create_asset(request, payload: schemas.CreateAssetSchema):
    owner = getattr(request.user, "company_profile", None)

    asset = AssetService.create_asset(
        owner=owner,
        **payload.dict(exclude_unset=True, exclude_none=True),
    )

    return asset


@router.patch(
    "/{asset_uuid}",
    auth=JWTAuth(),
    response={
        200: schemas.AssetOut,
        400: schemas.ErrorSchema,
        404: schemas.ErrorSchema,
    },
)
def update_asset(request, asset_uuid: UUID, payload: schemas.UpdateAssetSchema):
    asset = AssetSelector.get_asset_by_uuid(asset_uuid)

    asset = AssetService.update_asset(
        asset,
        **payload.dict(exclude_unset=True),
    )

    return asset


@router.delete(
    "/{asset_uuid}",
    auth=JWTAuth(),
    response={204: None, 404: schemas.ErrorSchema},
)
def delete_asset(request, asset_uuid: UUID):
    asset = AssetSelector.get_asset_by_uuid(asset_uuid)
    AssetService.delete_asset(asset)
    return 204, None