import configparser

class SingletonConfig:
    _instance = None
    _configuration = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SingletonConfig, cls).__new__(cls, *args, **kwargs)

        return cls._instance

    def get(self):
        if self._configuration is None:
            self._configuration = configparser.ConfigParser()
            self._configuration.read('config.ini')

        return self._configuration
