# from django.urls import reverse
# from ninja import ModelSchema

# from apps.core.users.models import User


# class UpdateUserSchema(ModelSchema):
#     class Meta:
#         model = User
#         fields = ["name"]


# class UserSchema(ModelSchema):
#     url: str

#     class Meta:
#         model = User
#         fields = ["email", "name"]

#     @staticmethod
#     def resolve_url(obj: User):
#         return reverse("api:retrieve_user", kwargs={"pk": obj.pk})
from __future__ import annotations

from datetime import datetime
from typing import Optional, Annotated
from uuid import UUID

from ninja import Schema, FilterSchema, FilterLookup
from pydantic import EmailStr, field_validator, ConfigDict, Field

from apps.core.users.selectors.user_selector import UserSelector


class LoginSchema(Schema):
    identifier: str
    password: str

    @field_validator("identifier")
    @classmethod
    def normalize_identifier(cls, value: str) -> str:
        return value.strip().lower()


class RegisterSchema(Schema):
    email: EmailStr
    username: str | None = None
    password: str
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None

    @field_validator("email")
    @classmethod
    def validate_email_strict(cls, value):
        if not value.isascii():
            raise ValueError("Email must contain only ASCII characters")
        return value.lower().strip()

    @field_validator("username")
    @classmethod
    def normalize_username(cls, value: str | None) -> str | None:
        if value is None:
            return value
        value = value.strip().lower()
        return value or None


class CreateUserSchema(Schema):
    email: EmailStr

    password: str

    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None


class VerifySchema(Schema):
    token: str


class VerifyResponseSchema(Schema):
    valid: bool


class MessageSchema(Schema):
    detail: str


class MeSchema(Schema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uuid: UUID
    email: str
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool


class AuthUserResponseSchema(Schema):
    access: str
    user: MeSchema


class RefreshResponseSchema(Schema):
    access: str


class ChangePasswordSchema(Schema):
    old_password: str
    new_password: str


class ResetPasswordRequestSchema(Schema):
    email: EmailStr



class ErrorSchema(Schema):
    detail: str


class UpdateUserSchema(Schema):
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    phone: str | None = None

    @field_validator("username")
    @classmethod
    def normalize_username(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        value = value.strip().lower()

        return value or None


class AcceptInvitationSchema(Schema):
    token: str

    password: str | None = None

    first_name: str | None = None
    last_name: str | None = None


class CreateInvitationSchema(Schema):
    email: EmailStr


class InvitationInfoSchema(Schema):
    email: EmailStr
    company_name: str
    user_exists: bool
    status: str
    invited_by: EmailStr | None = None
    expires_at: datetime


class InvitationListItemSchema(Schema):
    model_config = ConfigDict(from_attributes=True)

    uuid: UUID
    email: EmailStr
    status: str
    invited_by: EmailStr | None = None
    expires_at: datetime
    created_at: datetime


class InvitationListFilterSchema(FilterSchema):

    email: Annotated[
        str | None,
        FilterLookup("email__icontains"),
    ] = Field(
        default=None,
        description="Search invitations by email.",
    )




class CurrentCompanySchema(Schema):
    uuid: UUID
    name: str


