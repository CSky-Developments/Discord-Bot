from bot.commands.ping import setup_ping_command
from bot.commands.invite import setup_invite_command
from bot.commands.ticket import setup_ticket_command
from bot.commands.order import setup_order_command
from bot.commands.staffapp import setup_staffapp_command
from bot.commands.embed import setup_embed_command
from bot.commands.links import setup_links_command
from bot.commands.store import setup_store_command
from bot.commands.buyer import setup_buyer_command

__all__ = [
    "setup_ping_command",
    "setup_invite_command",
    "setup_ticket_command",
    "setup_order_command",
    "setup_staffapp_command",
    "setup_embed_command",
    "setup_links_command",
    "setup_store_command",
    "setup_buyer_command",
]
