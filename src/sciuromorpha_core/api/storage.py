from uuid import UUID
from typing import Any, Union
from pathlib import Path

from nameko.rpc import rpc
from nameko.events import EventHandler, EventDispatcher

import sciuromorpha_core.static as S
from sciuromorpha_core.config import config, logger
from sciuromorpha_core.exceptions import ArgumentTypeError

class Storage:
    name="storage"

    @rpc
    def get_service_path(self, service_meta: dict)->dict:
        # Generate the service subfolder by the service metadata.
        # Right now, we just create the service subfolder by the service name, and ignore the instance id.
        logger.info("get_service_path", service_meta)
        service_name = service_meta.get("name", None)

        if type(service_name) is not str:
            raise ArgumentTypeError("service_meta.name need to be a string.")

        storage_path = Path(config[S.CONFIG_SECTION_SCIUROMORPHA]["storage"])

        service_path = storage_path / service_name.lower()

        if not service_path.exists():
            service_path.mkdir(parents=True, exist_ok=True)

        return {
            "storage_path": str(storage_path),
            "service_path": str(service_path),
        }

    @rpc
    def import_document(self, meta_data: dict)-> dict:
        # Import document from exiting file/folder etc.
        pass

    @rpc
    def get_document(self, meta_data: dict)->dict:
        # Calcute and return absoulate path for this metadata.
        return {}

    @rpc
    def get_document_by_id(self, meta_id: Union[str, UUID])->dict:
        pass
