
import logging
import discord
from discord import app_commands
from datetime import datetime

from app.core.client import CustomClient

from app.singleton.config import SingletonConfig
from app.singleton.runner import SingletonRunner

from app.command.list_online_players import ListOnlinePlayers
from app.command.list_admins import ListAdmins
from app.command.update_config import UpdateConfig
from app.command.send_message import SendMessage

from app.job.kick_player import KickPlayerJob
from app.job.want_play import WantPlayJob
from app.job.ban_player import BanPlayerJob
from app.job.change_map import ChangeMapJob
from app.job.list_players import ListPlayersJob

from app.resources.resources import *
from app.resources.locales import *

# Logs, Save log with name as the date time formated
logger = logging.getLogger(__name__)
log_name = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
logging.basicConfig(filename=f'{log_name}.log', encoding='utf-8', level=logging.DEBUG)

# Singleton instance
config = SingletonConfig().get()
SERVER_IP = config['rcon']['host']

# Channels
ADMINS_CHANNEL_ID = int(config['discord']['admins_channel_id'])
BOT_COMMAND_CHANNEL_NAME = config['discord']['bot_commands_channel_name']
BOT_COMMAND_CHANNEL_ID = int(config['discord']['bot_commands_channel_id'])
BOT_COMMAND_PUBLIC_CHANNEL_ID = int(config['discord']['bot_commands_public_channel_id'])
LOGS_CHANNEL_ID = int(config['discord']['logs_channel_id'])
# Custom client
client = CustomClient(logger, discord.Object(id = config['discord']['guild_id']), LOGS_CHANNEL_ID)

@client.event
async def on_ready():
    logger.info(f'Entrou como {client.user} (ID: {client.user.id})')


@client.tree.command(name='listar-jogadores')
async def listar_jogadores(interaction: discord.Interaction):
    command_name = "listar-jogadores"
    permited_channels = [BOT_COMMAND_CHANNEL_ID, BOT_COMMAND_PUBLIC_CHANNEL_ID]

    if not await client.is_valid_execution(command_name, None, permited_channels, interaction):
        return

    await client.log_action(interaction, StrFmtComandoExecutado.format(command_name))
    await SingletonRunner().schedule(ListPlayersJob(interaction), retries=3)

    await interaction.response.send_message("Aguarde um momento, estou listando os jogadores online.", ephemeral=True)


@client.tree.command(name='enviar-mensagem')
@app_commands.describe(mensagem='Mensagem a ser enviada')
async def enviar_mensagem(interaction: discord.Interaction, mensagem: str):
    min_roles = ["Admin", "Moderador"]
    permited_channels = [BOT_COMMAND_CHANNEL_ID]
    command_name = "enviar-mensagem"

    if not await client.is_valid_execution(command_name, min_roles, permited_channels, interaction):
        return

    try:
        await client.log_action(interaction, f"Comando {command_name} executado com mensagem: {mensagem}")
        await SendMessage().run(mensagem)
    except Exception as e:
        await client.log_action(interaction, f"Erro ao enviar mensagem. {e}")
        return await interaction.response.send_message(f"Erro ao enviar mensagem. {e}")

    response_message = f"Mensagem enviada com sucesso: {mensagem}"
    await interaction.response.send_message(response_message)


@client.tree.command(name='quero-jogar')
async def quero_jogar(interaction: discord.Interaction):
    min_roles = ["Admin"]
    permited_channels = [BOT_COMMAND_CHANNEL_ID]
    command_name = "quero-jogar"

    if not await client.is_valid_execution(command_name, min_roles, permited_channels, interaction):
        return

    await client.log_action(interaction, "Comando quero-jogar executado.")
    await SingletonRunner().schedule(WantPlayJob(interaction), retries=3)

    await interaction.response.send_message("Espera só um poquinho que vou arrumar um espaço para você jogar.", ephemeral=True)


