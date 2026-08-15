from apps.core.tenants.models import Tenant, Domain
from apps.core.tenants.exceptions import TenantNotFound, PrimaryDomainNotFound



class TenantSelector:

    @staticmethod
    def get_tenant_by_uuid(*, tenant_uuid: int) -> Tenant:
        try:
            return Tenant.objects.get(uuid=tenant_uuid)
        except Tenant.DoesNotExist:
            raise TenantNotFound(f"Tenant with uuid '{tenant_uuid}' not found")

    @staticmethod
    def get_tenant_by_slug(*, slug: str) -> Tenant:
        try:
            return Tenant.objects.get(slug=slug)
        except Tenant.DoesNotExist:
            raise TenantNotFound(f"Tenant with slug '{slug}' not found")

    @staticmethod
    def get_tenant_by_domain(*, domain: str) -> Tenant:
        try:
            domain_obj = Domain.objects.get(domain=domain)
            return domain_obj.tenant
        except Domain.DoesNotExist:
            raise PrimaryDomainNotFound(f"Primary domain '{domain}' not found")

    @staticmethod
    def list_tenants():
        return Tenant.objects.all()

    @staticmethod
    def get_primary_domain(
    tenant: Tenant,
) -> Domain:

        domain = tenant.domains.filter(
            is_primary=True,
        ).first()

        if not domain:
            raise PrimaryDomainNotFound()

        return domain
