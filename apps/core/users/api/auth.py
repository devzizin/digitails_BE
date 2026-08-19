from django.db import IntegrityError
from django.http import JsonResponse
from ninja import Router
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.exceptions import TokenError
from ninja_jwt.tokens import RefreshToken
from django.http import JsonResponse

from apps.core.companies.exceptions import CompanyNotFound
from apps.core.companies.selectors.company_selector import CompanySelector
from apps.core.tenants.services.tenant_service import TenantService
from apps.core.users.api import schemas
from apps.core.users.exceptions import (
    UserValidationError,
    InvalidCredentials,
    EmailAlreadyExists,
    UsernameAlreadyExists,
    UserCreationFailed,
    UserInactive,
    MissingRefreshToken,
    InvalidRefreshToken,
)
from apps.core.users.jwt import build_token_pair_for_user, build_refresh_token
from apps.core.users.selectors.user_selector import UserSelector
from apps.core.users.services.token_service import TokenService
from apps.core.users.services.user_service import UserService
from apps.core.users.utils.cookies import clear_auth_cookies, set_refresh_cookie

router = Router(tags=["Auth"])


@router.post(
    "/register",
    response={
        200: schemas.AuthUserResponseSchema,
        400: schemas.ErrorSchema,
        422: schemas.ErrorSchema,
    },
    auth=None,
)
def register(request, payload: schemas.RegisterSchema):
    if UserService.email_exists(payload.email):
        raise EmailAlreadyExists()

    # if payload.username and UserService.username_exists(payload.username):
    #     raise UsernameAlreadyExists()

    try:
        company = request.tenant.company
        user = UserService.register_user(company=company, **payload.dict())

    except UserValidationError as exc:
        return 422, {"detail": str(exc)}

    except IntegrityError:
        raise UserCreationFailed()

    tokens = build_token_pair_for_user(
        user=user,
        company=company,
    )

    data = schemas.AuthUserResponseSchema.model_validate(
        {
            "access": tokens["access"],
            "user": user,
        }
    ).model_dump()
    data["access"] = tokens["access"]

    response = JsonResponse(data, status=200)

    set_refresh_cookie(
        response,
        refresh=tokens["refresh"],
    )

    return response


@router.post(
    "/login",
    response={
        200: schemas.AuthUserResponseSchema,
        401: schemas.ErrorSchema,
    },
    auth=None,
)
def login(request, payload: schemas.LoginSchema):
    user = UserService.authenticate_user(
        identifier=payload.identifier,
        password=payload.password,
    )
    company = request.tenant.company
    if not user:
        raise InvalidCredentials()

    if not user.is_active:
        raise UserInactive()


    tokens = build_token_pair_for_user(
        user=user,
        company=company,
    )

    data = schemas.AuthUserResponseSchema.model_validate(
        {
            "access": tokens["access"],
            "user": user,
        }
    ).model_dump()
    data["access"] = tokens["access"]

    response = JsonResponse(data, status=200)

    set_refresh_cookie(
        response,
        refresh=tokens["refresh"],
    )

    return response



@router.post(
    "/refresh",
    response={
        200: schemas.RefreshResponseSchema,
        401: schemas.ErrorSchema,
    },
)
def refresh_token(request):
    refresh_cookie = request.COOKIES.get("refresh")

    if not refresh_cookie:
        raise MissingRefreshToken()

    try:
        old_refresh = RefreshToken(refresh_cookie)
        user = UserSelector.get_user_by_id(old_refresh["user_id"])

        # blacklist old token
        old_refresh.blacklist()
        company_uuid = old_refresh["company_uuid"]
        company = CompanySelector.get_user_company(
            user=user,
            company_uuid=company_uuid,
        )
        # create NEW refresh token
        new_refresh = build_refresh_token(
            user=user,
            company=company,
        )

        response = JsonResponse(
            {
                "access": str(new_refresh.access_token),
            }
        )

        set_refresh_cookie(
            response,
            refresh=str(new_refresh),
        )
        return response

    except (TokenError, CompanyNotFound):

        raise InvalidRefreshToken()


@router.post(
    "/logout",
    response=schemas.MessageSchema,
)
def logout(request):
    refresh_cookie = request.COOKIES.get("refresh")

    if refresh_cookie:
        try:
            refresh = RefreshToken(refresh_cookie)
            refresh.blacklist()
        except TokenError:
            pass

    response = JsonResponse({"detail": "Logged out successfully."})
    clear_auth_cookies(response)

    return response



@router.post(
    "/change-password",
    auth=JWTAuth(),
    response={
        200: schemas.MessageSchema,
        400: schemas.ErrorSchema,
    },
)
def change_password(request, payload: schemas.ChangePasswordSchema):
    UserService.change_password(
        user=request.user,
        old_password=payload.old_password,
        new_password=payload.new_password,
    )

    return schemas.MessageSchema(
        detail="Password updated successfully.",
    )