@client.tree.command(name='listar-admins')
async def listar_admins(interaction: discord.Interaction):
    command_name = "listar-admins"
    permited_channels = [BOT_COMMAND_CHANNEL_ID, BOT_COMMAND_PUBLIC_CHANNEL_ID]

    if not await client.is_valid_execution(command_name, None, permited_channels, interaction):
        return

    await client.log_action(interaction, "Comando listar-admins executado.")
    message = await ListAdmins().run()

    await interaction.response.send_message(message, ephemeral=True)


@client.tree.command(name='banir-jogador')
@app_commands.describe(localizador='Nome ou Id da plataforma do jogador a ser banido',
                       duracao='Duração do ban em minutos, 0 para banimento permanente',
                       motivo='Motivo do ban em 4 palavras no máximo')
async def banir_jogador(interaction: discord.Interaction, localizador: str, duracao: int, motivo: str):
    command_name = "banir-jogador"
    min_roles = ["Admin"]
    permited_channels = [BOT_COMMAND_CHANNEL_ID]

    if not await client.is_valid_execution(command_name, min_roles, permited_channels, interaction):
        return

    await SingletonRunner().schedule(BanPlayerJob(interaction, localizador, duracao, motivo))
    await client.log_action(interaction, f"Comando banir-jogador agendado com id: {localizador}, motivo: {motivo}, duração: {duracao}")

    await interaction.response.send_message(f'Vou tentar encontrar um jogador com {localizador} no nome ou id e banir ele por {duracao} minutos.')


@client.tree.command(name='expulsar-jogador')
@app_commands.describe(localizador='Nome ou Id da plataforma do jogador a ser kickado', motivo='Motivo do kick em 4 palavras no máximo')
async def explusar_jogador(interaction: discord.Interaction, localizador: str, motivo: str):
    command_name = "expulsar-jogador"
    min_roles = ["Admin"]
    permited_channels = [BOT_COMMAND_CHANNEL_ID]

    if not await client.is_valid_execution(command_name, min_roles, permited_channels, interaction):
        return

    await SingletonRunner().schedule(KickPlayerJob(interaction, localizador, motivo))
    await client.log_action(interaction, f"Comando kickar-jogador agendado com o termo: {localizador} e motivo: {motivo}.")

    await interaction.response.send_message(f'Vou tentar encontrar um jogador com {localizador} no nome ou id e expulsar ele.')


@client.tree.command(name='trocar-mapa')
@app_commands.describe(mapa='Escolha o mapa para o qual deseja trocar', time='Escolha a equipe para a qual deseja trocar', iluminacao='Escolha o horário para a luz do mapa')
@app_commands.choices(
    mapa=[
        app_commands.Choice(name=available_map, value=available_map)
        for available_map in AVAILABLE_MAPS
    ],
    time=[
        app_commands.Choice(name='Security', value='Security'),
        app_commands.Choice(name='Insurgents', value='Insurgents')
    ],
    iluminacao=[
        app_commands.Choice(name='Day', value='Day'),
        app_commands.Choice(name='Night', value='Night')
    ]
)
async def trocar_mapa(interaction: discord.Interaction, mapa: str, time: str, iluminacao: str):
    command_name = "trocar-mapa"
    min_roles = ["Admin"]
    permited_channels = [BOT_COMMAND_CHANNEL_ID]

    if not await client.is_valid_execution(command_name, min_roles, permited_channels, interaction):
        return

    await client.log_action(interaction, f"Comando trocar-mapa agendado com mapa: {mapa}, equipe: {time}, luz: {iluminacao}")

    await SingletonRunner().schedule(ChangeMapJob(interaction, mapa, time, iluminacao))
    await interaction.response.send_message("O mapa será trocado em breve.")


async def update_config(interaction: discord.Interaction, nome_da_propriedade: str, novo_valor: str):
    command_name = "alterar-config"
    min_roles = ["Admin"]
    permited_channels = [BOT_COMMAND_CHANNEL_ID]

    if not await client.is_valid_execution(command_name, min_roles, permited_channels, interaction):
        return

    await client.log_action(interaction, f"Comando alterar_config executado com propriedade: {nome_da_propriedade}, valor: {novo_valor}")
    response = await UpdateConfig().run(nome_da_propriedade, novo_valor)

    await interaction.response.send_message(response)


