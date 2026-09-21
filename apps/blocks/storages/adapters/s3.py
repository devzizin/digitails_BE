import boto3
from botocore.exceptions import ClientError

from apps.blocks.storages.adapters.base import BaseStorageAdapter
from apps.blocks.storages.models import StorageConnection


class S3Adapter(BaseStorageAdapter):
    """
    S3 / MinIO storage adapter.

    Reads credentials/config directly off StorageConnection's explicit
    fields (access_key, secret_key, endpoint_url, region, bucket) --
    no metadata JSON blob, since there's only one provider shape to
    support right now.
    """

    def __init__(self, connection: StorageConnection):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=connection.access_key,
            aws_secret_access_key=connection.secret_key,
            endpoint_url=connection.endpoint_url or None,
            region_name=connection.region or None,
        )
        self.bucket = connection.bucket

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
            Params={"Bucket": self.bucket, "Key": key},
            ExpiresIn=expires,
        )

    def generate_upload_url(self, *, key: str, mime_type: str, expires: int) -> str:
        key = self._validated_key(key)
        return self.client.generate_presigned_url(
            "put_object",
            Params={"Bucket": self.bucket, "Key": key, "ContentType": mime_type},
            ExpiresIn=expires,
        )

    def delete(self, *, key: str) -> None:
        key = self._validated_key(key)
        self.client.delete_object(Bucket=self.bucket, Key=key)

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
            CopySource={"Bucket": self.bucket, "Key": source_key},
            Key=destination_key,
        )
