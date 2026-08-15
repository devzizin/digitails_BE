from ninja.errors import HttpError


class AssetException(HttpError):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(status_code, message)


class AssetNotFound(AssetException):
    def __init__(self):
        super().__init__("Asset not found", 404)


class AssetTypeNotFound(AssetException):
    def __init__(self):
        super().__init__("Asset type not found", 404)


class TagNotFound(AssetException):
    def __init__(self):
        super().__init__("One or more tags not found", 404)


class AssetCodeAlreadyExists(AssetException):
    def __init__(self):
        super().__init__("Asset with this code already exists", 400)