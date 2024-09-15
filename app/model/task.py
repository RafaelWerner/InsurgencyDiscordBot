from app.model.base import BaseModel
from datetime import datetime
from app.service.say import Say

class Task(BaseModel):
    def prepare(self):
        self.interval = 60
        self.last_execution = 0
        self.kind = 'say'


    def current_time(self):
        return int(datetime.now().timestamp())

    def is_time_to_execute(self):
        if self.last_execution == 0:
            return True

        return self.last_execution + self.interval > self.current_time()

    def update_last_execution(self):
        self.last_execution = self.current_time()
