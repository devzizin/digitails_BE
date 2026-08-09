from django.shortcuts import get_object_or_404
from ninja import Router

from apps.core.permissions.api.schemas import (
    AssignRoleIn,
    RevokeRoleIn,
    RoleCreateIn,
    RoleOut,
    UserRoleOut,
)
from apps.core.permissions.selectors.selectors import PermissionSelectors
from apps.core.permissions.services.services import PermissionServices
from apps.core.users.models import CompanyUser

router = Router(tags=["permissions"])


@router.get("/roles", response=list[RoleOut])
def list_roles(request):
    return PermissionSelectors.list_roles()


@router.get("/roles/{role_id}", response=RoleOut)
def get_role(request, role_id: int):
    return PermissionSelectors.get_role_by_id(role_id)


@router.post("/roles", response=RoleOut)
def create_role(request, payload: RoleCreateIn):
    return PermissionServices.create_role(
        name=payload.name,
        permission_codes=payload.permission_codes,
        is_system=payload.is_system,
    )


@router.post("/roles/assign", response=UserRoleOut)
def assign_role(request, payload: AssignRoleIn):
    company_user = get_object_or_404(CompanyUser, id=payload.company_user_id)
    role = PermissionSelectors.get_role_by_id(payload.role_id)
    return PermissionServices.assign_role(company_user=company_user, role=role)


@router.post("/roles/revoke", response={204: None})
def revoke_role(request, payload: RevokeRoleIn):
    company_user = get_object_or_404(CompanyUser, id=payload.company_user_id)
    role = PermissionSelectors.get_role_by_id(payload.role_id)
    PermissionServices.revoke_role(company_user=company_user, role=role)
    return 204, None


@router.get("/company-users/{company_user_id}/permissions", response=list[str])
def list_company_user_permissions(request, company_user_id: int):
    company_user = get_object_or_404(CompanyUser, id=company_user_id)
    return sorted(PermissionSelectors.get_company_user_permission_codes(company_user))