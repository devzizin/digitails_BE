from django.contrib.admin.views.decorators import staff_member_required
from ninja import NinjaAPI
from ninja_jwt.authentication import JWTAuth
from ninja.security import SessionAuth

from apps.core.tenants.api.routes import router as tenants_router
from apps.core.companies.api.routes import router as companies_router
from apps.core.users.api.routes import router as users_router
from apps.core.users.api.auth import router as auth_router
from apps.core.permissions.api.routes import router as permissions_router
from apps.business.assets.api.routes import router as assets_router


api = NinjaAPI(
    urls_namespace="api",
    # auth=JWTAuth(),
)

api.add_router("/users/", users_router)
api.add_router("/auth/", auth_router)
api.add_router("/core/companies/", companies_router)
api.add_router("/core/tenants/", tenants_router)
api.add_router("/core/permissions/", permissions_router)
api.add_router("/business/assets/", assets_router)
