from app.model.user import User

class SingletonUsers:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SingletonUsers, cls).__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self):
        self._users = []
        self._admin_users = []
        self._admins_ids = []
        self._hash_table = {}

        self.load()

    def load(self):
        self._users = User().all()

        for user in self._users:
            self._hash_table[user.plataform_id] = user
            self._hash_table[user.discord_id] = user

            if user.role == "admin":
                self._admin_users.append(user)
                self._admins_ids.append(user.plataform_id)
                self._admins_ids.append(user.discord_id)

    def get(self):
        return self._users

    async def find(self, id):
        return self._hash_table.get(id)

    def get_admins(self):
        return self._admin_users

    async def is_admin(self, id):
        return id in self._admins_ids

    async def is_normal_user(self, id):
        return id not in self._admins_ids
