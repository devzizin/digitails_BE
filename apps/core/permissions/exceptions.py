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



class InvalidPermissionCode(HttpError):
    def __init__(self, code):

        super().__init__(
            422,
            (
                f"Invalid permission code '{code}'. "
                f"Expected format: "
                f"'<namespace>.<resource>.<action>' "
                f"(example: 'core.company.read')"
            ),
        )


class InvalidTemplateCode(HttpError):
    def __init__(self, code):

        super().__init__(
            422,
            (
                f"Invalid template code '{code}'. "
                f"Expected formats: "
                f"'core.company.admin', "
                f"'business.assets.viewer', "
                f"'tenant.admin'"
            ),
        )


class InvalidTemplateLevel(HttpError):
    def __init__(self, level):
        super().__init__(
            422,
            (
                f"Invalid template level '{level}'. "
                f"Allowed levels: "
                f"admin, manager, editor, viewer, "
                f"contributor, restricted"
            ),
        )


class InvalidAction(HttpError):
    def __init__(self, action):

        super().__init__(
            422,
            (
                f"Invalid action '{action}'. "
                f"Allowed actions: "
                f"list, create, read, update, "
                f"delete, assign, manage, export"
            ),
        )


class InvalidResource(HttpError):
    def __init__(self, resource):

        super().__init__(
            422,
            (
                f"Invalid resource '{resource}'. "
                f"Resource must be: "
                f"lowercase, singular, snake_case"
            ),
        )


class InvalidNamespace(HttpError):
    def __init__(self, namespace):

        super().__init__(
            422,
            (
                f"Invalid namespace '{namespace}'. "
                f"Examples: "
                f"'core', 'business.assets'"
            ),
        )
