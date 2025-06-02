from app.job.base import BaseJob
from app.command.list_online_players import ListOnlinePlayers

class ListPlayersJob(BaseJob):
    def __str__(self):
        return f"ListPlayersJob"

    async def process(self):
        return await ListOnlinePlayers().run()