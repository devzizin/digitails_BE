from typing import List, Optional

from ninja import Router
from ninja_jwt.authentication import JWTAuth

from apps.core.companies.selectors.company_selector import CompanySelector
from apps.core.companies.services.company_service import CompanyService
from .schemas import (
    CompanyCreateSchema,
    CompanyUpdateSchema,
    CompanyResponseSchema,
    CompanyCreateResponseSchema,
    ErrorSchema,
)


router = Router(tags=["Core Companies"]) #, auth=JWTAuth())


@router.get(
    "/",
    response={200: List[CompanyResponseSchema]},
)
def list_companies(request, search: Optional[str] = None):
    return CompanySelector.list_companies(search=search)


@router.post(
    "/",
    response={
        201: CompanyCreateResponseSchema,
        400: ErrorSchema,
        409: ErrorSchema,
        422: ErrorSchema,
    },
)
def create_company(request, payload: CompanyCreateSchema):
    result = CompanyService.create_company(
        data=payload,
    )

    return 201, result


@router.get(
    "/{company_id}",
    response={
        200: CompanyResponseSchema,
        404: ErrorSchema,
    },
)
def get_company(request, company_id: int):
    company = CompanySelector.get_company_by_id(company_id)
    return CompanySelector.build_response(company)


@router.patch(
    "/{company_id}",
    response={
        200: CompanyResponseSchema,
        404: ErrorSchema,
        422: ErrorSchema,
    },
)
def update_company(request, company_id: int, payload: CompanyUpdateSchema):
    company = CompanySelector.get_company_by_id(company_id)

    company = CompanyService.update_company(
        company=company,
        data=payload,
    )

    return CompanySelector.build_response(company)


@router.delete(
    "/{company_id}",
    response={
        204: None,
        404: ErrorSchema,
    },
)
def delete_company(request, company_id: int):
    company = CompanySelector.get_company_by_id(company_id)
    CompanyService.delete_company(company=company)

    return 204, None
