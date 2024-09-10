import json
from app.model.base import BaseModel

class VIP(BaseModel):

    def prepare(self):
        self.steam_id = None
        self.discord_id = None
        self.name = None
        self.role = "soldier"

    def is_admin(self):
        return self.role == "admin"

class VIPs:
    def __init__(self, file):
        self.vips = []
        self.__load(file)

    def __load(self, file):
        with open(file, 'r') as f:
            data = json.load(f)

        for vip in data:
                self.vips.append(VIP(**vip))

    def __save(self, file):
        with open(file, 'w') as f:
            json.dump([vip.__dict__ for vip in self.vips], f)

    def all(self):
        return self.vips

    def add(self, steam_id, discord_id, name, role="vip"):
        self.vips.append(VIP(steam_id=steam_id, discord_id=discord_id, name=name, role=role))
        self.__save()

    def remove(self, vip_id):
        vip = self.find(vip_id)
        self.vips.remove(vip)
        self.__save()

    def find(self, id):
        for vip in self.vips:
            if vip.steam_id == id or vip.discord_id == id:
                return vip

        return None

    def is_admin(self, id):
        vip = self.find(id)

        if vip is None:
            return False

        return vip.is_admin() if vip else False

    def is_vip(self, id):
        vip = self.find(id)

        return not vip is None
