from app.service.base import BaseService

class Say(BaseService):
    MAX_LINE_LENGTH = 80

    def __parse_message(self, message):
        parsed_message = [message]

        if message is None:
            raise ValueError("Nenhuma mensagem encontrada")

        if "\n" in message:
            parsed_message = message.split("\n")

        for line in parsed_message:
            if len(line) > self.MAX_LINE_LENGTH:
                raise ValueError(f"A mensagem é muito comprida: [{line}]")

        return parsed_message

    async def __send(self, text):
        command = f"say {text}"
        return await self.rcon.execute(command)

    async def run(self, message):
        responses = []
        formatted_message = self.__parse_message(message.strip())

        for line in formatted_message:
            response = await self.__send(line)

            if response is not None:
                responses.append(response)

        return "\n".join(responses)
