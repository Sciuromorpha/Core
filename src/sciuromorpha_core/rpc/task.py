from uuid import UUID
from typing import Any, Union

from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import joinedload, sessionmaker
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
from sciuromorpha_core.mq_schema import task_rpc, task_topic


@broker.subscriber("task.create", task_rpc)
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


@broker.subscriber("task.update", task_rpc)
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

    await broker.publish(
        message=result, routing_key="task.updated", exchange=task_topic
    )
    return result


@broker.subscriber("task.get", task_rpc)
async def get_task(
    task_id: Union[str, UUID],
    db_session: sessionmaker = Context(),
) -> Union[dict, None]:
    with db_session.begin() as session:
        task = session.get(model.Task, task_id)

        if task is None:
            return None

        return task.to_dict()


@broker.subscriber("task.get-one", task_rpc)
async def get_one(
    worker: str,
    status: str = "pending",
    db_session: sessionmaker = Context(),
) -> Union[dict, None]:
    with db_session.begin() as session:
        task = session.execute(
            select(model.Task).where(
                (model.Task.worker == worker) & (model.Task.status == status)
            )
        ).first()

        if task is None:
            return None

        return task.to_dict()


@broker.subscriber("task.remove", task_rpc)
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
            stmt = delete(model.Task).where(model.Task.id == task_id)

        elif isinstance(task_id, list):
            # Delete tasks by ID.
            stmt = delete(model.Task).where(model.Task.id.in_(task_id))

        return session.execute(stmt).scalar()


@broker.subscriber("task.clean", task_rpc)
async def clean_task(
    worker: str,
    status: str = "finish",
    db_session: sessionmaker = Context(),
):
    with db_session.begin() as session:
        stmt = delete(model.Task).where(
            (model.Task.worker == worker) & (model.Task.status == status)
        )

        return session.execute(stmt).scalar()
