import pytest
from unittest.mock import MagicMock
from bot.invite.manager import InviteManager, InviteRecord

def test_invite_records(tmp_path):
    data_file = tmp_path / "invite_records.json"
    mgr = InviteManager(str(data_file))

    mgr.add_invite("101", "201")
    mgr.add_invite("101", "202")
    mgr.add_invite("102", "203")

    assert mgr.get_invites("101") == 2
    assert mgr.get_invites("102") == 1
    assert mgr.get_invites("999") == 0

    assert mgr.get_inviter_id("201") == "101"
    assert mgr.get_inviter_id("203") == "102"
    assert mgr.get_inviter_id("999") is None

    mgr.remove_invite("101", "201")
    assert mgr.get_invites("101") == 1
    assert mgr.get_inviter_id("201") is None

    mgr.reset_invites("101")
    assert mgr.get_invites("101") == 0

def test_invite_cache():
    mgr = InviteManager("/tmp/dummy.json")

    mock_invite1 = MagicMock()
    mock_invite1.code = "abc"
    mock_invite1.uses = 5

    mock_invite2 = MagicMock()
    mock_invite2.code = "xyz"
    mock_invite2.uses = 1

    mgr.cache_invites([mock_invite1, mock_invite2])
    assert mgr.invite_cache["abc"] == 5
    assert mgr.invite_cache["xyz"] == 1

    # Simulate updated invites
    mock_invite1_new = MagicMock()
    mock_invite1_new.code = "abc"
    mock_invite1_new.uses = 6

    mock_invite2_new = MagicMock()
    mock_invite2_new.code = "xyz"
    mock_invite2_new.uses = 1

    used = mgr.get_used_invite([mock_invite1_new, mock_invite2_new])
    assert used == mock_invite1_new
