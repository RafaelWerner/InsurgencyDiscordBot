import random

from app.task.base import BaseTask
from app.service.say import Say

class ServerMessage(BaseTask):
    last_message = None

    async def find_new_message(self):
        while random_message := random.choice(self.data):
            if random_message != self.last_message:
                return random_message

    async def _process(self):
        message = await self.find_new_message()

        self.last_message = message
        await Say().run(message)
