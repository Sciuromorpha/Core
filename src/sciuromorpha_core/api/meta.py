from nameko.rpc import rpc, RpcProxy
from nameko.events import EventDispatcher
from uuid import UUID
from typing import Any, Union

class Meta:
    name = 'meta'

    dispatch = EventDispatcher()

    @rpc
    def create(self, metadata: dict, origin_url: str):
        self.dispatch("create", metadata)

    @rpc
    def merge(self, meta_id: Union[str, UUID], metadata: dict, origin_url: str):
        # Try get meta line for UPDATE

        # If NOT exist, create it instead.

        # Publish event to other services.
        self.dispatch("merge", metadata)

    @rpc
    def get_by_id(self, id: Union[str, UUID]):
        pass

    @rpc
    def get_by_origin_url(self, url: str):
        pass

    @rpc
    def bulk_get(query: Any, offset:int = 0, limit: int = 100):
        pass