@client.tree.command(name='alterar-config-bot')
@app_commands.describe(nome_da_propriedade='Escolha a propriedade a ser alterada', novo_valor='Escolha o valor para a propriedade')
@app_commands.choices(
    nome_da_propriedade=[
        app_commands.Choice(name=description, value=name)
        for description, name in AVAILABLE_BOT_PROPERTIES.items()
    ]
)
async def update_bot_config(interaction: discord.Interaction, nome_da_propriedade: str, novo_valor: str):
    return await update_config(interaction, nome_da_propriedade, novo_valor)


@client.tree.command(name='alterar-config-jogadores')
@app_commands.describe(nome_da_propriedade='Escolha a propriedade a ser alterada', novo_valor='Escolha o valor para a propriedade')
@app_commands.choices(
    nome_da_propriedade=[
        app_commands.Choice(name=description, value=name)
        for description, name in AVAILABLE_PLAYER_PROPERTIES.items()
    ]
)
async def update_players_config(interaction: discord.Interaction, nome_da_propriedade: str, novo_valor: str):
    return await update_config(interaction, nome_da_propriedade, novo_valor)


@client.tree.command(name='alterar-config-rodada')
@app_commands.describe(nome_da_propriedade='Escolha a propriedade a ser alterada', novo_valor='Escolha o valor para a propriedade')
@app_commands.choices(
    nome_da_propriedade=[
        app_commands.Choice(name=description, value=name)
        for description, name in AVAILABLE_ROUND_PROPERTIES.items()
    ]
)
async def update_round_config(interaction: discord.Interaction, nome_da_propriedade: str, novo_valor: str):
    return await update_config(interaction, nome_da_propriedade, novo_valor)


@client.tree.command(name='alterar-config-sobrevivencia')
@app_commands.describe(nome_da_propriedade='Escolha a propriedade a ser alterada', novo_valor='Escolha o valor para a propriedade')
@app_commands.choices(
    nome_da_propriedade=[
        app_commands.Choice(name=description, value=name)
        for description, name in AVAILABLE_SURVIVAL_PROPERTIES.items()
    ]
)
async def update_survival_config(interaction: discord.Interaction, nome_da_propriedade: str, novo_valor: str):
    return await update_config(interaction, nome_da_propriedade, novo_valor)


@client.tree.command(name='ip_do_server')
async def exibir_ip(interaction: discord.Interaction):
    command_name = "ip_do_server"
    min_roles = ["Admin", "Moderador", "Chegados"]
    permited_channels = [BOT_COMMAND_CHANNEL_ID]

    if not await client.is_valid_execution(command_name, min_roles, permited_channels, interaction):
        return

    await client.log_action(interaction, "Comando ip do server executado.")
    message = f"{SERVER_IP}:27102"

    await interaction.response.send_message(message, ephemeral=True)


@client.tree.command(name='me-ajuda')
async def help_me(interaction: discord.Interaction):
    message = """
    **Comandos disponíveis:**
    [ Para usuários com permissões adicionais ]
    - /ip_do_server: Exibe o ip atual do server

    - /listar-jogadores: Lista os jogadores online.

    - /listar-admins: Lista os administradores online.

    [ Somente para Admins no canal de comandos do bot ]

    - /expulsar-jogador: Expulsa um jogador do servidor.

    - /enviar-mensagem: Envia uma mensagem para todos os jogadores.

    - /quero-jogar: Abrir uma vaga, expulsando um aleatório que não seja um admin.

    - /banir-jogador: Bane um jogador do servidor.

    - /trocar-mapa: Troca o mapa do servidor.

    - /alterar-config-bot: Altera uma configuração do bot.

    - /alterar-config-jogadores: Altera uma configuração dos jogadores.

    - /alterar-config-rodada: Altera uma configuração da rodada.

    - /alterar-config-sobrevivencia: Altera uma configuração de sobrevivência.
    """

    await interaction.response.send_message(message, ephemeral=True)


# Run the client
client.run(config['discord']['token'])
