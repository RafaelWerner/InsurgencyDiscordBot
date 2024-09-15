from app.core.manager import Manager
from app.model.player import Player

class ListPlayers:
    __player_lenght = 5
    __index_id = 0
    __index_name = 1
    __index_net_id = 2
    __index_ip = 3
    __index_score = 4

    def __init__(self):
        self.rcon = Manager().rcon()

    def __id(self, values, offset):
        try:
            return int(values[offset + self.__index_id].strip())
        except:
            return 0

    def __name(self, values, offset):
        try:
            return values[offset + self.__index_name].strip()
        except:
            return "Unknown"

    def __ip(self, values, offset):
        try:
            return values[offset + self.__index_ip].strip()
        except:
            return ""

    def __net_id(self, values, offset):
        try:
            return values[offset + self.__index_net_id].split(":")[1].strip()
        except:
            return "0"

    def __score(self, values, offset):
        try:
            return int(values[offset + self.__index_score].strip())
        except ValueError:
            return 0

    def __parse_player(self, values, offset):
        return Player(
            **{
                "id": self.__id(values, offset),
                "name": self.__name(values, offset),
                "net_id": self.__net_id(values, offset),
                "ip": self.__ip(values, offset),
                "score": self.__score(values, offset)
            }
        )

    def __parse_response(self, response):
        print(f"Response: {response}")
        values = response.split("\n")[2].split(" | ")
        offset = 0
        bots = 0
        players = []

        while offset + self.__player_lenght <= len(values):
            if self.__id(values, offset) == 0:
                bots = bots + 1
            else:
                players.append(self.__parse_player(values, offset))

            offset += 5

        return {"bots": bots, "humans": players}

    def run(self):
        response = self.rcon.execute("listplayers")

        return self.__parse_response(response)
