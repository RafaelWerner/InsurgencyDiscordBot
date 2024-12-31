from app.singleton.users import SingletonUsers

class ListAdmins():
    async def __build_admins(self):
        admins_list = SingletonUsers().get_admins()
        result = []

        for admin in admins_list:
            result.append(f"[2;35m- {admin.name}[0m")

        return result

    async def __build_moderators(self):
        moderators_list = SingletonUsers().get_moderators()
        result = []

        for moderator in moderators_list:
            result.append(f"[2;31m- {moderator.name}[0m")

        return result

    async def run(self):
        admins_list = await self.__build_admins()
        moderators_list = await self.__build_moderators()

        message = [
            "```ansi",
            f"Estamos com {len(admins_list)} Admins:\n",
            "\n".join(admins_list),
            f"Estamos com {len(moderators_list)} Moderadores:\n",
            "\n".join(moderators_list),
            "```"
        ]

        return "\n".join(message)
