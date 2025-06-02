import discord
from discord.ext import tasks

from app.singleton.runner import SingletonRunner
from app.resources.locales import *

class CustomClient(discord.Client):
    def __init__(self, logger, guild_id, logs_channel_id):
        super().__init__(intents=discord.Intents.default())
        self.tree = discord.app_commands.CommandTree(self)
        self.logger = logger
        self.guild_id = guild_id
        self.logs_channel_id = logs_channel_id

    def run(self, token):
        super().run(token)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=self.guild_id)

        self.background_tasks.start()
        await self.tree.sync(guild=self.guild_id)

    @tasks.loop(seconds=2)
    async def background_tasks(self):
        await self.runner.execute()

    @background_tasks.before_loop
    async def before_run_tasks(self):
        self.runner = SingletonRunner()
        await self.wait_until_ready()

    async def log_action(self, interaction, message):
        try:
            logs_channel = interaction.guild.get_channel(self.logs_channel_id)

            if logs_channel:
                log_content = f"**Usuário:** {interaction.user.name}\n> {message}"
                self.logger.info(log_content)
                await logs_channel.send(log_content)
            else:
                logger.error(f"Canal de logs não encontrado")
        except Exception as e:
            raise Exception(f"Erro ao logar ação: {e}")


    async def has_permission(self, necessary_roles, interaction):
        if necessary_roles is None or not necessary_roles:
            return True

        for role in interaction.user.roles:
            if role.name in necessary_roles:
                return True

        return False


    async def is_valid_execution(self, command_name, necessary_roles, permited_channels, interaction):
        if not await self.has_permission(necessary_roles, interaction):
            await self.log_action(interaction, StrFmtComandoExecutadoSemPermissao.format(command_name))
            await interaction.response.send_message(StrComandoDisponivelSomentePara.format(" ou ".join(necessary_roles)))
            return False

        if not interaction.channel_id in permited_channels:
            await self.log_action(interaction, StrFmtComandoExecutadoEmCanalIncorreto.format(command_name))
            await interaction.response.send_message(StrComandoNaoPermitidoNesteCanal, ephemeral=True)
            return False

        return True