from app.task.factory import TasksFactory
from app.model.task import Task

class Runner:
    def __init__(self):
        self._tasks = []
        tasks = Task().all()

        for task in tasks:
            try:
                self._tasks.append(TasksFactory.create(task))
            except ValueError as e:
                print(f"Erro ao criar processo {task}: {e}")

    async def execute(self):
        for task in self._tasks:
            try:
                await task.execute()
            except Exception as e:
                print(f"Erro executando processo {task}: {e}")
