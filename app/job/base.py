
class BaseJob:

    def __init__(self, interaction, retries=0):
        self.interaction = interaction
        self.retries = retries

    def retryable(self):
        return self.retries > 0

    def response_channel(self):
        return self.interaction.channel

    def user(self):
        return self.interaction.user

    async def process(self):
        raise NotImplementedError("process method must be implemented")

    async def execute(self):
        self.retries -= 1
        response = await self.process()

        await self.response_channel().send(content = response)
