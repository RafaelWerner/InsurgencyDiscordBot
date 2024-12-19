import discord
from discord.ext import tasks

from app.core.runner import Runner

class CustomClient(discord.Client):
    def __init__(self, guild_id):
        super().__init__(intents=discord.Intents.default())
        self.tree = discord.app_commands.CommandTree(self)
        self.guild_id = guild_id

    def run(self, token):
        super().run(token)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=self.guild_id)

        self.background_tasks.start()
        await self.tree.sync(guild=self.guild_id)

    @tasks.loop(seconds=60)
    async def background_tasks(self):
        await self.runner.execute()

    @background_tasks.before_loop
    async def before_run_tasks(self):
        self.runner = Runner()
        await self.wait_until_ready()
