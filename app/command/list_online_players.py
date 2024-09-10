from app.core.manager import Manager
from app.service.server.listplayers import ListPlayers

class ListOnlinePlayers:
    def __init__(self):
        self.__vips = Manager().vips

    def __format_players(self, players):
        return "\n".join([self.__format_player(player) for player in players])

    def __format_player(self, player):
        if self.__vips.is_vip(player.net_id):
            return f"- **{player.name} ({player.score})** : VIP"

        return f"- {player.name} ({player.score})"

    def run(self):
        online_players = ListPlayers().run()

        return f"Agora temos [ {len(online_players)} ] jogadores online\n\n{self.__format_players(online_players)}"
