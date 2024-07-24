from uuid import UUID
from typing import Any, Union
from faststream import apply_types
from faststream.rabbit.annotations import RabbitBroker

from sciuromorpha_core.mq_schema import task_rpc


@apply_types(cast=False)
async def create(
    task: Any,
    broker: RabbitBroker,
) -> Union[dict, None]:
    """
    Create a task.
    task params:
      worker: str,
      param: Any,
      meta_id: Union[str, UUID, None] = None,
      status: TASK_STATUS = TASK_STATUS.PENDING,
    return: dict, or None if failed.
    """
    return await broker.publish(
        task,
        "task.create",
        exchange=task_rpc,
        rpc=True,
    )


@apply_types(cast=False)
async def update(
    task: Any,
    broker: RabbitBroker,
) -> Union[dict, None]:
    """
    Update existing task.
    task params:
      id: UUID,
      status: TASK_STATUS,
      result: Any,
    return: dict, or None if failed.
    """
    return await broker.publish(
        task,
        "task.update",
        exchange=task_rpc,
        rpc=True,
    )
