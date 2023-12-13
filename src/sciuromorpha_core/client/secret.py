from uuid import UUID
from typing import Any, Union
from faststream import apply_types
from faststream.rabbit.annotations import RabbitBroker

from sciuromorpha_core.mq_schema import secret_rpc


@apply_types(cast=False)
async def put(
    service: str,
    key: str,
    data: Any,
    broker: RabbitBroker,
) -> int:
    """
    Put a data(json like) in secret store.
    """
    return await broker.publish(
        {
            "service": service,
            "key": key,
            "data": data,
        },
        "secret.put",
        exchange=secret_rpc,
        rpc=True,
    )


@apply_types(cast=False)
async def get(
    service: str,
    key: str,
    broker: RabbitBroker,
) -> Union[dict[str, Any], None]:
    """
    Get a secret by service&key.
    """
    return await broker.publish(
        {
            "service": service,
            "key": key,
        },
        "secret.get",
        exchange=secret_rpc,
        rpc=True,
    )


@apply_types(cast=False)
async def get_by_id(
    id: int,
    broker: RabbitBroker,
) -> Union[dict[str, Any], None]:
    """
    Get a secret by id.
    """
    return await broker.publish(
        {
            "id": id,
        },
        "secret.get-by-id",
        exchange=secret_rpc,
        rpc=True,
    )


@apply_types(cast=False)
async def delete(
    service: str,
    key: str,
    broker: RabbitBroker,
) -> Any:
    """
    Delete a secret by service&key.
    Return last store data.
    """
    return await broker.publish(
        {
            "service": service,
            "key": key,
        },
        "secret.delete",
        exchange=secret_rpc,
        rpc=True,
    )
