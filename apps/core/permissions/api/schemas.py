from ninja import Schema


class PermissionOut(Schema):
    code: str
    name: str


class RoleOut(Schema):
    id: int
    name: str
    is_system: bool
    permissions: list[PermissionOut]


class RoleCreateIn(Schema):
    name: str
    permission_codes: list[str] = []
    is_system: bool = False


class AssignRoleIn(Schema):
    company_user_uuid: int
    role_uuid: int


class RevokeRoleIn(Schema):
    company_user_uuid: int
    role_uuid: int


class UserRoleOut(Schema):
    id: int
    role: RoleOut
    assigned_at: str