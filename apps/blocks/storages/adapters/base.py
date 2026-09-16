from abc import ABC, abstractmethod
from typing import BinaryIO

from apps.blocks.storages.security.storage_key_validation import validate_storage_key


class BaseStorageAdapter(ABC):

    def _validated_key(self, key: str) -> str:
        return validate_storage_key(key)

    @abstractmethod
    def upload(
        self,
        *,
        file: BinaryIO,
        key: str,
        mime_type: str,
    ) -> None:
        pass

    @abstractmethod
    def generate_download_url(
        self,
        *,
        key: str,
        expires: int,
    ) -> str:
        pass

    @abstractmethod
    def generate_upload_url(
        self,
        *,
        key: str,
        mime_type: str,
        expires: int,
    ) -> str:
        pass

    @abstractmethod
    def delete(self, *, key: str) -> None:
        pass

    @abstractmethod
    def exists(self, *, key: str) -> bool:
        pass

    @abstractmethod
    def copy(
        self,
        *,
        source_key: str,
        destination_key: str,
    ) -> None:
        pass