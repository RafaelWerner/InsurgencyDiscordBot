from app.service.base import BaseService

class Ban(BaseService):
    def __formated_reason(self, reason):
        if reason is None:
            return ""
        return "_".join(reason.split(" "))

    async def run(self, identifier, duration, reason=None):
        formatted_reason = self.__formated_reason(reason)

        if duration == 0:
            command = f"permban {identifier} {formatted_reason}".strip()
        else:
            command = f"ban {identifier} {duration} {formatted_reason}".strip()

        return await self.rcon.execute(command)
