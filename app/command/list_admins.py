from app.singleton.users import SingletonUsers

class ListAdmins():
    async def __build_admins(self):
        admins_list = SingletonUsers().get_admins()
        result = []

        for admin in admins_list:
            result.append(f"- {admin.name}")

        return result

    async def __build_moderators(self):
        moderators_list = SingletonUsers().get_moderators()
        result = []

        for moderator in moderators_list:
            result.append(f"- {moderator.name}")

        return result

    async def run(self):
        admins_list = await self.__build_admins()
        moderators_list = await self.__build_moderators()

        message = [
            "```ansi",
            f"Estamos com {len(admins_list)} [2;35mAdmins[0m e [2;31mModeradores[0m:\n[2;35m",
            "\n".join(admins_list),
            f"[0m\nEstamos com {len(moderators_list)} Moderadores:\n[2;31m",
            "\n".join(moderators_list),
            "[0m```"
        ]

        return "\n".join(message)
