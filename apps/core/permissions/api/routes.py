from django.shortcuts import get_object_or_404
from ninja import Router

from apps.core.permissions.api.schemas import (
    AssignRoleIn,
    RevokeRoleIn,
    RoleCreateIn,
    RoleOut,
    UserRoleOut,
)
from apps.core.permissions.selectors.permission_selector import PermissionSelector
from apps.core.permissions.services.permission_service import PermissionService
from apps.core.users.models import User, UserCompany

router = Router(tags=["permissions"])


@router.get("/roles", response=list[RoleOut])
def list_roles(request):
    return PermissionSelector.list_roles()


@router.get("/roles/{role_uuid}", response=RoleOut)
def get_role(request, role_uuid: str):
    return PermissionSelector.get_role_by_uuid(role_uuid)



@router.post("/roles/assign", response=UserRoleOut)
def assign_role(request, payload: AssignRoleIn):
    company_user = get_object_or_404(UserCompany, uuid=payload.company_user_uuid)
    role = PermissionSelector.get_role_by_uuid(payload.role_uuid)
    return PermissionService.assign_role(company_user=company_user, role=role)


@router.post("/roles/revoke", response={204: None})
def revoke_role(request, payload: RevokeRoleIn):
    company_user = get_object_or_404(UserCompany, uuid=payload.company_user_uuid)
    role = PermissionSelector.get_role_by_uuid(payload.role_uuid)
    PermissionService.revoke_role(company_user=company_user, role=role)
    return 204, None


@router.get("/company-users/{company_user_uuid}/permissions", response=list[str])
def list_company_user_permissions(request, company_user_uuid: str):
    company_user = get_object_or_404(UserCompany, uuid=company_user_uuid)
    return sorted(PermissionSelector.get_company_user_permission_codes(company_user))