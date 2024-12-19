from app.model.user import User

class Admin:
    def __init__(self):
        self.admins = User().find_by({'role': 'admin'})

    def all(self):
        return self.admins
