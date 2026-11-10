import discord
from discord import app_commands
import pytest

from bot.commands.ping import setup_ping_command
from bot.commands.embed import setup_embed_command
from bot.commands.invite import setup_invite_command
from bot.commands.ticket import setup_ticket_command
from bot.commands.order import setup_order_command
from bot.commands.plugin import setup_plugin_command
from bot.commands.reward import setup_reward_command
from bot.commands.staffapp import setup_staffapp_command
from bot.commands.license import setup_license_command
from unittest.mock import MagicMock

def test_all_commands_registration():
    client = discord.Client(intents=discord.Intents.none())
    tree = app_commands.CommandTree(client)
    guild_target = discord.Object(id=1111724818614722690)

    invite_mgr = MagicMock()
    ticket_mgr = MagicMock()

    setup_ping_command(tree, guild_target)
    setup_embed_command(tree, guild_target)
    setup_invite_command(tree, guild_target, invite_mgr)
    setup_ticket_command(tree, guild_target, ticket_mgr)
    setup_order_command(tree, guild_target, ticket_mgr)
    setup_plugin_command(tree, guild_target, ticket_mgr)
    setup_reward_command(tree, guild_target, ticket_mgr)
    setup_staffapp_command(tree, guild_target)
    setup_license_command(tree, guild_target)

    commands = tree.get_commands(guild=guild_target)
    command_names = [cmd.name for cmd in commands]

    assert "ping" in command_names
    assert "embed" in command_names
    assert "invite" in command_names
    assert "ticket" in command_names
    assert "order" in command_names
    assert "plugin" in command_names
    assert "reward" in command_names
    assert "staffapp" in command_names
    assert "license" in command_names
