from ninja.errors import HttpError


class CompanyException(HttpError):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(status_code, message)


class CompanyNotFound(CompanyException):
    def __init__(self):
        super().__init__("Company not found", 404)


class CompanyAlreadyExists(HttpError):

    def __init__(
        self,
        message: str = "Company already exists.",
    ):
        super().__init__(
            400,
            message,
        )

class InvalidCompanyData(CompanyException):
    def __init__(self, message="Invalid company data"):
        super().__init__(message, 422)
