from app.model.admin import Admin

class SingletonAdmins:
    _instance = None
    _admins = []

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SingletonAdmins, cls).__new__(cls, *args, **kwargs)

        return cls._instance

    def load(self):
        if not self._admins:
            self._admins = Admin().all()

    def get(self):
        self.load()

        return self._admins

    async def find(self, id):
        self.load()

        for admin in self._admins:
            if admin.plataform_id == id or admin.discord_id == id:
                return admin

        return None

    async def is_admin(self, id):
        result = await self.find(id)

        return result is not None
