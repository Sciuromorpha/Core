import copy
from uuid import UUID
from typing import Any, Union

from nameko.rpc import rpc
from nameko.events import EventDispatcher

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from sciuromorpha_core.db.session import SessionFactory
from sciuromorpha_core import model, static as S


class Meta:
    name = "meta"

    dispatch = EventDispatcher()

    @rpc
    def create(self, meta_data: dict):
        # Extract origin_url from meta.
        with SessionFactory.begin() as session:
            # stmt = insert(model.Meta).values(meta=metadata, origin_url=origin_url).on_conflict_do_nothing()
            # session.execute(stmt)
            meta = model.Meta(
                data=meta_data, origin_url=meta_data.get(S.META_KEY_ORIGIN_URL, None)
            )
            with session.begin_nested():
                session.add(meta)

            result = meta.to_dict()

        # Publish event to other services.
        self.dispatch("create", result)
        return result

    @rpc
    def merge(self, meta_id: Union[str, UUID], meta_data: dict):
        # Try get meta for UPDATE
        with SessionFactory.begin() as session:
            meta = session.get(model.Meta, meta_id)

            if meta is None:
                # Cannot merge a none
                return None

            clone_meta = copy.copy(meta.data)

            if clone_meta is not dict:
                # Ensure this metadata is dict.
                clone_meta = (
                    {S.META_KEY_STUB: clone_meta} if clone_meta is not None else {}
                )

            # Not deep merge right now.
            for key, value in meta_data.items():
                if value is not None:
                    clone_meta[key] = meta_data[key]
                else:
                    try:
                        del clone_meta[key]
                    except KeyError:
                        pass

            meta.data = clone_meta
            meta.origin_url = clone_meta.get(S.META_KEY_ORIGIN_URL, None)
            with session.begin_nested():
                session.add(meta)

            result = meta.to_dict()

        # Publish event to other services.
        self.dispatch("merge", result)
        return result

    @rpc
    def get_by_id(self, id: Union[str, UUID]):
        with SessionFactory.begin() as session:
            # stmt = select(model.Meta).where(model.Meta.id == id)
            # return session.execute(stmt).first()
            meta = session.get(model.Meta, id)
            return meta.to_dict()

    @rpc
    def get_by_origin_url(self, url: str):
        with SessionFactory.begin() as session:
            meta = session.execute(
                select(model.Meta).where(model.Meta.origin_url == url)
            ).first()

        return meta.to_dict()

    @rpc
    def query(query: Any, offset: int = 0, limit: int = 100):
        pass
