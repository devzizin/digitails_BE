from apps.core.permissions.exceptions import PermissionNotFoundError, RoleNotFoundError
from apps.core.permissions.models import Permission, Role, UserRole
from apps.core.users.models import CompanyUser


class PermissionSelector:
    @staticmethod
    def get_role_by_id(role_id: int) -> Role:
        role = Role.objects.filter(id=role_id).first()
        if not role:
            raise RoleNotFoundError()
        return role

    @staticmethod
    def get_role_by_name(name: str) -> Role | None:
        # Stays nullable: callers use this to check whether a default
        # role already exists before seeding it — None is expected.
        return Role.objects.filter(name=name).first()

    @staticmethod
    def get_permission_by_code(code: str) -> Permission:
        permission = Permission.objects.filter(code=code).first()
        if not permission:
            raise PermissionNotFoundError()
        return permission

    @staticmethod
    def list_roles():
        return Role.objects.all().order_by("name")

    @staticmethod
    def get_user_role(*, company_user: CompanyUser, role: Role) -> UserRole | None:
        # Stays nullable: used as an existence check (is this role
        # already assigned?), not a "fetch a required object" lookup.
        return UserRole.objects.filter(company_user=company_user, role=role).first()

    @staticmethod
    def get_company_user_permission_codes(company_user: CompanyUser) -> set[str]:
        return set(
            Permission.objects.filter(roles__user_roles__company_user=company_user).values_list(
                "code", flat=True
            )
        )

    @staticmethod
    def company_user_has_permission(*, company_user: CompanyUser, code: str) -> bool:
        return Permission.objects.filter(
            code=code,
            roles__user_roles__company_user=company_user,
        ).exists()