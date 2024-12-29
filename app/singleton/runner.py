import logging

from app.task.factory import TasksFactory
from app.model.task import Task

class SingletonRunner:
    _instance = None
    _tasks = []
    _jobs = []

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SingletonRunner, cls).__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self._tasks = []
        tasks = Task().all()

        for task in tasks:
            try:
                self._tasks.append(TasksFactory.create(task))
            except ValueError as e:
                self.logger.error(f"Erro ao criar a tarefa {task}: {e}")

    async def schedule(self, job):
        self._jobs.append(job)

    async def execute(self):
        while self._jobs:
            try:
                job = self._jobs.pop(0)
                self.logger.info(f"Executando o job {job}")
                await job.execute()
            except Exception as e:
                self.logger.error(f"Erro executando o job {job}: {e}")

        for task in self._tasks:
            try:
                await task.execute()
            except Exception as e:
                self.logger.error(f"Erro executando a tarefa {task}: {e}")
