from typing import Any, Union

from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload, sessionmaker
from sqlalchemy.dialects.postgresql import insert
from faststream.rabbit.annotations import (
    Logger,
    Context,
    ContextRepo,
    RabbitMessage,
    RabbitBroker as BrokerAnnotation,
    RabbitProducer,
)

from sciuromorpha_core import model
from sciuromorpha_core.db import session
from sciuromorpha_core.app import app, broker
from sciuromorpha_core.exceptions import ArgumentMissingError
from .mq_schema import secret_rpc


@broker.subscriber("put", secret_rpc)
async def put(
    secret_meta: dict,
    db_session: sessionmaker = Context(),
) -> int:
    # Insert or update secret data, and return id of the row.

    # Params check.
    # TODO: Use schema or Pydantic to check.
    if secret_meta.get("name", None) is None or secret_meta.get("key", None) is None:
        raise ArgumentMissingError(
            "secret_meta need both name&key exists and should not be None."
        )

    with db_session.begin() as session:
        data = secret_meta.get("data", None)
        stmt = insert(model.Secret).values(
            service=secret_meta["name"],
            key=secret_meta["key"],
            data=data,
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=["service", "key"], set_=dict(data=stmt.excluded.data)
        )
        result = session.execute(stmt)

    return result.returned_defaults[0]


@broker.subscriber("get-by-id", secret_rpc)
async def get_by_id(
    secret_id: int,
    db_session: sessionmaker = Context(),
) -> Union[dict, None]:
    with db_session.begin() as session:
        secret = session.get(model.Secret, secret_id, with_for_update=False)

        if secret is None:
            return None

        result = secret.to_dict()

    return result


@broker.subscriber("get", secret_rpc)
async def get(
    secret_meta: dict[str, str],
    db_session: sessionmaker = Context(),
) -> Union[dict, None]:
    # Fetch secret data by service name & secret key.

    with db_session.begin() as session:
        stmt = select(model.Secret).where(
            (model.Secret.service == secret_meta["name"])
            & (model.Secret.key == secret_meta["key"])
        )

        result = session.execute(stmt).scalar()

        if result is None:
            return None

        result = result.to_dict()

    return result


@broker.subscriber("delete", secret_rpc)
async def delete(
    secret_meta: dict,
    db_session: sessionmaker = Context(),
) -> Union[dict, None]:
    # Delete a secret data by service name @ secret key.
    # It will return the content of row if it exist,
    # Otherwise return none.
    with db_session.begin() as session:
        stmt = delete(model.Secret).where(
            (model.Secret.service == secret_meta["name"])
            & (model.Secret.key == secret_meta["key"])
        )

        result = session.execute(stmt).scalar()

        if result is None:
            return result

        return result.returned_defaults
