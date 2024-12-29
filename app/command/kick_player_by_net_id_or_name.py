import asyncio
import re

from unidecode import unidecode

from app.service.listplayers import ListPlayers
from app.service.kick import Kick
from app.service.say import Say

class KickPlayerByNetIdOrName:
    async def __kick_player(self, player, reason):
        message = f"{player.name} você sera kickado pelo \nmotivo de: {reason}."

        await Say().run(message)
        await asyncio.sleep(3)
        await Kick().run(player.net_id, reason)

    async def _get_player(self, locator_term):
        players = await ListPlayers().run()
        humans = players["humans"]

        for player in humans:
            if locator_term in player.name.lower() or locator_term == player.net_id:
                return player

        return None

    async def run(self, locator_term, reason):
        player = await self._get_player(locator_term)
        sanitized_reason = unidecode(reason).lower()
        sanitized_reason = re.sub(r"\W", "_", sanitized_reason)

        if player:
            await self.__kick_player(player, sanitized_reason)
            return f"O jogador {player.name} foi expuso com sucesso!"

        return f"Não encontrei nenhum jogador com {locator_term} no nome ou como id"
