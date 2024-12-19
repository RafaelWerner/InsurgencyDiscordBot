import asyncio
from app.service.travel import Travel
from app.resources.resources import AVAILABLE_MAPS

class ChangeMap:
    AVAILABLE_TEAMS = ["Insurgents", "Security"]
    AVAILABLE_LIGHTING = ["Day", "Night"]

    def __get_team(self, team_name):
        for team in self.AVAILABLE_TEAMS:
            if team.lower() == team_name.lower():
                return team

        raise ValueError(f"Time {team_name} não encontrado.")

    def __get_lighting(self, lighting_description):
        for lighting in self.AVAILABLE_LIGHTING:
            if lighting.lower() == lighting_description.lower():
                return lighting

        raise ValueError(f"Lighting {lighting_description} não encontrado.")

    async def __get_map_name(self, map_name):
        for map in AVAILABLE_MAPS:
            if map.lower() == map_name.lower():
                return map

        raise ValueError(f"Mapa {map_name} não encontrado.")

    async def run(self, map_name, team_name, lighting_description):
        try:
            team = self.__get_team(team_name)
            lighting = self.__get_lighting(lighting_description)
            name = await self.__get_map_name(map_name)

            await Travel().run(name, team, lighting)
        except Exception as e:
            return str(e)

        return f"Mapa alterado com sucesso para {name} {team} {lighting}"
