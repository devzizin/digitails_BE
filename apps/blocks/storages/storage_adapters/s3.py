import boto3
from botocore.exceptions import ClientError

from apps.blocks.storages.enums import StorageProvider
from apps.blocks.storages.models import DriveConnection
from apps.blocks.storages.storage_adapters.base import BaseStorageAdapter


class S3Adapter(BaseStorageAdapter):
    """
    S3 / MinIO storage adapter.
    """

    def __init__(self, connection: DriveConnection):
        cfg = connection.metadata

        self.client = boto3.client(
            StorageProvider.S3,
            aws_access_key_id=connection.access_key,
            aws_secret_access_key=connection.secret_key,
            endpoint_url=cfg.get("endpoint_url"),
            region_name=cfg.get("region"),
        )

        self.bucket = cfg.get("bucket")


    def upload(self, *, file, key, mime_type):
        key = self._validated_key(key)
        self.client.upload_fileobj(
            file,
            self.bucket,
            key,
            ExtraArgs={"ContentType": mime_type},
        )

    def generate_download_url(self, *, key: str, expires: int) -> str:
        key = self._validated_key(key)
        return self.client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": self.bucket,
                "Key": key,
            },
            ExpiresIn=expires,
        )

    def generate_upload_url(self, *, key: str, mime_type: str, expires: int) -> str:
        key = self._validated_key(key)
        return self.client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": self.bucket,
                "Key": key,
                "ContentType": mime_type,
            },
            ExpiresIn=expires,
        )

    def delete(self, *, key: str) -> None:
        key = self._validated_key(key)
        self.client.delete_object(
            Bucket=self.bucket,
            Key=key,
        )

    def exists(self, *, key: str) -> bool:
        key = self._validated_key(key)
        try:
            self.client.head_object(Bucket=self.bucket, Key=key)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            raise

    def copy(self, *, source_key: str, destination_key: str) -> None:
        source_key = self._validated_key(source_key)
        destination_key = self._validated_key(destination_key)
        self.client.copy_object(
            Bucket=self.bucket,
            CopySource={
                "Bucket": self.bucket,
                "Key": source_key,
            },
            Key=destination_key,
        )

    def list_objects(self, *, prefix: str = "", max_keys: int = 1000):
        prefix = prefix.strip().strip("/")
        if prefix:
            prefix = f"{prefix}/"

        paginator = self.client.get_paginator("list_objects_v2")
        for page in paginator.paginate(
            Bucket=self.bucket,
            Prefix=prefix,
            PaginationConfig={"MaxItems": max_keys},
        ):
            for item in page.get("Contents", []):
                key = item.get("Key", "")
                if not key or key.endswith("/"):
                    continue
                yield {
                    "key": key,
                    "size": item.get("Size", 0),
                    "etag": item.get("ETag", "").strip('"'),
                    "mime_type": None,
                }
