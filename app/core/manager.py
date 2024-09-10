
import json
import os
from configparser import ConfigParser

from app.core.singleton import Singleton
from app.core.rcon import RCON
from app.model.vip import VIP, VIPs

class Manager(Singleton):
    __rcon = None

    def __str__(self):
        return f"""
            Manager instance:
            - Config:
                {self.config}
            - Tasks:
                {self.tasks}
            - Vips:
                {self.vips.all()}
        """
    def setup(self, config_file='config.ini', tasks_file='tasks.json', vips_file='vips.json'):
        self.__load_config(config_file)
        self.__load_tasks(tasks_file)
        self.__load_vips(vips_file)

    def __file_exists(self, file):
        if not os.path.isfile(file):
            raise FileNotFoundError(f"File not found: {file}")

    def __load_config(self, config_file):
        self.__file_exists(config_file)
        self.config = ConfigParser()
        self.config.read(config_file)

    def __load_tasks(self, tasks_file):
        self.__file_exists(tasks_file)

        with open(tasks_file) as f:
            self.tasks = json.load(f)

    def __load_vips(self, vips_file):
        self.__file_exists(vips_file)
        self.vips = VIPs(vips_file)

    def rcon(self):
        if self.__rcon is None:
            self.__rcon = RCON(self.config['rcon'])

        return self.__rcon
