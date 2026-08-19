import re
from datetime import datetime
from typing import Optional
from uuid import UUID

import unicodedata
from ninja import Schema
# from pydantic import EmailStr, field_validator

from apps.core.tenants.api.schemas import TenantResponseSchema


class ErrorSchema(Schema):
    detail: str


class CompanyCreateSchema(Schema):
    name: str
    email: Optional[str] = None
    address_text: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    identification_number: Optional[str] = None
    is_verified: bool = False
    secret_key: Optional[str] = None

    # @field_validator("name")
    # @classmethod
    # def validate_name(cls, v):

    #     v = unicodedata.normalize(
    #         "NFKC",
    #         v.strip(),
    #     )

    #     if len(v) < 2:
    #         raise ValueError("Name too short")

    #     has_latin = bool(
    #         re.search(
    #             r"[A-Za-z]",
    #             v,
    #         )
    #     )

    #     has_cyrillic = bool(
    #         re.search(
    #             r"[А-Яа-яІіЇїЄєҐґ]",
    #             v,
    #         )
    #     )

    #     if has_latin and has_cyrillic:
    #         raise ValueError("Company name cannot mix Latin and Cyrillic characters.")

    #     return v


class CompanyUpdateSchema(Schema):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    logo_url: Optional[str] = None
    is_verified: Optional[bool] = None


class CompanyResponseSchema(Schema):
    id: int
    # uuid: UUID
    name: str
    email: Optional[str]
    phone: Optional[str]
    is_verified: bool
    created_at: datetime
    logo_url: str | None

class CompanyCreateResponseSchema(Schema):
    tenant: TenantResponseSchema
    company: CompanyResponseSchema
