from app.service.base import BaseService

class OnlinePlayer:
    def __init__(self, **kwargs):
        self.id = None
        self.name = None
        self.net_id = None
        self.ip = None
        self.score = 0

        for key, value in kwargs.items():
            setattr(self, key, value)

    def safe_name(self):
        return self.name[0:20]

    def __repr__(self):
        return str(self.__dict__)

class ListPlayers(BaseService):
    __player_lenght = 5
    __index_id = 0
    __index_name = 1
    __index_net_id = 2
    __index_ip = 3
    __index_score = 4

    __TERMS_TO_SANITIZE = ["TGS | ",]

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
        return OnlinePlayer(
            **{
                "id": self.__id(values, offset),
                "name": self.__name(values, offset),
                "net_id": self.__net_id(values, offset),
                "ip": self.__ip(values, offset),
                "score": self.__score(values, offset)
            }
        )

    def __parse_response(self, response):
        values = response.split("\n")[2].split(" | ")
        offset = 0
        bots = 0
        players = []

        while offset + self.__player_lenght <= len(values):
            if self.__id(values, offset) == 0:
                bots += 1
            else:
                players.append(self.__parse_player(values, offset))

            offset += 5

        return {"bots": bots, "humans": players}

    def __sanitize(self, response):
        for term in self.__TERMS_TO_SANITIZE:
            response = response.replace(term, "")

        return response

    async def run(self):
        response = await self.rcon.execute("listplayers")
        sanitized_response = self.__sanitize(response)

        return self.__parse_response(sanitized_response)
