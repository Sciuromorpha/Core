import copy
from uuid import UUID
from typing import Any, Union

from nameko.rpc import rpc
from nameko.events import EventDispatcher

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.dialects.postgresql import insert

from sciuromorpha_core.db.session import SessionFactory
from sciuromorpha_core import model, static as S


class Meta:
    name = "meta"

    dispatch = EventDispatcher()

    @classmethod
    def clone_meta_data(cls, meta: model.Meta):
        clone = copy.copy(meta.data)

        # Ensure meta.data is dict.
        if not isinstance(clone, dict):
            clone = {S.META_KEY_STUB: clone} if clone is not None else {}

        return clone

    @classmethod
    def merge_meta_data(cls, origin: dict, append: dict):
        # Merge append dict to origin.
        # Not deep merge right now.

        for key, value in append.items():
            if value is not None:
                origin[key] = append[key]
            else:
                try:
                    del origin[key]
                except KeyError:
                    pass

        return origin

    @classmethod
    def clone_process_tag(cls, meta: model.Meta):
        try:
            result = set(meta.process_tag)
        except TypeError:
            result = {meta.process_tag} if meta.process_tag is not None else set()

        return result

    @rpc
    def create(self, meta_data: dict):
        # Extract origin_url from meta.
        with SessionFactory.begin() as session:
            # stmt = insert(model.Meta).values(data=metadata, origin_url=origin_url).on_conflict_do_nothing()
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
    def merge(
        self, meta_id: Union[str, UUID], meta_data: dict, process_tag: Union[None, str]
    ):
        with SessionFactory.begin() as session:
            # Try get meta for UPDATE
            meta = session.get(model.Meta, meta_id, with_for_update=True)

            if meta is None:
                # Cannot merge a none
                return None

            clone_meta = Meta.clone_meta_data(meta)
            meta.data = Meta.merge_meta_data(clone_meta, meta_data)
            meta.origin_url = clone_meta.get(S.META_KEY_ORIGIN_URL, None)

            if process_tag is not None:
                clone_tags = Meta.clone_process_tag(meta)
                clone_tags.add(process_tag)
                meta.process_tag = list(clone_tags)

            with session.begin_nested():
                session.add(meta)

            result = meta.to_dict()

        # Publish event to other services.
        self.dispatch("merge", result)
        return result

    @rpc
    def add_process_tag(self, meta_id: Union[str, UUID], tag: str):
        with SessionFactory.begin() as session:
            # Try get meta for UPDATE
            meta = session.get(model.Meta, meta_id, with_for_update=True)

            if meta is None:
                # Cannot merge a none, slient failed.
                return None

            clone_tags = Meta.clone_process_tag(meta)
            clone_tags.add(tag)
            meta.process_tag = list(clone_tags)

            with session.begin_nested():
                session.add(meta)

            result = meta.to_dict()

        return result

    @rpc
    def remove_process_tag(self, meta_id: Union[str, UUID], tag: str):
        with SessionFactory.begin() as session:
            # Try get meta for UPDATE
            meta = session.get(model.Meta, meta_id, with_for_update=True)

            if meta is None:
                # Cannot merge a none, slient failed.
                return None

            clone_tags = Meta.clone_process_tag(meta)

            try:
                clone_tags.remove(tag)
                meta.process_tag = list(clone_tags)
                with session.begin_nested():
                    session.add(meta)

            except KeyError:
                pass

            result = meta.to_dict()

        return result

    @rpc
    def get_by_id(self, id: Union[str, UUID]):
        with SessionFactory.begin() as session:
            meta = session.get(model.Meta, id, options=(joinedload(model.Meta.tasks),))
            return meta.to_dict(rules=("tasks",))

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

    @rpc
    def query_by_process_tag(self, tags: list, offset: int = 0, limit: int = 100):
        if not isinstance(tags, list):
            tags = [tags]

        with SessionFactory.begin() as session:
            stmt = (
                select(model.Meta)
                .where(model.Meta.process_tag.contains(tags))
                .order_by(model.Meta.id)
                .offset(offset)
                .limit(limit)
            )
            result = [row.to_dict() for row in session.execute(stmt).scalars()]

        return result

    @rpc
    def query_without_process_tag(self, tags: list, offset: int = 0, limit: int = 100):
        if not isinstance(tags, list):
            tags = [tags]

        with SessionFactory.begin() as session:
            stmt = (
                select(model.Meta)
                .where(~model.Meta.process_tag.contains(tags))
                .order_by(model.Meta.id)
                .offset(offset)
                .limit(limit)
            )
            result = [row.to_dict() for row in session.execute(stmt).scalars()]

        return result
