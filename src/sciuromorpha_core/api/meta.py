from uuid import UUID
from typing import Any, Union

from nameko.rpc import rpc, RpcProxy
from nameko.events import EventDispatcher

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.dialects.postgresql import insert

from sciuromorpha_core.db.session import SessionFactory
from sciuromorpha_core.model import Meta as MetaModel


class Meta:
    name = "meta"

    dispatch = EventDispatcher()

    @rpc
    def create(self, metadata: dict, origin_url: str):
        meta = MetaModel(meta=metadata, origin_url=origin_url)
        with SessionFactory.begin() as session:
            # stmt = insert(MetaModel).values(meta=metadata, origin_url=origin_url).on_conflict_do_nothing()
            # session.execute(stmt)
            session.add(meta)

        # Publish event to other services.
        self.dispatch("create", meta)
        return meta

    @rpc
    def merge(self, meta_id: Union[str, UUID], metadata: dict, origin_url):
        # Try get meta for UPDATE
        with SessionFactory.begin() as session:
            try:
                meta = (
                    session.query(MetaModel)
                    .filter(
                        (MetaModel.id == meta_id) | (MetaModel.origin_url == origin_url)
                    )
                    .with_for_update()
                    .one()
                )
                
            except NoResultFound:
                session.rollback()
                return self.create(metadata=metadata, origin_url=origin_url)
            except MultipleResultsFound:
                pass

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
