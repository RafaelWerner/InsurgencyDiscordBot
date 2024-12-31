
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

from app.resources.resources import *
from app.resources.locales import *

# Logs, Save log with name as the date time formated
logger = logging.getLogger(__name__)
log_name = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
logging.basicConfig(filename=f'{log_name}.log', encoding='utf-8', level=logging.DEBUG)

# Singleton instance
config = SingletonConfig().get()

# Channels
ADMINS_CHANNEL_ID = int(config['discord']['admins_channel_id'])
BOT_COMMAND_CHANNEL_NAME = config['discord']['bot_commands_channel_name']
BOT_COMMAND_CHANNEL_ID = int(config['discord']['bot_commands_channel_id'])

# Custom client
client = CustomClient(discord.Object(id = config['discord']['guild_id']))

async def log_action(interaction, message):
    try:
        logs_channel = interaction.guild.get_channel(int(config['discord']['logs_channel_id']))

        if logs_channel:
            log_content = f"**Usuário:** {interaction.user.name}\n> {message}"
            logger.info(log_content)
            await logs_channel.send(log_content)
        else:
            logger.error(f"Canal de logs não encontrado")
    except Exception as e:
        raise Exception(f"Erro ao logar ação: {e}")


async def has_permission(necessary_roles, interaction):
    for role in interaction.user.roles:
        if role.name in necessary_roles:
            return True

    return False

@client.event
async def on_ready():
    logger.info(f'Entrou como {client.user} (ID: {client.user.id})')


@client.tree.command(name='listar-jogadores')
async def listar_jogadores(interaction: discord.Interaction):
    command_name = "listar-jogadores"

    if interaction.channel_id != BOT_COMMAND_CHANNEL_ID:
        await log_action(interaction, StrFmtComandoExecutadoEmCanalIncorreto.format(command_name))
        return await interaction.response.send_message(StrComandoDeveSerExecutadoNoCanal.format(BOT_COMMAND_CHANNEL_NAME))

    await log_action(interaction, StrFmtComandoExecutado.format(command_name))
    playerslist = await ListOnlinePlayers().run()
    await interaction.response.send_message(playerslist)


@client.tree.command(name='enviar-mensagem')
@app_commands.describe(mensagem='Mensagem a ser enviada')
async def enviar_mensagem(interaction: discord.Interaction, mensagem: str):
    min_roles = ["Admin", "Moderador"]
    command_name = "enviar-mensagem"

    if interaction.channel_id != BOT_COMMAND_CHANNEL_ID:
        await log_action(interaction, StrFmtComandoExecutadoEmCanalIncorreto.format(command_name))
        return await interaction.response.send_message(StrComandoDeveSerExecutadoNoCanal.format(BOT_COMMAND_CHANNEL_NAME))

    if not await has_permission(min_roles, interaction):
        await log_action(interaction, StrFmtComandoExecutadoSemPermissao.format(command_name))
        return await interaction.response.send_message(StrComandoDisponivelSomentePara.format(" e ".join(min_roles)))

    try:
        await log_action(interaction, f"Comando {command_name} executado com mensagem: {mensagem}")
        await SendMessage().run(mensagem)
    except Exception as e:
        await log_action(interaction, f"Erro ao enviar mensagem. {e}")
        return await interaction.response.send_message(f"Erro ao enviar mensagem. {e}")

    response_message = f"Mensagem enviada com sucesso: {mensagem}"
    await interaction.response.send_message(response_message)


@client.tree.command(name='quero-jogar')
async def quero_jogar(interaction: discord.Interaction):
    min_roles = ["Admin", "Moderador"]
    command_name = "quero-jogar"

    if interaction.channel_id != BOT_COMMAND_CHANNEL_ID:
        await log_action(interaction, StrFmtComandoExecutadoEmCanalIncorreto.format(command_name))
        return await interaction.response.send_message(StrComandoDeveSerExecutadoNoCanal.format(BOT_COMMAND_CHANNEL_NAME))

    if not await has_permission(min_roles, interaction):
        await log_action(interaction, StrFmtComandoExecutadoSemPermissao.format(command_name))
        return await interaction.response.send_message(StrComandoDisponivelSomentePara.format(" e ".join(min_roles)))

    await log_action(interaction, "Comando quero-jogar executado.")
    await SingletonRunner().schedule(WantPlayJob(interaction))

    await interaction.response.send_message("Espera só um poquinho que vou arrumar um espaço para você jogar.", ephemeral=True)


@client.tree.command(name='listar-admins')
async def listar_admins(interaction: discord.Interaction):
    command_name = "listar-admins"

    if interaction.channel_id != BOT_COMMAND_CHANNEL_ID:
        await log_action(interaction, StrFmtComandoExecutadoEmCanalIncorreto.format(command_name))
        return await interaction.response.send_message(StrComandoDeveSerExecutadoNoCanal.format(BOT_COMMAND_CHANNEL_NAME))

    await log_action(interaction, "Comando listar-admins executado.")
    message = await ListAdmins().run()

    await interaction.response.send_message(message, ephemeral=True)


