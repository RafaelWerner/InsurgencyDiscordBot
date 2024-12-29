from app.job.base import BaseJob
from app.command.kick_player_by_net_id_or_name import KickPlayerByNetIdOrName

class KickPlayerJob(BaseJob):
    def __init__(self, interaction, locator_term, reason):
        super().__init__(interaction)
        self.locator_term = locator_term
        self.reason = reason

    def __str__(self):
        return f"KickPlayerJob: {self.locator_term} {self.reason}"

    async def process(self):
        return await KickPlayerByNetIdOrName().run(self.locator_term, self.reason)

