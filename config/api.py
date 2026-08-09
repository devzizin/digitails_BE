from django.contrib.admin.views.decorators import staff_member_required
from ninja import NinjaAPI
from ninja.security import SessionAuth

from apps.core.tenants.api.routes import router as tenants_router
from apps.core.companies.api.routes import router as companies_router

api = NinjaAPI(
    urls_namespace="api",
    auth=SessionAuth(),
)

api.add_router("/users/", "svitup.users.api.views.router")
api.add_router("/core/companies/", companies_router)
api.add_router("/core/tenants/", tenants_router)

