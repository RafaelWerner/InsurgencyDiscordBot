from app.service.server.base import BaseServer
from app.model.player import Player

class ListPlayers(BaseServer):
    def __parse_net_id(self, net_id):
        return net_id.split(":")[1].strip()

    def __parse_score(self, score):
        try:
            return int(score)
        except ValueError:
            return 0

    def __parse_player(self, values, offset):
        return Player(
            **{
                "id": values[offset].strip(),
                "name": values[offset + 1].strip(),
                "net_id": self.__parse_net_id(values[offset + 2]),
                "ip": values[offset + 3].strip(),
                "score": self.__parse_score(values[offset + 4].strip())
            }
        )

    def __parse_response(self, response):
        print(f"Response: {response}")
        values = response.split("\n")[2].split(" | ")
        offset = 0
        players = []

        while offset < len(values) - 1:
            if values[offset].strip() != "0":
                players.append(self.__parse_player(values, offset))
            offset += 5

        return players

    def run(self):
        response = self.rcon.execute("listplayers")

        return self.__parse_response(response)
