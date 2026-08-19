from ninja import Router
from ninja_jwt.authentication import JWTAuth

from apps.core.permissions.selectors.permission_selector import PermissionSelector
from apps.core.users.api import schemas
from apps.core.users.selectors.user_selector import UserSelector
from apps.core.users.services.user_service import UserService
from apps.core.permissions.decorators import permission_required
from apps.core.users.exceptions import (
    Unauthorized,
    UserInactive,
)


router = Router(tags=["Users"])


@router.get(
    "/me",
    auth=JWTAuth(),
    response={
        200: schemas.MeSchema,
    },
)
def me(request):
    user = request.user

    if not user or not user.is_authenticated:
        raise Unauthorized()

    if not user.is_active:
        raise UserInactive()

    return 200, user


@router.patch(
    "/me",
    auth=JWTAuth(),
    response={
        200: schemas.MeSchema,
        400: schemas.ErrorSchema,
    },
)
def update_me(
    request,
    payload: schemas.UpdateUserSchema,
):
    user = UserService.update_user(
        user=request.user,
        **payload.dict(
            exclude_unset=True,
            exclude_none=True,
        ),
    )

    return 200, user


# @router.get(
#     "/me/permissions",
#     auth=JWTAuth(),
#     response={
#         200: schemas.UserPermissionsSchema,
#     },
#     summary="Get current user permissions",
#     description="""
#     Return aggregated permission snapshot for the authenticated user.
#     """,
# )
# def me_permissions(request):
#     return 200, PermissionSelector.get_user_permission_snapshot(request.user)

