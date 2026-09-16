from apps.blocks.storages.exceptions import StorageConnectionRequired
from apps.blocks.storages.models import StorageConnection
from apps.blocks.storages.selectors.connection_selectors import get_default_connection


class StorageConnectionResolver:
    """
    Single-tier resolver: always the tenant's default connection.

    No explicit connection_id override and no per-entity blueprint yet
    (unlike Drive's 3-level resolve()) -- add those only if the client
    actually needs multiple connections per tenant later.
    """

    @staticmethod
    def resolve() -> StorageConnection:
        connection = get_default_connection()

        if not connection:
            raise StorageConnectionRequired()

        return connection
