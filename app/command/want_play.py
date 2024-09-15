import random
import asyncio

from app.core.manager import Manager
from app.service.listplayers import ListPlayers
from app.service.say import Say
from app.service.kick import Kick

class WantPlay:
    SLOTS_AMOUNT = 12
    MAX_TRIES = 12

    def __randomize(self, players):
        tries = 0
        while tries < self.MAX_TRIES:
            tries += 1
            chosen = random.choice(players)

            if not Manager().vips.is_vip(chosen.id):
                return chosen

        raise ValueError("Não foi possível encontrar um jogador para ser removido")

    async def __kick_player(self, player):
        message = f"""
            Um VIP está tentando entrar no servidor.
            {player.name}, você será kickado
            para a entrada dele.
            Torne-se VIP e garanta sua vaga.
        """
        Say(message).run()

        await asyncio.sleep(2)

        Kick(player.id, "entrada_de_um_vip").run()

    async def __make_room(self, players):
        try:
            player = self.__randomize(players)
            await self.__kick_player(player)
            return "Liberei uma vaga para você, divirta-se!"
        except ValueError as err:
            return str(err)

    async def process(self):
        online_players = ListPlayers().run()["humans"]

        if len(online_players) < self.SLOTS_AMOUNT:
           return f"Temos {self.SLOTS_AMOUNT - len(online_players)} vagas disponíveis, pode entrar!"

        return await self.__make_room(online_players)

    async def run(self, discord_id):
        self.discord_id = discord_id
        return await self.process()
