from uuid import UUID
from typing import Any, Union

from nameko.rpc import rpc
from nameko.events import EventDispatcher

from sciuromorpha_core import model, static as S
from sciuromorpha_core.db.session import SessionFactory


class Task:
    name = "task"

    dispatch = EventDispatcher()

    @rpc
    def create(
        self,
        worker: str,
        param: Any = None,
        meta_id: Union[str, UUID, None] = None,
        status: str = "pending",
    ):
        with SessionFactory.begin() as session:
            task = model.Task(
                worker=worker, param=param, meta_id=meta_id, status=status
            )

            with session.begin_nested():
                session.add(task)

            result = task.to_dict()

        self.dispatch("create", result)
        return result

    @rpc
    def update(self):
        pass

    @rpc
    def remove(self):
        pass

    @rpc
    def clean_finished(self):
        pass
