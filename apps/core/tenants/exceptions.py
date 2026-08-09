from ninja.errors import HttpError


class TenantNotFound(HttpError):

    def __init__(self):
        super().__init__(
            404,
            "Tenant not found.",
        )

class PrimaryDomainNotFound(HttpError):

    def __init__(self):
        super().__init__(
            404,
            "Primary domain not found.",
        )


