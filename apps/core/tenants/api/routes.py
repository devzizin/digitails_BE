from ninja import Router
from ninja_jwt.authentication import JWTAuth

from apps.core.tenants.api.schemas import (
    TenantCreateSchema,
    TenantUpdateSchema,
    TenantResponseSchema,
    TenantListSchema,
)

from apps.core.tenants.selectors.selectors import TenantSelector
from apps.core.tenants.services.services import TenantService


router = Router(tags=["Platform Tenants"]) #, auth=JWTAuth())


@router.get(
    "/",
    response=list[TenantListSchema],
    summary="List tenants",
    description="""
Return list of all platform tenants.

Each tenant corresponds to an isolated PostgreSQL schema.
This endpoint is usually restricted to platform administrators.
""",
)
def tenants_list(request):
    return TenantSelector.list_tenants()


@router.get(
    "/{slug}",
    response=TenantResponseSchema,
    summary="Get tenant",
    description="""
    Retrieve a single tenant by slug.

    The slug uniquely identifies a tenant workspace
    and also matches the PostgreSQL schema name.
    """,
    )
def tenant_get(request, slug: str):
    tenant = TenantSelector.get_tenant_by_slug(slug=slug)
    return tenant


@router.post(
    "/",
    response=TenantResponseSchema,
    summary="Create tenant",
    description="""
    Create a new tenant workspace.

    This operation will:

    • Create a Tenant record
    • Create a Domain mapping
    • Automatically create a PostgreSQL schema
    • Run tenant migrations
    """,
    )
def tenant_create(
    request,
    payload: TenantCreateSchema,
):

    tenant = TenantService.create_tenant(**payload.dict())
    return tenant


@router.patch(
    "/{slug}",
    response=TenantResponseSchema,
    summary="Update tenant",
    description="""
    Update tenant information.

    Currently only the display name can be updated.
    Changing slug or schema name is not allowed.
    """,
    )
def tenant_update(
    request,
    slug: str,
    payload: TenantUpdateSchema,
):

    tenant = TenantSelector.get_tenant_by_slug(slug=slug)
    tenant = TenantService.update_tenant_name(
        tenant=tenant,
        name=payload.name,
    )

    return tenant


@router.post(
    "/{slug}/deactivate",
    response=TenantResponseSchema,
    summary="Deactivate tenant",
    description="""
    Deactivate tenant access.

    The tenant schema remains intact
    but the workspace becomes inactive.
    """,
    )
def tenant_deactivate(
    request,
    slug: str,
):

    tenant = TenantSelector.get_tenant_by_slug(slug=slug)
    tenant = TenantService.deactivate_tenant(tenant=tenant)

    return tenant


@router.post(
    "/{slug}/activate",
    response=TenantResponseSchema,
    summary="Activate tenant",
    description="""
    Re-activate a previously deactivated tenant.
    """,
    )
def tenant_activate(
    request,
    slug: str,
):
    tenant = TenantSelector.get_tenant_by_slug(slug=slug)
    tenant = TenantService.activate_tenant(tenant=tenant)

    return tenant
