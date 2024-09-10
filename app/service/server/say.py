
from app.service.server.base import BaseServer

class Say(BaseServer):
    MAX_LINE_LENGTH = 60

    def __init__(self, message):
        super().__init__()
        self.message = self.__parse_message(message.strip())

    def __parse_message(self, message):
        parsed_message = [message]

        if message is None:
            raise ValueError("Message is required")

        if "\n" in message:
            parsed_message = message.split("\n")

        for line in parsed_message:
            if len(line) > self.MAX_LINE_LENGTH:
                raise ValueError("Message is too long")

        return parsed_message

    def __send(self, text):
        command = f"say {text}"
        return self.rcon.execute(command)

    def run(self):
        responses = []

        for line in self.message:
            response = self.__send(line)

            if response is not None:
                responses.append(response)

        return "\n".join(responses)
