from app.core.manager import Manager

class BaseServer:

    def __init__(self):
        self.rcon = Manager().rcon()
