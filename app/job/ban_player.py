from app.job.base import BaseJob
from app.command.ban_player_by_net_id_or_name import BanPlayerByNetIdOrName

class BanPlayerJob(BaseJob):
    def __init__(self, interaction, locator_term, duration, reason):
        super().__init__(interaction)
        self.locator_term = locator_term
        self.duration = duration
        self.reason = reason

    def __str__(self):
        return f"BanPlayerJob: {self.locator_term} {self.duration} {self.reason}"

    async def process(self):
        return await BanPlayerByNetIdOrName().run(self.locator_term, self.reason)

