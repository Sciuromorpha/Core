from uuid import UUID
from typing import Any, Union

from faststream.rabbit.annotations import (
    Logger,
    Context,
    ContextRepo,
    RabbitMessage,
    RabbitBroker as BrokerAnnotation,
    RabbitProducer,
)
from sqlalchemy.orm import joinedload, sessionmaker

from sciuromorpha_core import model
from sciuromorpha_core.db import session
from sciuromorpha_core.app import app, broker
from sciuromorpha_core.mq_schema import task_rpc, task_topic


@broker.subscriber("create", task_rpc)
@broker.publisher(routing_key="task.created", exchange=task_topic)
async def create(
    worker: str,
    param: Any = None,
    meta_id: Union[str, UUID, None] = None,
    status: str = "pending",
    db_session: sessionmaker = Context(),
) -> dict:
    with db_session.begin() as session:
        task = model.Task(worker=worker, param=param, meta_id=meta_id, status=status)

        with session.begin_nested():
            session.add(task)

        result = task.to_dict()

    return result


@broker.subscriber("update", task_rpc)
async def update(
    task_id: Union[str, UUID],
    broker: BrokerAnnotation,
    worker: str = None,
    param: Any = None,
    meta_id: Union[str, UUID, None] = None,
    status: str = "pending",
    db_session: sessionmaker = Context(),
) -> Union[None, dict]:
    with db_session.begin() as session:
        task = session.get(model.Task, task_id)

        if task is None:
            return None

        if worker is not None:
            task.worker = worker

        if param is not None:
            task.param = param

        if meta_id is not None:
            task.meta_id = meta_id

        task.status = status

        with session.begin_nested():
            session.add(task)

        result = task.to_dict()

    broker.publish(message=result, routing_key="task.updated", exchange=task_topic)
    return result


@broker.subscriber("remove", task_rpc)
async def remove(
    task_id: Union[str, UUID, list],
    db_session: sessionmaker = Context(),
):
    with db_session.begin() as session:
        if isinstance(
            task_id,
            (
                str,
                UUID,
            ),
        ):
            # Delete one task by ID.
            pass

        elif isinstance(task_id, list):
            # Delete tasks by ID.
            pass


async def clean_task():
    pass
