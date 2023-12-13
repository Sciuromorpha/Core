import os
import sys
import asyncio
import logging
from typing import Any, Optional, Union
from faststream import Context, apply_types
from faststream.rabbit.annotations import (
    RabbitBroker,
)

from sciuromorpha_core import S, Settings
from sciuromorpha_core.mq_schema import meta_rpc
from uuid import UUID
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


@apply_types(cast=False)
async def create(
    meta: dict[str, Any],
    broker: RabbitBroker,
):
    return await broker.publish(
        meta,
        "meta.create",
        exchange=meta_rpc,
        rpc=True,
    )


@apply_types(cast=False)
async def merge(
    meta: dict[str, Any],
    broker: RabbitBroker,
) -> Union[dict[str, Any], None]:
    return await broker.publish(
        meta,
        "meta.merge",
        exchange=meta_rpc,
        rpc=True,
    )


@apply_types(cast=False)
async def get(
    id: Union[str, UUID],
    broker: RabbitBroker,
    with_tasks: bool = False,
) -> Union[dict[str, Any], None]:
    return await broker.publish(
        {"id": id, "with_tasks": with_tasks},
        "meta.get",
        exchange=meta_rpc,
        rpc=True,
    )
