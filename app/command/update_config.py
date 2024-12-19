import asyncio
from app.service.gamemodeproperty import GameModeProperty
from app.service.say import Say

class UpdateConfig:
    async def __warn_change_property(self, property_name, new_value):
        message = f"A propriedade {property_name} foi alterada para {new_value}."

        await Say().run(message)

    def __sanitize_value(self, new_value):
        if ',' in new_value:
            new_value = new_value.replace(',', '.')

        return new_value

    async def run(self, property_name, new_value):
        sanitized_value = self.__sanitize_value(new_value)
        await self.__warn_change_property(property_name, sanitized_value)

        try:
            return await GameModeProperty().run(property_name, sanitized_value)
        except Exception as e:
            return str(e)
