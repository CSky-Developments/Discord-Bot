from bot.commands.ping import setup_ping_command
from bot.commands.license import setup_license_command
from bot.commands.invite import setup_invite_command
from bot.commands.ticket import setup_ticket_command
from bot.commands.order import setup_order_command
from bot.commands.plugin import setup_plugin_command
from bot.commands.reward import setup_reward_command
from bot.commands.staffapp import setup_staffapp_command
from bot.commands.embed import setup_embed_command

__all__ = [
    "setup_ping_command",
    "setup_license_command",
    "setup_invite_command",
    "setup_ticket_command",
    "setup_order_command",
    "setup_plugin_command",
    "setup_reward_command",
    "setup_staffapp_command",
    "setup_embed_command",
]
