import sqlite3

from app.singleton.config import SingletonConfig

class SingletonDatabase:
    _instance = None
    _database = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SingletonDatabase, cls).__new__(cls, *args, **kwargs)

        return cls._instance

    def __del__(self):
        if self._database is not None:
            self._database.close()

    def get(self):
        if self._database is None:
            self._database = sqlite3.connect(SingletonConfig().get()['database']['file'])

        return self._database
