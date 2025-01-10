from app.service.listplayers import ListPlayers
from app.singleton.users import SingletonUsers

class ListOnlinePlayers:
    async def __format_players(self, players):
        return "\n".join([await self.__format_player(player) for player in players])

    async def __format_player(self, player):

        if await SingletonUsers().is_admin(player.net_id):
            return f"- [2;35m{player.name}[0m ({player.score})"

        return f"- {player.name} ({player.score}) [ {player.net_id} ]"

    async def run(self):
        online_players = await ListPlayers().run()

        bot_count = online_players["bots"]
        sorted_humans = sorted(online_players["humans"], key=lambda player: player.score, reverse=True)

        return f"```ansi\nAgora temos [ {len(sorted_humans)} ] jogadores online, jogando contra [ {bot_count} ] bots.\n\n{await self.__format_players(sorted_humans)}\n```"
