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
    assert "currently unavailable" in not_avail.description

def test_service_embeds():
    custom_work = embeds.make_custom_work_embed()
    assert isinstance(custom_work, discord.Embed)
    assert "Custom Work" in custom_work.title
    assert custom_work.color.value == 0x1A73E8

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
    assert tick.title == "Support Ticket"

    tick_create = embeds.make_ticket_create_embed()
    assert isinstance(tick_create, discord.Embed)
    assert "Support Ticket Opened" in tick_create.title

    order_emb = embeds.make_order_embed()
    assert isinstance(order_emb, discord.Embed)
    assert "Commission & Order Service" in order_emb.title

    dev_q = embeds.make_developer_questions_embed()
    assert isinstance(dev_q, discord.Embed)
    assert "Answer the following" in dev_q.title
