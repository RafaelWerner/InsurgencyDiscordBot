from app.task.base import BaseTask

from app.service.listplayers import ListPlayers
from app.model.historic import Historic

class SavePlayers(BaseTask):
    async def _process(self):
        actual_players = await ListPlayers().run()
        historic = Historic()

        for player in actual_players['humans']:
            historic.create({'player': player.name, 'plataform_id': player.net_id, 'score': player.score})
