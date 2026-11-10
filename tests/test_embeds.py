import pytest
import discord
from bot import embeds

def test_help_embeds():
    emb = embeds.make_help_embed()
    assert isinstance(emb, discord.Embed)
    assert emb.title == "CSky Developments - Help Menu"
    assert emb.footer.text == embeds.FOOTER_TEXT

    not_avail = embeds.make_not_available_embed()
    assert isinstance(not_avail, discord.Embed)
    assert "currently not available" in not_avail.description

def test_reward_embeds():
    inv_emb = embeds.make_invite_reward_embed()
    assert isinstance(inv_emb, discord.Embed)
    assert inv_emb.title == "Invite・Rewards"

    boost_emb = embeds.make_booster_reward_embed()
    assert isinstance(boost_emb, discord.Embed)
    assert boost_emb.title == "Boost・Rewards"

def test_service_embeds():
    building = embeds.make_building_embed()
    assert isinstance(building, discord.Embed)
    assert building.title == "Build・Building"

    setup = embeds.make_server_setup_embed()
    assert isinstance(setup, discord.Embed)
    assert setup.title == "Server・Setup"

    dirt = embeds.make_dirt_plan_embed()
    assert isinstance(dirt, discord.Embed)
    assert dirt.title == "Dirt Plan"

    service_order = embeds.make_service_order_embed()
    assert isinstance(service_order, discord.Embed)
    assert "Place Order" in service_order.description

def test_ticket_embeds():
    tick = embeds.make_ticket_embed()
    assert isinstance(tick, discord.Embed)
    assert tick.title == "**Ticket**"

    tick_create = embeds.make_ticket_create_embed()
    assert isinstance(tick_create, discord.Embed)
    assert "Thank you for creating a ticket" in tick_create.title

    dev_q = embeds.make_developer_questions_embed()
    assert isinstance(dev_q, discord.Embed)
    assert "Answer the following" in dev_q.title
