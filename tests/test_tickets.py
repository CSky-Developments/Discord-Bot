import os
import json
from unittest.mock import MagicMock
import pytest
from bot.ticket.manager import TicketManager, TicketData
from bot.ticket.types import TicketType

def test_ticket_data_serialization():
    data = TicketData()
    data.normal_ticket_id = 42
    data.order_ticket_id = 15
    data.plugin_gen_ticket_id = 7
    data.reward_ticket_id = 3
    data.staff_app_ticket_id = 99

    d = data.to_dict()
    assert d == {
        "normalTicketID": 42,
        "orderTicketID": 15,
        "pluginGenTicketID": 7,
        "rewardTicketID": 3,
        "staffAppTicketID": 99,
    }

    reloaded = TicketData.from_dict(d)
    assert reloaded.normal_ticket_id == 42
    assert reloaded.order_ticket_id == 15
    assert reloaded.plugin_gen_ticket_id == 7
    assert reloaded.reward_ticket_id == 3
    assert reloaded.staff_app_ticket_id == 99

def test_ticket_id_increment_and_rollover(tmp_path):
    data_file = tmp_path / "test_ticket_data.json"
    guild_mock = MagicMock()

    tm = TicketManager(guild=guild_mock, data_file=str(data_file))
    
    # Check initial ID formatting
    id1 = tm.get_ticket_id(TicketType.NORMAL)
    assert id1 == "0001"
    assert tm.ticket_data.normal_ticket_id == 2

    id2 = tm.get_ticket_id(TicketType.NORMAL)
    assert id2 == "0002"

    # Test rollover at 9999
    tm.ticket_data.normal_ticket_id = 9999
    id_9999 = tm.get_ticket_id(TicketType.NORMAL)
    assert id_9999 == "9999"
    assert tm.ticket_data.normal_ticket_id == 0

    id_0000 = tm.get_ticket_id(TicketType.NORMAL)
    assert id_0000 == "0000"

    # Check persistence on disk
    with open(str(data_file), "r", encoding="utf-8") as f:
        disk_data = json.load(f)
    assert disk_data["normalTicketID"] == 1
