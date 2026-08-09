from django.db import transaction

from apps.core.permissions.exceptions import RoleAlreadyAssignedError, RoleNotFoundError
from apps.core.permissions.models import Permission, Role, UserRole
from apps.core.permissions.selector import PermissionSelectors
from apps.core.users.models import CompanyUser


class PermissionServices:
    @staticmethod
    @transaction.atomic
    def create_role(
        *, name: str, permission_codes: list[str] | None = None, is_system: bool = False
    ) -> Role:
        role = Role.objects.create(name=name, is_system=is_system)
        if permission_codes:
            permissions = Permission.objects.filter(code__in=permission_codes)
            role.permissions.set(permissions)
        return role

    @staticmethod
    @transaction.atomic
    def assign_role(*, company_user: CompanyUser, role: Role) -> UserRole:
        if PermissionSelectors.get_user_role(company_user=company_user, role=role):
            raise RoleAlreadyAssignedError()

        return UserRole.objects.create(company_user=company_user, role=role)

    @staticmethod
    @transaction.atomic
    def revoke_role(*, company_user: CompanyUser, role: Role) -> None:
        user_role = PermissionSelectors.get_user_role(company_user=company_user, role=role)
        if not user_role:
            raise RoleNotFoundError()
        user_role.delete()