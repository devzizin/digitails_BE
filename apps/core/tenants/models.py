import uuid

from django.db import models
from django.utils import timezone
from django_tenants.models import DomainMixin, TenantMixin



class Tenant(TenantMixin):
    """
    Platform tenant.

    One tenant = one isolated PostgreSQL schema.
    This is an infrastructure model, not a business company model.
    """

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    name = models.CharField(
        max_length=255,
        help_text="Human-readable tenant name",
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text="Unique tenant slug used for references and defaults",
    )
    is_active = models.BooleanField(
        default=True,
    )
    is_initialized = models.BooleanField(
        default=False,
        help_text="Indicates whether tenant bootstrap process has completed successfully.",
    )
    initialized_at = models.DateTimeField(
        null=True,
        blank=True,
    ) 

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
    )   

    auto_create_schema = True

    class Meta:
        db_table = "tenants"
        ordering = ["name"]

    def mark_initialized(self) -> None:
        self.is_initialized = True
        self.initialized_at = timezone.now()
        self.save(update_fields=["is_initialized", "initialized_at", "updated_at"])

    def __str__(self) -> str:
        return self.name


class Domain(DomainMixin):
    """
    Maps a hostname to a tenant.

    Example:
    - main.localhost
    - acme.localhost
    - app.customer.com
    """

    class Meta:
        db_table = "domains"

    def __str__(self) -> str:
        return self.domain
