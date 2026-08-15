from ninja_jwt.tokens import RefreshToken, Token

from apps.core.users.models import User
from apps.core.companies.models import Company


def build_refresh_token(
    *,
    user: User,
    company: Company,
) -> Token:
    refresh = RefreshToken.for_user(user)

    refresh["email"] = user.email
    refresh["user_uuid"] = str(user.uuid)

    refresh["company_id"] = company.id
    refresh["company_uuid"] = str(company.uuid)
    refresh["company_name"] = company.name

    refresh["tenant_id"] = company.tenant.id
    refresh["tenant_uuid"] = str(company.tenant.uuid)
    refresh["tenant_slug"] = company.tenant.slug

    return refresh


def build_token_pair_for_user(
    *,
    user: User,
    company: Company,
) -> dict[str, str]:

    refresh = build_refresh_token(
        user=user,
        company=company,
    )

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }
