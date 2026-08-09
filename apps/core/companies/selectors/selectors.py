from apps.core.companies.models import Company
from apps.core.companies.exceptions import CompanyNotFound


class CompanySelector:

    @staticmethod
    def build_response(company):
        return {
            "id": company.id,
            "uuid": company.uuid,
            "name": company.name,
            "email": company.email,
            "phone": company.phone,
            "is_verified": company.is_verified,
            "created_at": company.created_at,
            "logo_url": company.logo_url,
            "logo_url": company.logo_url,
        }

    @staticmethod
    def get_by_name(name: str):
        return (
            Company.objects.active()
            .filter(name__iexact=name)
            .select_related("tenant")
            .first()
        )

    @staticmethod
    def list_companies(search=None):
        qs = Company.objects.active()

        if search:
            qs = qs.filter(name__icontains=search)

        return qs

    @staticmethod
    def get_company_by_id(
        company_id: int,
    ):
        company = Company.objects.active().filter(id=company_id).first()

        if not company:
            raise CompanyNotFound()

        return company

    @staticmethod
    def get_current_company(tenant):
        company = Company.objects.active().filter(tenant=tenant).first()

        if not company:
            raise CompanyNotFound()

        return company

