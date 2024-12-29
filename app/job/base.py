
class BaseJob:

    def __init__(self, interaction):
        self.response_channel = interaction.channel
        self.user = interaction.user

    async def process(self):
        raise NotImplementedError("process method must be implemented")

    async def execute(self):
        response = await self.process()

        await self.response_channel.send(content = response)
