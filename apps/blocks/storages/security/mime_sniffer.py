from apps.blocks.storages.exceptions import StorageFileTypeNotAllowed
from apps.blocks.storages.security.upload_validation import validate_upload_mime_type

_SNIFF_SIGNATURES: tuple[tuple[bytes, str], ...] = (
    (b"%PDF", "application/pdf"),
    (b"\x89PNG\r\n\x1a\n", "image/png"),
    (b"\xff\xd8\xff", "image/jpeg"),
    (b"GIF87a", "image/gif"),
    (b"GIF89a", "image/gif"),
    (b"PK\x03\x04", "application/zip"),
    (b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1", "application/msword"),
    (b"RIFF", "application/octet-stream"),
)

_EXECUTABLE_PREFIXES: tuple[bytes, ...] = (
    b"MZ",
    b"\x7fELF",
)


def detect_mime_from_bytes(data: bytes) -> str | None:
    for signature, mime_type in _SNIFF_SIGNATURES:
        if data.startswith(signature):
            if signature == b"RIFF" and len(data) >= 12 and data[8:12] == b"WEBP":
                return "image/webp"
            return mime_type

    return None


def validate_upload_content(*, head: bytes, declared_mime: str) -> str:
    for prefix in _EXECUTABLE_PREFIXES:
        if head.startswith(prefix):
            raise StorageFileTypeNotAllowed()

    sniffed_mime = detect_mime_from_bytes(head)
    if sniffed_mime:
        validate_upload_mime_type(mime_type=sniffed_mime)
        return sniffed_mime

    return declared_mime


def read_upload_head(file, *, max_bytes: int = 8192) -> bytes:
    position = file.tell()
    file.seek(0)
    head = file.read(max_bytes)
    file.seek(position if position else 0)
    return head
