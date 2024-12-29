from app.job.base import BaseJob
from app.command.change_map import ChangeMap

class ChangeMapJob(BaseJob):
    def __init__(self, interaction, map_name, team, lightning):
        super().__init__(interaction)
        self.map_name = map_name
        self.team = team
        self.lightning = lightning

    def __str__(self):
        return f"ChangeMapJob {self.map_name} {self.team} {self.lightning}"

    async def process(self):
        return await ChangeMap().run(self.map_name, self.team, self.lightning)
