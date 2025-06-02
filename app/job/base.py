
class BaseJob:

    def __init__(self, interaction):
        self.interaction = interaction

    def response_channel(self):
        return self.interaction.channel

    def user(self):
        return self.interaction.user

    async def process(self):
        raise NotImplementedError("process method must be implemented")

    async def execute(self):
        response = await self.process()

        await self.response_channel().send(content = response)
