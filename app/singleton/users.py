from app.model.user import User

class SingletonUsers:
    _instance = None
    _users = []
    _admin_users = []
    _moderator_users = []
    _admins_ids = []
    _moderators_ids = []
    _hash_table = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SingletonUsers, cls).__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self):
        self.load()

    def load(self):
        self._users = User().all()

        for user in self._users:
            self._hash_table[user.net_id] = user
            self._hash_table[user.discord_id] = user

            if user.role == "admin":
                self._admin_users.append(user)
                self._admins_ids.append(user.net_id)
                self._admins_ids.append(user.discord_id)
            elif user.role == "moderator":
                self._moderator_users.append(user)
                self._moderators_ids.append(user.net_id)
                self._moderators_ids.append(user.discord_id)

    def get(self):
        return self._users

    async def find(self, id):
        return self._hash_table.get(id)

    async def is_admin(self, id):
        return id in self._admins_ids

    async def is_moderator(self, id):
        return id in self._moderators_ids

    async def is_normal_user(self, id):
        return id not in self._admins_ids and id not in self._moderators_ids
