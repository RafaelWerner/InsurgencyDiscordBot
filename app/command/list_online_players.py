from app.core.manager import Manager
from app.service.listplayers import ListPlayers

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
        print("Online players: ", online_players)

        bot_count = online_players["bots"]
        sorted_humans = sorted(online_players["humans"], key=lambda player: player.score, reverse=True)

        return f"Agora temos [ {len(sorted_humans)} ] jogadores online, jogando contra [ {bot_count} ] bots.\n\n{self.__format_players(sorted_humans)}"
