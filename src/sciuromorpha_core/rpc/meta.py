import copy
from uuid import UUID
from typing import Any, Union

from sqlalchemy import select
from sqlalchemy.orm import joinedload, sessionmaker
from sqlalchemy.dialects.postgresql import insert

from faststream.rabbit.annotations import (
    Logger, Context, ContextRepo, RabbitMessage,
    RabbitBroker as BrokerAnnotation, RabbitProducer, NoCast,
)

from sciuromorpha_core import model, static as S
from sciuromorpha_core.app import broker


def clone_meta_data(meta: model.Meta):
    clone = copy.copy(meta.data)

    # Ensure meta.data is dict.
    if not isinstance(clone, dict):
        clone = {S.META_KEY_STUB: clone} if clone is not None else {}

    return clone


def merge_meta_data(origin: dict, append: dict):
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


def clone_process_tag(meta: model.Meta):
    try:
        result = set(meta.process_tag)
    except TypeError:
        result = {meta.process_tag} if meta.process_tag is not None else set()

    return result


@broker.subscriber("core-meta-create")
@broker.publisher("meta-created")
def create(
    meta: dict,
    db_session: sessionmaker = Context(),
):
    # Extract origin_url from meta.
    with db_session.begin() as session:
        # stmt = insert(model.Meta).values(data=metadata, origin_url=origin_url).on_conflict_do_nothing()
        # session.execute(stmt)
        meta = model.Meta(
            data=meta, origin_url=meta.get(S.META_KEY_ORIGIN_URL, None)
        )
        with session.begin_nested():
            session.add(meta)

    return meta.to_dict()


@broker.subscriber("core-meta-merge")
@broker.publisher("meta-updated")
def merge(
    meta_id: Union[str, UUID],
    meta: dict,
    process_tag: Union[None, str] = None,
    db_session: sessionmaker = Context(),
):
    with db_session.begin() as session:
        # Try get meta for UPDATE
        meta = session.get(model.Meta, meta_id, with_for_update=True)

        if meta is None:
            # Cannot merge to not exist meta
            return None

        clone_meta = clone_meta_data(meta)
        meta.data = merge_meta_data(clone_meta, meta)
        meta.origin_url = clone_meta.get(S.META_KEY_ORIGIN_URL, None)

        if process_tag is not None:
            clone_tags = clone_process_tag(meta)
            clone_tags.add(process_tag)
            meta.process_tag = list(clone_tags)

        with session.begin_nested():
            session.add(meta)

    return meta.to_dict()


@broker.subscriber("core-meta-addtag")
def add_process_tag(
    meta_id: Union[str, UUID], tag: str,
    db_session: sessionmaker = Context(),
):
    with db_session.begin() as session:
        # Try get meta for UPDATE
        meta = session.get(model.Meta, meta_id, with_for_update=True)

        if meta is None:
            # Cannot merge a none, slient failed.
            return None

        clone_tags = clone_process_tag(meta)
        clone_tags.add(tag)
        meta.process_tag = list(clone_tags)

        with session.begin_nested():
            session.add(meta)

    return meta.to_dict()


@broker.subscriber("core-meta-removetag")
def remove_process_tag(meta_id: Union[str, UUID], tag: str,
                       db_session: sessionmaker = Context(),
                       ):
    with db_session.begin() as session:
        # Try get meta for UPDATE
        meta = session.get(model.Meta, meta_id, with_for_update=True)

        if meta is None:
            # Cannot merge a none, slient failed.
            return None

        clone_tags = clone_process_tag(meta)

        try:
            clone_tags.remove(tag)
            meta.process_tag = list(clone_tags)
            with session.begin_nested():
                session.add(meta)

        except KeyError:
            pass

        result = meta.to_dict()

    return result


@broker.subscriber("core-meta-get-byid")
def get_by_id(
    id: Union[str, UUID],
    with_tasks: bool = False,
    db_session: sessionmaker = Context(),
) -> Union[model.Meta, None]:
    with db_session.begin() as session:
        if with_tasks:
            meta = session.get(model.Meta, id, options=(
                joinedload(model.Meta.tasks),))
            if meta is None:
                return None
            result = meta.to_dict(rules=("tasks",))
        else:
            meta = session.get(model.Meta, id)
            if meta is None:
                return None
            result = meta.to_dict()

    return result


@broker.subscriber("core-meta-get-byurl")
def get_by_origin_url(
    url: str,
    db_session: sessionmaker = Context(),

) -> Union[model.Meta, None]:
    with db_session.begin() as session:
        meta = session.execute(
            select(model.Meta).where(model.Meta.origin_url == url)
        ).first()
        if meta is None:
            return None
        result = meta.to_dict()

    return result


@broker.subscriber("core-meta-query-bytag")
def query_by_process_tag(
    tags: [str, list],
    offset: int = 0, limit: int = 100,
    db_session: sessionmaker = Context(),

) -> list:
    if not isinstance(tags, list):
        tags = [tags]

    with db_session.begin() as session:
        stmt = (
            select(model.Meta)
            .where(model.Meta.process_tag.contains(tags))
            .order_by(model.Meta.id)
            .offset(offset)
            .limit(limit)
        )
        result = [row.to_dict() for row in session.execute(stmt).scalars()]

    return result


@broker.subscriber("core-meta-query-withouttag")
def query_without_process_tag(
    tags: [str, list], offset: int = 0, limit: int = 100,
    db_session: sessionmaker = Context(),
):
    if not isinstance(tags, list):
        tags = [tags]

    with db_session.begin() as session:
        stmt = (
            select(model.Meta)
            .where(~model.Meta.process_tag.contains(tags))
            .order_by(model.Meta.id)
            .offset(offset)
            .limit(limit)
        )
        result = [row.to_dict() for row in session.execute(stmt).scalars()]

    return result
