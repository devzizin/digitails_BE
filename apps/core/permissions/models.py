import uuid

from django.db import models


class Permission(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, db_index=True)

    code = models.CharField(max_length=100, unique=True)
    action = models.CharField(max_length=50, db_index=True)
    resource_type = models.CharField(max_length=100, db_index=True)
    module_code = models.CharField(max_length=100, db_index=True)

    description = models.TextField(blank=True)
    is_system = models.BooleanField(default=False)

    class Meta:
        db_table = "permissions"

    def __str__(self) -> str:
        return self.code


class Role(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, db_index=True)

    code = models.CharField(max_length=100, unique=True)
    label = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    permissions = models.ManyToManyField(
        Permission,
        through="RolePermission",
        related_name="roles",
        blank=True,
    )

    is_system = models.BooleanField(
        default=False,
        help_text="Bootstrap-created roles (Owner, Manager, etc.) that cannot be deleted.",
    )

    class Meta:
        db_table = "roles"

    def __str__(self) -> str:
        return self.code


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="role_permissions")
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name="permission_roles")

    class Meta:
        db_table = "role_permissions"
        unique_together = ("role", "permission")


class UserRole(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, db_index=True)

    company_user = models.ForeignKey(
        "users.UserCompany",
        on_delete=models.CASCADE,
        related_name="roles",
    )
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="user_roles")

    entity = models.ForeignKey(
        "entities.Entity",
        on_delete=models.CASCADE,
        related_name="user_roles",
        null=True,
        blank=True,
        help_text="If not specified — the role applies to the entire company.",
    )

    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_roles"
        unique_together = ("company_user", "role", "entity")

    def __str__(self) -> str:
        scope = self.entity_id or "company-wide"
        return f"{self.company_user} -> {self.role} ({scope})"