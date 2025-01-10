from app.singleton.users import SingletonUsers

class ListAdmins():
    async def __build_admins(self):
        admins_list = SingletonUsers().get_admins()
        result = []

        for admin in admins_list:
            result.append(f"- {admin.name}")

        return result

    async def run(self):
        admins_list = await self.__build_admins()

        message = [
            "```ansi",
            f"Estamos com {len(admins_list)} [2;35mAdmins[0m:\n[2;35m",
            "\n".join(admins_list),
            "[0m```"
        ]

        return "\n".join(message)
