from functools import wraps

from apps.core.permissions.exceptions import PermissionDeniedError
from apps.core.permissions.selectors.selectors import PermissionSelectors


def require_permission(code: str):
    """Guards a Ninja route: raises PermissionDeniedError (403) unless
    the requesting user's CompanyUser has the given permission code.

    Assumes request.auth is a User with a related CompanyUser via
    `company_profile` (see apps.core.users.models.CompanyUser).
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            company_user = request.auth.company_profile
            if not PermissionSelectors.company_user_has_permission(
                company_user=company_user, code=code
            ):
                raise PermissionDeniedError()
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator