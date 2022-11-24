from nameko.rpc import rpc
from sciuromorpha_core import model, static as S


class Task:
    name = "task"

    @rpc
    def create(self):
        pass

    @rpc
    def update(self):
        pass

    @rpc
    def remove(self):
        pass

    @rpc
    def clean_finished(self):
        pass