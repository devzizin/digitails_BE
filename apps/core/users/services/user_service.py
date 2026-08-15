from __future__ import annotations

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from ninja_jwt.token_blacklist.models import OutstandingToken, BlacklistedToken

from apps.core.companies.models import Company
from apps.core.permissions.services.permission_service import PermissionService
from apps.core.users.exceptions import (
    UserValidationError,
    InvalidOldPassword,
    InvalidPassword,
)
from apps.core.users.models import User, UserCompany
from apps.core.users.services.token_service import TokenService



class UserService:

    @staticmethod
    @transaction.atomic
    def revoke_refresh_tokens(user: User) -> None:
        for token in OutstandingToken.objects.filter(user=user):
            BlacklistedToken.objects.get_or_create(token=token)

    @staticmethod
    @transaction.atomic
    def create_user(**data) -> User:
        password = data.pop("password")
        temp_user = User(**data)

        try:
            temp_user.full_clean(
                exclude=[
                    "password",
                ],
            )
        except ValidationError as exc:
            raise UserValidationError(exc.message_dict)

        try:
            validate_password(password, temp_user)
        except ValidationError as exc:
            raise UserValidationError(exc.messages)

        return User.objects.create_user(password=password, **data)

    @staticmethod
    def authenticate_user(identifier: str, password: str) -> User | None:
        return authenticate(identifier=identifier, password=password)

    @staticmethod
    def email_exists(email: str) -> bool:
        return User.objects.filter(email=email.strip().lower()).exists()

    @staticmethod
    def username_exists(username: str) -> bool:
        return User.objects.filter(username=username.strip().lower()).exists()

    @staticmethod
    def change_password(user: User, old_password: str, new_password: str) -> None:
        if not user.check_password(old_password):
            raise InvalidOldPassword()

        try:
            validate_password(new_password, user)
        except ValidationError as exc:
            raise InvalidPassword(", ".join(exc.messages))

        user.set_password(new_password)
        user.save(update_fields=["password"])
        UserService.revoke_refresh_tokens(user)


  
    @staticmethod
    @transaction.atomic
    def register_user(
        *,
        company: Company,
        **data,
    ) -> User:

        user = UserService.create_user(**data)
        UserCompany.objects.create(
            user=user,
            company=company,
        )
        return user

    @staticmethod
    @transaction.atomic
    def update_user(
        user,
        **data,
    ):
        allowed_fields = {
            "first_name",
            "last_name",
            "username",
            "phone",
        }
        updated_fields = []
        for field, value in data.items():
            if field not in allowed_fields:
                continue
            if value is None:
                continue
            if isinstance(value, str):
                value = value.strip()

            setattr(user, field, value)
            updated_fields.append(field)

        try:
            user.full_clean(
                exclude=[
                    "password",
                ],
            )
        except ValidationError as exc:
            raise UserValidationError(
                getattr(
                    exc,
                    "message_dict",
                    exc.messages,
                )
            )

        user.save(
            update_fields=updated_fields,
        )

        return user

