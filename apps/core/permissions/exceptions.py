from ninja.errors import HttpError


class RoleNotFoundError(HttpError):
    def __init__(self):
        super().__init__(404, "Role not found")


class PermissionNotFoundError(HttpError):
    def __init__(self):
        super().__init__(404, "Permission not found")


class RoleAlreadyAssignedError(HttpError):
    def __init__(self):
        super().__init__(409, "Role is already assigned to this user")


class PermissionDeniedError(HttpError):
    def __init__(self):
        super().__init__(403, "You do not have permission to perform this action")