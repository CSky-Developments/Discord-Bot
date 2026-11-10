import pytest
from unittest.mock import AsyncMock, MagicMock
import discord
from bot.game.counting import CountingGame, COUNTING_GOALS
from bot.config import Config

@pytest.fixture
def counting_game(tmp_path):
    data_file = tmp_path / "counting_data.json"
    game = CountingGame(str(data_file))
    Config.COUNTING_CHANNEL_ID = 12345
    return game

@pytest.mark.asyncio
async def test_counting_success(counting_game):
    message = AsyncMock(spec=discord.Message)
    message.channel.id = 12345
    message.channel.name = "counting"
    message.author.bot = False
    message.author.id = 101
    message.author.name = "TestUser"
    message.author.mention = "<@101>"
    message.content = "1"
    message.guild = MagicMock()
    message.guild.emojis = []

    await counting_game.handle_message(message)

    assert counting_game.current_count == 2
    assert counting_game.last_counter_id == "101"

@pytest.mark.asyncio
async def test_counting_double_count(counting_game):
    counting_game.current_count = 2
    counting_game.last_counter_id = "101"

    message = AsyncMock(spec=discord.Message)
    message.channel.id = 12345
    message.channel.name = "counting"
    message.author.bot = False
    message.author.id = 101
    message.author.name = "TestUser"
    message.author.mention = "<@101>"
    message.content = "2"
    message.guild = MagicMock()
    message.guild.emojis = []

    await counting_game.handle_message(message)

    message.reply.assert_called_once()
    assert "can't count twice in a row" in message.reply.call_args[0][0]
    assert counting_game.current_count == 1
    assert counting_game.last_counter_id is None

@pytest.mark.asyncio
async def test_counting_wrong_number(counting_game):
    counting_game.current_count = 5
    counting_game.last_counter_id = "101"

    message = AsyncMock(spec=discord.Message)
    message.channel.id = 12345
    message.channel.name = "counting"
    message.author.bot = False
    message.author.id = 102
    message.author.name = "AnotherUser"
    message.content = "7"
    message.guild = MagicMock()
    message.guild.emojis = []

    await counting_game.handle_message(message)

    message.reply.assert_called_once()
    assert "Sike!" in message.reply.call_args[0][0]
    assert "Number should be 5" in message.reply.call_args[0][0]
    assert counting_game.current_count == 1
    assert counting_game.last_counter_id is None

@pytest.mark.asyncio
async def test_counting_goal_reached(counting_game):
    counting_game.current_count = 10
    counting_game.last_counter_id = "101"

    message = AsyncMock(spec=discord.Message)
    message.channel.id = 12345
    message.channel.name = "counting"
    message.author.bot = False
    message.author.id = 102
    message.author.name = "MilestoneUser"
    message.author.mention = "<@102>"
    message.content = "10"
    message.guild = MagicMock()
    message.guild.emojis = []

    await counting_game.handle_message(message)

    message.reply.assert_called_once()
    assert "Hooray!" in message.reply.call_args[0][0]
    assert counting_game.current_count == 11
    assert counting_game.last_counter_id == "102"
