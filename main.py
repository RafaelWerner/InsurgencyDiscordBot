# Description: Main file of the bot, where the discord client is created and the commands are defined.
import requests

from discord import app_commands
import discord

from app.core.manager import Manager
from app.model.vip import VIP

from app.command.list_online_players import ListOnlinePlayers
from app.command.want_play import WantPlay
from app.command.kick_player_by_name import KickPlayerByName

MY_GUILD = discord.Object(id=1269368944355971133)

#channels
VIPS_CHANNEL = 1277410614083584073
LOGS_CHANNEL = 1277640729463619686

#roles
VIP_ROLE = 1270096989216051305

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


Manager(config_file="config.ini", tasks_file="tasks.json", vips_file="vips.json")
client = MyClient()


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

@client.tree.command(name='listar-jogadores')
async def listplayers(interaction: discord.Interaction):
    playerslist = ListOnlinePlayers().run()
    await interaction.response.send_message(playerslist)

@client.tree.command(name='quero-jogar')
async def want_play(interaction: discord.Interaction):
    if (interaction.channel_id != VIPS_CHANNEL):
        return await interaction.response.send_message("Comando disponível apenas para VIPS no canal **vips**.")

    sender_id = interaction.user.id

    if not Manager().vips.is_vip(sender_id):
        return "Você não tem permissão para executar este comando.\nTorne-se VIP para garantir sua vaga."

    response = await WantPlay().run(sender_id)

    await interaction.response.send_message(response)

@client.tree.command(name='listar-vips')
async def list_vips(interaction: discord.Interaction):
    vips = Manager().vips.all()
    vips_list = f"Estamos com {len(vips)} VIPs:\n"

    for vip in vips:
        vips_list += f"- **{vip.name}**\n"

    await interaction.response.send_message(vips_list)

async def catch_steam_info(steam_id):
    response = requests.get(f"https://playerdb.co/api/player/steam/{steam_id}")

    if response.status_code == 200:
        return response.json()

    return None

@client.tree.command(name='kickar-jogador-por-nome')
@app_commands.describe(player_name='Nome do jogador a ser kickado')
async def kick_player_by_name(interaction: discord.Interaction, player_name: str):
    sender_id = interaction.user.id

    if not Manager().vips.is_admin(sender_id):
        return await interaction.response.send_message("Você não tem permissão para kickar jogadores.")

    response = await KickPlayerByName(player_name).run()

    await interaction.response.send_message(response)

@client.tree.command(name='adicionar-vip')
@app_commands.describe(user='Usuário a ser adicionado como VIP', steam_id='ID da conta Steam do usuário, pegar no perfil do usuário na Steam')
async def add_new_vip(interaction: discord.Interaction, user: discord.Member, steam_id: str):
    sender_id = interaction.user.id

    if not Manager().vips.is_admin(sender_id):
        return await interaction.response.send_message("Você não tem permissão para adicionar VIPs.")

    if Manager().vips.find(user.id):
        return await interaction.response.send_message("O {user.name} já é um VIP.")

    if (steam_id.strip() == ""):
        return await interaction.response.send_message("É necessário informar o ID da conta Steam do usuário.")

    steam_info = await catch_steam_info(steam_id)

    if steam_info is None:
        return await interaction.response.send_message("Não foi possível validar o ID da conta Steam do usuário")

    steam_id64 = steam_info["data"]["player"]["meta"]["steamid64"]

    Manager().vips.add(steam_id64, user.id, user.name)

    guild = client.get_guild(MY_GUILD.id)
    role = guild.get_role(VIP_ROLE)

    user.add_roles(role)

    await interaction.response.send_message(f'Pronto adicionei o {user.name} como VIP.')

client.run(Manager().config['discord']['token'])
