from django.conf import settings


def set_refresh_cookie(
    response,
    refresh: str,
):
    response.set_cookie(
        key=settings.AUTH_COOKIE_REFRESH_NAME,
        value=refresh,
        httponly=settings.AUTH_COOKIE_HTTP_ONLY,
        secure=settings.AUTH_COOKIE_SECURE,
        samesite=settings.AUTH_COOKIE_SAMESITE_REFRESH,
        domain=settings.AUTH_COOKIE_DOMAIN,
        max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
        path="/",
    )


def clear_auth_cookies(response):
    response.delete_cookie(
        settings.AUTH_COOKIE_REFRESH_NAME,
        domain=settings.AUTH_COOKIE_DOMAIN,
        path="/",
    )
