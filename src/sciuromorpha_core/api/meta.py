from uuid import UUID
from typing import Any, Union

from nameko.rpc import rpc, RpcProxy
from nameko.events import EventDispatcher

from sqlalchemy import MetaData, select
from sqlalchemy.dialects.postgresql import insert
from sciuromorpha_core.db.session import SessionFactory
from sciuromorpha_core.model import Meta as MetaModel


class Meta:
    name = "meta"

    dispatch = EventDispatcher()

    @rpc
    def create(self, metadata: dict, origin_url: str):
        new_meta = MetaModel(meta=metadata, origin_url=origin_url)
        with SessionFactory.begin() as session:
            # stmt = insert(MetaModel).values(meta=metadata, origin_url=origin_url).on_conflict_do_nothing()
            # session.execute(stmt)
            session.add(new_meta)
            # session.refresh(new_meta)

        self.dispatch("create", new_meta)
        return new_meta

    @rpc
    def merge(self, meta_id: Union[str, UUID], metadata: dict, origin_url: str):
        # Try get meta for UPDATE
        with SessionFactory.begin() as session:
            meta = session.query(MetaModel).filter()

        # Publish event to other services.
        self.dispatch("merge", meta)
        return meta

    @rpc
    def get_by_id(self, id: Union[str, UUID]):
        with SessionFactory.begin() as session:
            # stmt = select(MetaModel).where(MetaModel.id == id)
            # return session.execute(stmt).first()
            meta = session.get(MetaModel, id)
        
        return meta

    @rpc
    def get_by_origin_url(self, url: str):
        pass

    @rpc
    def bulk_get(query: Any, offset: int = 0, limit: int = 100):
        pass
