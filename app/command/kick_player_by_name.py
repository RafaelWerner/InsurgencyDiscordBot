import asyncio

from app.service.server.listplayers import ListPlayers
from app.service.server.kick import Kick
from app.service.server.say import Say

class KickPlayerByName:

    def __init__(self, player_name):
        self.player_name = player_name

    async def __kick_player(self, player):
        message = f"""
            {player.name} você foi kickado por um VIP.
            Torne-se VIP e garanta sua vaga.
        """
        Say(message).run()

        await asyncio.sleep(3)

        Kick(player.id, "entrada_de_um_vip").run()


    def _get_player(self):
        players = ListPlayers().run()

        for player in players:
            if player.name == self.player_name:
                return player

        return None

    async def run(self):
        player = self._get_player()

        if player:
            await self.__kick_player(player)
            return "Jogador kickado com sucesso!"

        return "Jogador não encontrado"
