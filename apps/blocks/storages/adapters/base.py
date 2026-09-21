from abc import ABC, abstractmethod
from typing import BinaryIO

from apps.blocks.storages.validators.storage_key_validation import validate_storage_key


class BaseStorageAdapter(ABC):
    """
    Contract every storage backend implements. Only one concrete
    implementation (S3Adapter) exists today -- kept as an ABC + factory
    so a second provider later is additive, not a rewrite.
    """

    def _validated_key(self, key: str) -> str:
        return validate_storage_key(key)

    @abstractmethod
    def upload(self, *, file: BinaryIO, key: str, mime_type: str) -> None: ...

    @abstractmethod
    def generate_download_url(self, *, key: str, expires: int) -> str: ...

    @abstractmethod
    def generate_upload_url(self, *, key: str, mime_type: str, expires: int) -> str: ...

    @abstractmethod
    def delete(self, *, key: str) -> None: ...

    @abstractmethod
    def exists(self, *, key: str) -> bool: ...

    @abstractmethod
    def copy(self, *, source_key: str, destination_key: str) -> None: ...
