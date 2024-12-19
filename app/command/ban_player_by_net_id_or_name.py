import asyncio
import re

from unidecode import unidecode

from app.service.listplayers import ListPlayers
from app.service.ban import Ban
from app.service.say import Say

class BanPlayerByNetIdOrName:
    async def __ban_player(self, player, reason):
        message = f"O jogador {player.name} foi \n banido por motivo de:\n{reason}."

        await Say().run(message)
        await asyncio.sleep(3)
        await Ban().run(player.net_id, reason)

    async def _get_player(self, locator_term):
        players = await ListPlayers().run()
        humans = players["humans"]
        sanitized_locator_term = locator_term.split(":")[-1]

        for player in humans:
            if locator_term in player.name.lower() or sanitized_locator_term == player.net_id:
                return player

        return None

    async def run(self, locator_term, reason):
        player = await self._get_player(locator_term)
        sanitized_reason = unidecode(reason).lower()
        sanitized_reason = re.sub(r"\W", "_", sanitized_reason)

        if player:
            await self.__ban_player(player, sanitized_reason)
            return f"Jogador {player.name} banido com sucesso!"

        return f"Termo não encontrado: {locator_term}"
