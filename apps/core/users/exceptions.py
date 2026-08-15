from ninja.errors import HttpError


class UserException(HttpError):
    def __init__(
        self,
        message: str,
        status_code: int = 400,
    ):
        super().__init__(
            status_code,
            message,
        )


class UserNotFound(UserException):
    def __init__(self):
        super().__init__(
            "User not found",
            404,
        )


class InvalidCredentials(UserException):
    def __init__(self):
        super().__init__(
            "Invalid credentials",
            401,
        )


class UserInactive(UserException):
    def __init__(self):
        super().__init__(
            "User account is inactive",
            401,
        )


class Unauthorized(UserException):
    def __init__(self):
        super().__init__(
            "Authentication required",
            401,
        )


class InvalidRefreshToken(UserException):
    def __init__(self):
        super().__init__(
            "Invalid refresh token",
            401,
        )


class MissingRefreshToken(UserException):
    def __init__(self):
        super().__init__(
            "Refresh token is missing",
            401,
        )


class InvalidAccessToken(UserException):
    def __init__(self):
        super().__init__(
            "Invalid access token",
            401,
        )


class ExpiredAccessToken(UserException):
    def __init__(self):
        super().__init__(
            "Access token expired",
            401,
        )


class SessionExpired(UserException):
    def __init__(self):
        super().__init__(
            "Session expired",
            401,
        )


class SessionRevoked(UserException):
    def __init__(self):
        super().__init__(
            "Session revoked",
            401,
        )


class EmailAlreadyExists(UserException):
    def __init__(self):
        super().__init__(
            "User with this email already exists",
            400,
        )


class UsernameAlreadyExists(UserException):
    def __init__(self):
        super().__init__(
            "User with this username already exists",
            400,
        )


class UserCreationFailed(UserException):
    def __init__(self):
        super().__init__(
            "Unable to create user",
            400,
        )


class InvalidOldPassword(UserException):
    def __init__(self):
        super().__init__(
            "Old password is incorrect",
            400,
        )


class InvalidPassword(UserException):
    def __init__(self, message):
        super().__init__(message, 400)


class UserCompanyAccessDenied(UserException):
    def __init__(self):
        super().__init__(
            "User does not belong to this company",
            403,
        )


class InvalidTenant(UserException):
    def __init__(self):
        super().__init__(
            "Invalid tenant",
            401,
        )


class TooManyLoginAttempts(UserException):
    def __init__(self):
        super().__init__(
            "Too many login attempts",
            429,
        )


class SuspiciousAuthentication(UserException):
    def __init__(self):
        super().__init__(
            "Suspicious authentication activity detected",
            403,
        )



class UserAlreadyInCompany(UserException):
    def __init__(self):
        super().__init__(
            "User already belongs to this company",
            400,
        )


class UserValidationError(UserException):
    def __init__(self, messages):

        if isinstance(messages, dict):
            formatted = []

            for field, errors in messages.items():
                for error in errors:
                    formatted.append(f"{field}: {error}")

            message = "; ".join(formatted)

        elif isinstance(messages, list):
            message = "; ".join(messages)

        else:
            message = str(messages)

        super().__init__(
            message,
            422,
        )


class InvitationAlreadyExists(UserException):
    def __init__(self):
        super().__init__(
            "Active invitation already exists",
            400,
        )


class InvitationNotFound(UserException):
    def __init__(self):
        super().__init__(
            "Invitation not found",
            404,
        )

class InvalidToken(UserException):
    def __init__(self):
        super().__init__(
            "Invalid token",
            400,
        )


class TokenExpired(UserException):
    def __init__(self):
        super().__init__(
            "Token expired",
            400,
        )


class TokenRevoked(UserException):
    def __init__(self):
        super().__init__(
            "Token revoked",
            400,
        )


class TokenAlreadyUsed(UserException):
    def __init__(self):
        super().__init__(
            "Token already used",
            400,
        )



