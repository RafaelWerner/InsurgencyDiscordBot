import asyncio
import re

from unidecode import unidecode

from app.service.listplayers import ListPlayers
from app.service.ban import Ban
from app.service.say import Say

class BanPlayerByNetIdOrName:
    async def __ban_player(self, player, duration, reason):
        message = f"O jogador {player.name} foi banido por motivo de: {reason}."

        await Say().run(message)
        await asyncio.sleep(3)
        await Ban().run(player.net_id, duration, reason)

    async def _get_player(self, locator_term):
        players = await ListPlayers().run()
        humans = players["humans"]

        for player in humans:
            if locator_term in player.name.lower() or locator_term == player.net_id:
                return player

        return None

    async def run(self, locator_term, duration, reason):
        player = await self._get_player(locator_term)
        sanitized_reason = unidecode(reason).lower()
        sanitized_reason = re.sub(r"\W", "_", sanitized_reason)

        if player:
            await self.__ban_player(player, duration, sanitized_reason)
            return f"O jogador {player.name} foi banido com sucesso por {duration} minutos!"

        return f"Não encontrei nenhum jogador com {locator_term} no nome ou como id"
