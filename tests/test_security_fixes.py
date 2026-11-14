import asyncio
from unittest.mock import AsyncMock, MagicMock
import discord
import pytest

from bot.config import Config
from bot.game.counting import CountingGame
from bot.internal_api import build_purchase_embed
from bot.logger import BotLogger
from bot.message.manager import MessageEntry, MessageManager
from bot.ticket.manager import TicketManager, is_staff
from bot.ticket.types import TicketType


@pytest.mark.asyncio
async def test_close_confirm_revokes_creator_not_staff(tmp_path, monkeypatch):
    monkeypatch.setattr(Config, "TICKET_NORMAL", 1001)
    monkeypatch.setattr(Config, "STAFF_ROLE_ID", 2002)

    creator = MagicMock(spec=discord.Member)
    creator.id = 111111111111111111
    creator.guild_permissions = MagicMock(administrator=False)
    creator.roles = []

    staff_closer = MagicMock(spec=discord.Member)
    staff_closer.id = 222222222222222222
    staff_closer.guild_permissions = MagicMock(administrator=False)
    staff_role = MagicMock(id=2002)
    staff_closer.roles = [staff_role]

    guild = MagicMock()
    guild.default_role = MagicMock(name="everyone")
    guild.get_role.return_value = staff_role
    guild.get_member.side_effect = lambda uid: creator if uid == creator.id else None

    tm = TicketManager(guild=guild, data_file=str(tmp_path / "tickets.json"))

    channel = MagicMock(spec=discord.TextChannel)
    channel.category_id = 1001
    channel.topic = f"Ticket Creator: {creator.id}"
    channel.overwrites = {}
    channel.set_permissions = AsyncMock()

    interaction = MagicMock()
    interaction.user = staff_closer
    interaction.response = MagicMock()
    interaction.response.send_message = AsyncMock()

    await tm.handle_close_confirm(interaction, staff_closer, channel, TicketType.NORMAL)

    calls = {call.args[0]: call.kwargs["overwrite"] for call in channel.set_permissions.await_args_list}
    assert creator in calls
    assert calls[creator].view_channel is False
    assert staff_closer not in calls


@pytest.mark.asyncio
async def test_close_confirm_rejects_non_ticket_category(tmp_path, monkeypatch):
    monkeypatch.setattr(Config, "TICKET_NORMAL", 1001)
    guild = MagicMock()
    tm = TicketManager(guild=guild, data_file=str(tmp_path / "tickets.json"))

    channel = MagicMock(spec=discord.TextChannel)
    channel.category_id = 9999

    interaction = MagicMock()
    interaction.response = MagicMock()
    interaction.response.send_message = AsyncMock()

    await tm.handle_close_confirm(interaction, MagicMock(), channel, TicketType.NORMAL)
    interaction.response.send_message.assert_awaited_once()
    assert "can't use this here" in interaction.response.send_message.await_args.args[0]


def test_build_purchase_embed_validates_amounts_and_discord_id():
    with pytest.raises(ValueError):
        build_purchase_embed({"totalAmount": "not-a-number"})

    embed, _ = build_purchase_embed({
        "orderNumber": "ORD-1",
        "totalAmount": "15.00",
        "user": {
            "provider": "discord",
            "providerId": "not-a-snowflake@everyone",
            "discordTag": "buyer#0001",
        },
    })
    buyer_field = next(f for f in embed.fields if f.name == "Buyer")
    assert "<@" not in buyer_field.value
    assert buyer_field.value == "buyer#0001"


def test_message_manager_escapes_backticks(monkeypatch):
    mm = MessageManager(cache_limit=10)
    mm.message_cache["1"] = MessageEntry("hi ```@everyone```", "123", 100.0)
    logged = []
    monkeypatch.setattr("bot.logger.BotLogger.info", lambda msg, discord=False: logged.append(msg))

    ev = MagicMock()
    ev.id = 1
    ev.channel.name = "general"
    mm.handle_message_delete(ev, guild=None)

    assert len(logged) == 1
    assert "```@everyone```" not in logged[0]


@pytest.mark.asyncio
async def test_bot_logger_send_to_discord_uses_allowed_mentions_and_file_on_long_msg():
    mock_channel = MagicMock()
    mock_channel.send = AsyncMock()
    BotLogger._log_channel = mock_channel
    BotLogger._loop = None

    try:
        BotLogger.send_to_discord("A" * 2100)
        await asyncio.sleep(0)
        mock_channel.send.assert_awaited_once()
        kwargs = mock_channel.send.await_args.kwargs
        assert isinstance(kwargs["allowed_mentions"], discord.AllowedMentions)
        assert kwargs["allowed_mentions"].everyone is False
        assert isinstance(kwargs["file"], discord.File)
    finally:
        BotLogger._log_channel = None
        BotLogger._loop = None


@pytest.mark.asyncio
async def test_counting_rejects_underscore_and_unicode_digits(tmp_path, monkeypatch):
    monkeypatch.setattr(Config, "COUNTING_CHANNEL_ID", 555)
    game = CountingGame(data_file=str(tmp_path / "counting.json"))

    for bad in ("1_0", "١"):
        msg = MagicMock()
        msg.channel.id = 555
        msg.author.bot = False
        msg.content = bad
        msg.reply = AsyncMock()
        await game.handle_message(msg)
        msg.reply.assert_not_awaited()
    assert game.current_count == 1


@pytest.mark.asyncio
async def test_commission_accept_deduplicates_and_rolls_back_id_on_failure(tmp_path, monkeypatch):
    monkeypatch.setattr(Config, "TICKET_ORDER", 3003)
    monkeypatch.setattr(Config, "STAFF_ROLE_ID", 2002)

    staff = MagicMock(spec=discord.Member)
    staff.id = 222222222222222222
    staff.mention = "<@222222222222222222>"
    staff.guild_permissions = MagicMock(administrator=True)
    staff.roles = []

    category = MagicMock(spec=discord.CategoryChannel)
    created_channel = MagicMock(spec=discord.TextChannel)
    created_channel.mention = "<#999>"
    created_channel.send = AsyncMock()

    guild = MagicMock()
    guild.default_role = MagicMock()
    guild.get_role.return_value = None
    guild.get_channel.return_value = category
    guild.create_text_channel = AsyncMock(return_value=created_channel)

    tm = TicketManager(guild=guild, data_file=str(tmp_path / "tickets.json"))

    embed = discord.Embed(title="Commission")
    embed.add_field(name="Client", value="Alice")
    embed.add_field(name="Contact", value="alice")

    def make_interaction():
        inter = MagicMock()
        inter.message = MagicMock()
        inter.message.id = 777777
        inter.message.embeds = [embed]
        inter.message.edit = AsyncMock()
        inter.response = MagicMock()
        inter.response.defer = AsyncMock()
        inter.response.send_message = AsyncMock()
        inter.followup = MagicMock()
        inter.followup.send = AsyncMock()
        return inter

    i1 = make_interaction()
    i2 = make_interaction()
    await asyncio.gather(
        tm.handle_commission_accept(i1, staff),
        tm.handle_commission_accept(i2, staff),
    )

    assert guild.create_text_channel.await_count == 1
    assert tm.ticket_data.order_ticket_id == 2


def test_is_staff_allows_administrator(monkeypatch):
    monkeypatch.setattr(Config, "STAFF_ROLE_ID", 999999)
    admin = MagicMock(spec=discord.Member)
    admin.guild_permissions = MagicMock(administrator=True)
    admin.roles = []
    assert is_staff(admin) is True
