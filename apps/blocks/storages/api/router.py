from ninja import Router

from apps.blocks.storages.api.connection_router import router as connection_router
from apps.blocks.storages.api.file_router import router as file_router
from apps.blocks.storages.api.folder_router import router as folder_router

storages_router = Router()
storages_router.add_router("/connections", connection_router)
storages_router.add_router("/folders", folder_router)
storages_router.add_router("/files", file_router)

# then in your main api.py: api.add_router("/storages", storages_router)
