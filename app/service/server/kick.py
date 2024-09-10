from app.service.server.base import BaseServer

class Kick(BaseServer):

    def __init__(self, identifier, reason=None):
        super().__init__()
        self.identifier = identifier
        self.reason = self.__formated_reason(reason)

    def __formated_reason(self, reason):
        if reason is None:
            return ""

        return "_".join(reason.split(" "))

    def run(self):
        command = f"kick {self.identifier} {self.reason}".strip()

        return self.rcon.execute(command)
