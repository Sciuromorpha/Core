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
async def add_tag(
    meta: dict[str, Any],
    broker: RabbitBroker,
) -> Union[dict[str, Any], None]:
    return await broker.publish(
        meta,
        "meta.addtag",
        exchange=meta_rpc,
        rpc=True,
    )


@apply_types(cast=False)
async def remove_tag(
    meta: dict[str, Any],
    broker: RabbitBroker,
) -> Union[dict[str, Any], None]:
    return await broker.publish(
        meta,
        "meta.removetag",
        exchange=meta_rpc,
        rpc=True,
    )


@apply_types(cast=False)
async def get(
    id: Union[str, UUID],
    broker: RabbitBroker,
    **kwargs,
) -> Union[dict[str, Any], None]:
    return await broker.publish(
        {"id": id, **kwargs},
        "meta.get",
        exchange=meta_rpc,
        rpc=True,
    )


@apply_types(cast=False)
async def get_by_url(
    url: str,
    broker: RabbitBroker,
) -> Union[dict[str, Any], None]:
    return await broker.publish(
        {"url": url},
        "meta.get_by_url",
        exchange=meta_rpc,
        rpc=True,
    )


@apply_types(cast=False)
async def query_by_tag(
    tags: Union[str, list[str]],
    broker: RabbitBroker,
    **kwargs,
) -> list:
    return await broker.publish(
        {
            "tags": tags,
            **kwargs,
        },
        "meta.query-by-tag",
        exchange=meta_rpc,
        rpc=True,
    )


@apply_types(cast=False)
async def query_witout_tag(
    tags: Union[str, list[str]],
    broker: RabbitBroker,
    **kwargs,
) -> list:
    return await broker.publish(
        {"tags": tags, **kwargs},
        "meta.query-without-tag",
        exchange=meta_rpc,
        rpc=True,
    )
