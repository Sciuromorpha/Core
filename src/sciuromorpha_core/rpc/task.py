from uuid import UUID
from typing import Any, Union

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
    ) -> dict:
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
    def update(
        self,
        task_id: Union[str, UUID],
        worker: str = None,
        param: Any = None,
        meta_id: Union[str, UUID, None] = None,
        status: str = "pending",
    ) -> Union[None, dict]:
        with SessionFactory.begin() as session:
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

        self.dispatch("update", result)
        return result

    @rpc
    def remove(self, task_id: Union[str, UUID, list]):
        with SessionFactory.begin() as session:
            if isinstance(task_id, (str, UUID,)):
                # Delete one task by ID.
                pass

            elif isinstance(task_id, list):
                # Delete tasks by ID.
                pass

    @rpc
    def clean_finished(self):
        pass
