from app.singleton.admins import SingletonAdmins

class ListAdmins():
    async def run(self):
        admins_list = SingletonAdmins().all()
        message = f"```ansi\nEstamos com {len(admins_list)} VIPs:\n\n"

        for admin in admins_list:
            message += f"[1;2m[1;35m- {admin.name}[0m[0m\n"

        message = message + "```"

        return message
