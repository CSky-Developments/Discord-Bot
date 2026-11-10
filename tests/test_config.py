import os
import pytest
from bot.config import Config

def test_config_parsing(tmp_path):
    yaml_file = tmp_path / "config.yml"
    yaml_file.write_text("""
Token: "TEST_TOKEN"
AI-Key: "TEST_AI_KEY"
Guild-ID: "1111724818614722690"
Log-Channel-ID: "1111724820086915158"
Staff-Role-ID: "1384520568451108974"
Member-Role-ID: "1111724818614722697"
Plugin-Gen-Access-Role-ID: "1459133869977632848"
Counting-Channel-ID: "1172387394356510803"
Member-Count-Channel-ID: "1113098819257761813"
Ticket-Channel-ID: "1114831112439607356"
Ticket-Order-Category: "1118890322735407214"
Ticket-Plugin-Generation-Category: "1459233399175643319"
Ticket-Reward-Category: "1118943418597515355"
Ticket-Normal-Category: "1112389077547896842"
Ticket-Staff-App-Category: "1117767193933905921"
Support-Category-ID: "1112388539083128933"
License-Gen-Access-IDs:
  - "793030841449840641"
  - "648009919303254026"
  - "1109014350380945478"
""", encoding="utf-8")

    Config.load(str(yaml_file))

    assert Config.TOKEN == "TEST_TOKEN"
    assert Config.AI_KEY == "TEST_AI_KEY"
    assert Config.GUILD_ID == 1111724818614722690
    assert Config.LOG_CHANNEL_ID == 1111724820086915158
    assert Config.STAFF_ROLE_ID == 1384520568451108974
    assert Config.MEMBER_ROLE_ID == 1111724818614722697
    assert Config.COUNTING_CHANNEL_ID == 1172387394356510803
    assert Config.MEMBER_COUNT_CHANNEL_ID == 1113098819257761813
    assert Config.TICKET_CHANNEL_ID == 1114831112439607356
    assert Config.TICKET_ORDER == 1118890322735407214
    assert Config.TICKET_PLUGIN_GEN == 1459233399175643319
    assert Config.TICKET_REWARD == 1118943418597515355
    assert Config.TICKET_NORMAL == 1112389077547896842
    assert Config.TICKET_STAFF_APP == 1117767193933905921
    assert Config.SUPPORT_CATEGORY_ID == 1112388539083128933
    assert Config.PLUGIN_GEN_ACCESS_ROLE_ID == 1459133869977632848
    assert Config.LICENSE_GEN_ACCESS_ID_LIST == ["793030841449840641", "648009919303254026", "1109014350380945478"]

def test_config_env_override(tmp_path, monkeypatch):
    monkeypatch.setenv("DISCORD_TOKEN", "OVERRIDDEN_TOKEN")
    monkeypatch.setenv("GUILD_ID", "999888777")
    monkeypatch.setenv("LICENSE_GEN_ACCESS_IDS", "user1,user2")

    yaml_file = tmp_path / "config.yml"
    yaml_file.write_text("""
Token: "YAML_TOKEN"
AI-Key: "TEST_AI_KEY"
Guild-ID: "111"
Log-Channel-ID: "1111724820086915158"
Staff-Role-ID: "1384520568451108974"
Member-Role-ID: "1111724818614722697"
Plugin-Gen-Access-Role-ID: "1459133869977632848"
Counting-Channel-ID: "1172387394356510803"
Member-Count-Channel-ID: "1113098819257761813"
Ticket-Channel-ID: "1114831112439607356"
Ticket-Order-Category: "1118890322735407214"
Ticket-Plugin-Generation-Category: "1459233399175643319"
Ticket-Reward-Category: "1118943418597515355"
Ticket-Normal-Category: "1112389077547896842"
Ticket-Staff-App-Category: "1117767193933905921"
Support-Category-ID: "1112388539083128933"
License-Gen-Access-IDs:
  - "yaml_user"
""", encoding="utf-8")

    Config.load(str(yaml_file))

    assert Config.TOKEN == "OVERRIDDEN_TOKEN"
    assert Config.GUILD_ID == 999888777
    assert Config.LICENSE_GEN_ACCESS_ID_LIST == ["user1", "user2"]
