from __future__ import annotations

from django.db import transaction
from django_tenants.utils import schema_context, get_public_schema_name

from apps.core.companies.exceptions import CompanyAlreadyExists
from apps.core.companies.models import Company
from apps.core.companies.selectors.company_selector import CompanySelector
from apps.core.tenants.services.tenant_service import TenantService
from apps.core.tenants.services.slug_service import SlugService
from config.settings.base import TENANT_BASE_DOMAIN


class CompanyService:
    """
    Handles company creation + tenant bootstrap.
    """

    @staticmethod
    @transaction.atomic
    def create_company(*, data, slug=None):
        """
        Flow:
        1. Create Company (public)
        2. Create Tenant (public)
        """
        company_name = data.name
        if CompanySelector.get_by_name(company_name):
            raise CompanyAlreadyExists("Company with this name already exists.")

        schema_slug = SlugService.prepare_schema(
            name=company_name,
            slug=slug,
        )

        domain_slug = SlugService.prepare_domain(
            name=company_name,
            slug=slug,
        )

        domain = f"{domain_slug}.{TENANT_BASE_DOMAIN}"

        tenant = TenantService.create_tenant(
            name=company_name,
            slug=schema_slug,
            domain=domain,
        )

        company = Company.objects.create(
            tenant=tenant,
            name=company_name,
            address_text=data.address_text,
            phone=data.phone,
            email=data.email,
            website=data.website,
            logo_url=data.logo_url,
            identification_number=data.identification_number,
            is_verified=data.is_verified,
        )

        return {
            "tenant": {
                "id": tenant.id,
                "slug": tenant.slug,
                "schema_name": tenant.schema_name,
                "domain": domain,
            },
            "company": company,
        }
    

    @staticmethod
    @transaction.atomic
    def update_company(*, company, data):
        update_data = data.dict(exclude_unset=True)

        for field, value in update_data.items():
            setattr(company, field, value)

        company.save(update_fields=list(update_data.keys()))

        return company

    @staticmethod
    def delete_company(*, company):
        """
        Soft delete company + deactivate tenant.
        """
        with schema_context(get_public_schema_name()):
            tenant = company.tenant
            company.mark_deleted()
            TenantService.deactivate_tenant(tenant=tenant)
