from typing import Any, Union

from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload, sessionmaker
from sqlalchemy.dialects.postgresql import insert
from faststream.rabbit.annotations import (
    Context,
)

from sciuromorpha_core import model
from sciuromorpha_core.app import broker
from sciuromorpha_core.mq_schema import secret_rpc


@broker.subscriber("secret.put", secret_rpc)
async def secret_put(
    service: str,
    key: str,
    data: Any,
    db_session: sessionmaker = Context(),
) -> int:
    # Insert or update secret data, and return id of the row.
    with db_session.begin() as session:
        stmt = insert(model.Secret).values(
            service=service,
            key=key,
            data=data,
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=["service", "key"], set_=dict(data=stmt.excluded.data)
        )

        result = session.execute(stmt)
        return result.returned_defaults[0]


@broker.subscriber("secret.get-by-id", secret_rpc)
async def secret_get_by_id(
    id: int,
    db_session: sessionmaker = Context(),
) -> Union[dict, None]:
    with db_session.begin() as session:
        secret = session.get(model.Secret, id, with_for_update=False)

        if secret is None:
            return None

        return secret.to_dict()


@broker.subscriber("secret.get", secret_rpc)
async def secret_get(
    service: str,
    key: str,
    db_session: sessionmaker = Context(),
) -> Union[dict, None]:
    # Fetch secret data by service name & secret key.

    with db_session.begin() as session:
        stmt = (
            select(model.Secret)
            .where((model.Secret.service == service) & (model.Secret.key == key))
            .limit(1)
        )

        result = session.execute(stmt).scalar()

        if result is None:
            return None

        return result.to_dict()


@broker.subscriber("secret.delete", secret_rpc)
async def secret_delete(
    service: str,
    key: str,
    db_session: sessionmaker = Context(),
) -> Any:
    # Delete a secret data by service name @ secret key.
    # It will return the content of data if it exist,
    # Otherwise return none.
    with db_session.begin() as session:
        stmt = (
            delete(model.Secret)
            .where((model.Secret.service == service) & (model.Secret.key == key))
            .returning(model.Secret.data)
        )

        result = session.execute(stmt).scalar()

        return result
