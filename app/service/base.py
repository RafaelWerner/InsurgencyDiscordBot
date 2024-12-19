from app.singleton.rcon import SingletonRCON

class BaseService:
    def __init__(self):
        self.rcon = SingletonRCON().get()
