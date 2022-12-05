from uuid import UUID
from typing import Any, Union

from nameko.rpc import rpc
from nameko.events import EventHandler, EventDispatcher

class Storage:
    name="storage"

    @rpc
    def get_service_path(self, service_meta: dict)->dict:
        # Generate the service subfolder by the service metadata.
        pass

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
