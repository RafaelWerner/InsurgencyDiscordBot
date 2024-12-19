from app.singleton.config import SingletonConfig
from app.core.rcon import RCON

class SingletonRCON:
    _instance = None
    _rcon = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SingletonRCON, cls).__new__(cls, *args, **kwargs)

        return cls._instance

    def get(self):
        if self._rcon is None:
            config = SingletonConfig().get()['rcon']
            self._rcon = RCON(config['host'], config['port'], config['password'])

        return self._rcon