@client.tree.command(name='banir-jogador')
@app_commands.describe(localizador='Nome ou Id da plataforma do jogador a ser banido',
                       duracao='Duração do ban em minutos, 0 para banimento permanente',
                       motivo='Motivo do ban em 4 palavras no máximo')
async def banir_jogador(interaction: discord.Interaction, localizador: str, duracao: int, motivo: str):
    command_name = "banir-jogador"
    min_roles = ["Admin"]

    if interaction.channel_id != BOT_COMMAND_CHANNEL_ID:
        await log_action(interaction, StrFmtComandoExecutadoEmCanalIncorreto.format(command_name))
        return await interaction.response.send_message(StrComandoDeveSerExecutadoNoCanal.format(BOT_COMMAND_CHANNEL_NAME))

    if not await has_permission(min_roles, interaction):
        await log_action(interaction, StrFmtComandoExecutadoSemPermissao.format(command_name))
        return await interaction.response.send_message(StrComandoDisponivelSomentePara.format(" e ".join(min_roles)))

    await SingletonRunner().schedule(BanPlayerJob(interaction, localizador, duracao, motivo))
    await log_action(interaction, f"Comando banir-jogador agendado com id: {localizador}, motivo: {motivo}, duração: {duracao}")

    await interaction.response.send_message(f'Vou tentar encontrar um jogador com {localizador} no nome ou id e banir ele por {duracao} minutos.')


@client.tree.command(name='expulsar-jogador')
@app_commands.describe(localizador='Nome ou Id da plataforma do jogador a ser kickado', motivo='Motivo do kick em 4 palavras no máximo')
async def explusar_jogador(interaction: discord.Interaction, localizador: str, motivo: str):
    command_name = "expulsar-jogador"
    min_roles = ["Admin", "Moderador"]

    if interaction.channel_id != BOT_COMMAND_CHANNEL_ID:
        await log_action(interaction, StrFmtComandoExecutadoEmCanalIncorreto.format(command_name))
        return await interaction.response.send_message(StrComandoDeveSerExecutadoNoCanal.format(BOT_COMMAND_CHANNEL_NAME))

    if not await has_permission(min_roles, interaction):
        await log_action(interaction, StrFmtComandoExecutadoSemPermissao.format(command_name))
        return await interaction.response.send_message(StrComandoDisponivelSomentePara.format(" e ".join(min_roles)))

    await SingletonRunner().schedule(KickPlayerJob(interaction, localizador, motivo))
    await log_action(interaction, f"Comando kickar-jogador agendado com o termo: {localizador} e motivo: {motivo}.")

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

    if interaction.channel_id != BOT_COMMAND_CHANNEL_ID:
        await log_action(interaction, StrFmtComandoExecutadoEmCanalIncorreto.format(command_name))
        return await interaction.response.send_message(StrComandoDeveSerExecutadoNoCanal.format(BOT_COMMAND_CHANNEL_NAME))

    if not await has_permission(min_roles, interaction):
        await log_action(interaction, StrFmtComandoExecutadoSemPermissao.format(command_name))
        return await interaction.response.send_message(StrComandoDisponivelSomentePara.format(" e ".join(min_roles)))

    await log_action(interaction, f"Comando trocar-mapa agendado com mapa: {mapa}, equipe: {time}, luz: {iluminacao}")

    await SingletonRunner().schedule(ChangeMapJob(interaction, mapa, time, iluminacao))
    await interaction.response.send_message("O mapa será trocado em breve.")


async def update_config(interaction: discord.Interaction, nome_da_propriedade: str, novo_valor: str):
    command_name = "alterar-config"
    min_roles = ["Admin"]

    if interaction.channel_id != BOT_COMMAND_CHANNEL_ID:
        await log_action(interaction, StrFmtComandoExecutadoEmCanalIncorreto.format(command_name))
        return await interaction.response.send_message(StrComandoDeveSerExecutadoNoCanal.format(BOT_COMMAND_CHANNEL_NAME))

    if not await has_permission(min_roles, interaction):
        await log_action(interaction, StrFmtComandoExecutadoSemPermissao.format(command_name))
        return await interaction.response.send_message(StrComandoDisponivelSomentePara.format(" e ".join(min_roles)))

    await log_action(interaction, f"Comando alterar_config executado com propriedade: {nome_da_propriedade}, valor: {novo_valor}")
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


@client.tree.command(name='me-ajuda')
async def help_me(interaction: discord.Interaction):
    message = """
    **Comandos disponíveis:**
    [ Para todos]
    - /listar-jogadores: Lista os jogadores online.
    - /listar-admins: Lista os administradores online.

    [ Somente para Moderadores e Admins ]
    - /expulsar-jogador: Expulsa um jogador do servidor.
    - /enviar-mensagem: Envia uma mensagem para todos os jogadores.
    - /quero-jogar: Entra na fila para jogar.

    [ Somente para Admins ]
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
