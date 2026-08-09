from uuid import UUID

from ninja import Schema


class TenantCreateSchema(Schema):
    name: str
    slug: str
    domain: str


class TenantUpdateSchema(Schema):
    name: str


class TenantResponseSchema(Schema):
    id: int
    slug: str
    schema_name: str
    domain: str

class TenantListSchema(Schema):
    id: int
    uuid: UUID
    name: str
    slug: str
    is_active: bool
    is_initialized: bool
