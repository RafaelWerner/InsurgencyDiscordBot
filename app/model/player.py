from app.model.base import BaseModel

class Player(BaseModel):

    def prepare(self):
        self.id = None
        self.name = None
        self.net_id = None
        self.ip = None
        self.score = 0
