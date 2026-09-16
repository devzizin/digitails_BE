import hashlib
from typing import BinaryIO


def compute_stream_sha256(file: BinaryIO, *, chunk_size: int = 8192) -> str:
    hasher = hashlib.sha256()
    position = file.tell()
    file.seek(0)

    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break
        hasher.update(chunk)

    file.seek(position if position else 0)
    return hasher.hexdigest()
