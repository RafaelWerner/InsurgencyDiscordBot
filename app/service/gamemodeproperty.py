from app.service.base import BaseService

class GameModeProperty(BaseService):
    async def run(self, name, new_value):
        command = f"gamemodeproperty {name} {new_value}".strip()

        return await self.rcon.execute(command)
