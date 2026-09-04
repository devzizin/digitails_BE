from functools import wraps

from typing import Callable

from apps.core.permissions.exceptions import PermissionDeniedError
from apps.core.permissions.selectors.permission_selector import PermissionSelector
from apps.core.entities.models import Entity


def permission_required(code: str, entity_kwarg: str | None = None):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            company_user = request.auth.company_profile

            entity = None
            if entity_kwarg:
                entity_id = kwargs.get(entity_kwarg)
                entity = Entity.objects.filter(pk=entity_id).first() if entity_id else None

            if not PermissionSelector.company_user_has_permission(
                company_user=company_user, code=code, entity=entity
            ):
                raise PermissionDeniedError()
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator