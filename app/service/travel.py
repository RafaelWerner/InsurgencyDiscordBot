from app.service.base import BaseService

class Travel(BaseService):
    def __build_map_string(self, map_name, team, lighting):
        single_name = map_name

        if single_name.lower() == "hideout":
            single_name = "Town"

        return f"{map_name}?Scenario=Scenario_{map_name}_Checkpoint_{team}?Lighting={lighting}"

    async def run(self, map_name, team, lighting):
        map_string = self.__build_map_string(map_name, team, lighting)
        command = f"travel {map_string}".strip()

        return await self.rcon.execute(command)
