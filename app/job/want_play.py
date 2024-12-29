from app.job.base import BaseJob
from app.command.want_play import WantPlay

class WantPlayJob(BaseJob):
    def __str__(self):
        return f"WantPlayJob"

    async def process(self):
        return await WantPlay().run()
