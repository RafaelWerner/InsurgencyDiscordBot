import json
from datetime import datetime

class BaseTask():
    def __init__(self, interval = 60, data = '{}'):
        self.interval = int(interval)
        self.data = json.loads(data)
        self._set_next_execution()

    def _current_time(self):
        return int(datetime.now().timestamp())

    def _is_time_to_execute(self):
        return self.next_execution <= self._current_time()

    def _set_next_execution(self):
        self.next_execution = self._current_time() + self.interval

    async def _process(self):
        raise NotImplementedError("Método process não implementado")

    async def execute(self):
        if not self._is_time_to_execute():
            return False

        self._set_next_execution()
        await self._process()

        return True


