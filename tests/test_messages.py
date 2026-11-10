from unittest.mock import MagicMock
import pytest
from bot.message.manager import MessageManager, MessageEntry

def test_message_caching():
    mm = MessageManager(cache_limit=3)
    
    msg1 = MagicMock()
    msg1.author.bot = False
    msg1.channel.id = 123
    msg1.content = "Hello 1"
    msg1.id = 1001
    msg1.author.id = 555
    
    mm.handle_message(msg1)
    assert "1001" in mm.message_cache
    assert mm.message_cache["1001"].content == "Hello 1"

    # Add 3 more to test LRU eviction
    for i in range(2, 5):
        m = MagicMock()
        m.author.bot = False
        m.channel.id = 123
        m.content = f"Hello {i}"
        m.id = 1000 + i
        m.author.id = 555
        mm.handle_message(m)

    assert len(mm.message_cache) == 3
    # 1001 should have been evicted
    assert "1001" not in mm.message_cache
    assert "1004" in mm.message_cache

def test_message_delete_logging(monkeypatch):
    mm = MessageManager(cache_limit=10)
    mm.message_cache["2001"] = MessageEntry("Secret message", "12345", 100.0)

    logged = []
    monkeypatch.setattr("bot.logger.BotLogger.info", lambda msg, discord=False: logged.append(msg))

    mock_event = MagicMock()
    mock_event.id = 2001
    mock_event.channel.name = "general"

    guild_mock = MagicMock()
    member_mock = MagicMock()
    member_mock.name = "Arsh"
    guild_mock.get_member.return_value = member_mock

    mm.handle_message_delete(mock_event, guild=guild_mock)
    
    assert "2001" not in mm.message_cache
    assert len(logged) == 1
    assert "Messages of `Arsh` was deleted in `general`" in logged[0]
    assert "Secret message" in logged[0]

def test_message_edit_logging(monkeypatch):
    mm = MessageManager(cache_limit=10)
    mm.message_cache["3001"] = MessageEntry("Before edit", "12345", 100.0)

    logged = []
    monkeypatch.setattr("bot.logger.BotLogger.info", lambda msg, discord=False: logged.append(msg))

    after_msg = MagicMock()
    after_msg.author.bot = False
    after_msg.channel.id = 999
    after_msg.channel.name = "announcements"
    after_msg.id = 3001
    after_msg.author.name = "Arsh"
    after_msg.content = "After edit"

    mm.handle_message_edit(None, after_msg)

    assert mm.message_cache["3001"].content == "After edit"
    assert len(logged) == 1
    assert "`Arsh` edited their message in `announcements`" in logged[0]
    assert "Original: Before edit" in logged[0]
    assert "Edited: After edit" in logged[0]
