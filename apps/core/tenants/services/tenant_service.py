from django.conf import settings
from django.db import transaction, IntegrityError
from django_tenants.utils import schema_context

from apps.core.tenants.models import Tenant, Domain
from apps.core.tenants.services.slug_service import SlugService
from apps.core.tenants.selectors.tenants_selector import TenantSelector

class TenantService:

    @staticmethod
    @transaction.atomic
    def create_tenant(
        *,
        name: str,
        slug: str | None = None,
        domain: str,
    ) -> Tenant:

        with schema_context("public"):
            slug = slug or None

            if Domain.objects.filter(domain=domain).exists():
                raise ValueError(f"Domain '{domain}' already exists")

            for _ in range(3):
                try:
                    prepared_slug = SlugService.prepare(name=name, slug=slug)

                    tenant = Tenant.objects.create(
                        name=name,
                        slug=prepared_slug,
                        schema_name=prepared_slug,
                    )
                    break

                except IntegrityError:
                    slug = None

            else:
                raise RuntimeError("Failed to generate unique tenant slug")

            Domain.objects.create(
                tenant=tenant,
                domain=domain,
                is_primary=True,
            )

        return tenant

    @staticmethod
    def deactivate_tenant(*, tenant: Tenant) -> Tenant:
        """
        Disable tenant access.
        """
        tenant.is_active = False
        tenant.save(update_fields=["is_active"])
        return tenant

    @staticmethod
    def activate_tenant(*, tenant: Tenant) -> Tenant:
        """
        Enable tenant access again.
        """
        tenant.is_active = True
        tenant.save(update_fields=["is_active"])
        return tenant

    @staticmethod
    def update_tenant_name(*, tenant: Tenant, name: str) -> Tenant:
        """
        Update tenant display name.
        """
        tenant.name = name
        tenant.save(update_fields=["name"])
        return tenant

    @staticmethod
    def build_frontend_base_url(tenant: Tenant) -> str:
        protocol = "http" if settings.DEBUG else "https"
        domain = TenantSelector.get_primary_domain(tenant)

        return f"{protocol}://" f"{domain.domain}:{settings.FRONTEND_PORT}"
