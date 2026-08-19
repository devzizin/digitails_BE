import uuid

from django.db import models


class Permission(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, db_index=True)

    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "permissions"

    def __str__(self) -> str:
        return self.code


class Role(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, db_index=True)

    name = models.CharField(max_length=100)
    is_system = models.BooleanField(
        default=False,
        help_text="Default roles (e.g. Owner, Manager) that cannot be deleted.",
    )
    permissions = models.ManyToManyField(Permission, related_name="roles", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "roles"

    def __str__(self) -> str:
        return self.name


class UserRole(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, db_index=True)

    company_user = models.ForeignKey(
        "users.UserCompany",
        on_delete=models.CASCADE,
        related_name="roles",
    )
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="user_roles")
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_roles"
        unique_together = ("company_user", "role")

    def __str__(self) -> str:
        return f"{self.company_user} -> {self.role}"