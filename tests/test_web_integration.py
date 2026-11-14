from unittest.mock import AsyncMock, MagicMock, patch
import discord
import pytest

from bot.commands.buyer import make_buyer_sync_embed, sync_buyer_role
from bot.commands.links import make_links_embed, make_status_embed
from bot.commands.store import (
    create_store_view,
    format_price,
    make_store_product_embed,
    make_store_search_embed,
)
from bot.embeds import help_embeds, ticket_embeds
from bot.ticket import buttons


def test_links_embed_and_view():
    emb = make_links_embed()
    assert isinstance(emb, discord.Embed)
    assert "csky.dev" in emb.description
    assert "store.csky.dev" in emb.description
    assert "crafter.csky.dev" in emb.description
    assert "auth.csky.dev" in emb.description


@pytest.mark.asyncio
async def test_web_link_views_inside_event_loop():
    links_view = buttons.create_links_view()
    urls = [item.url for item in links_view.children if isinstance(item, discord.ui.Button)]
    assert "https://csky.dev" in urls
    assert "https://store.csky.dev" in urls
    assert "https://crafter.csky.dev" in urls
    assert "https://auth.csky.dev" in urls
    assert "https://csky.dev/terms" in urls

    order_view = buttons.create_order_create_view()
    order_urls = [item.url for item in order_view.children if getattr(item, "url", None)]
    assert "https://csky.dev/services" in order_urls
    assert "https://csky.dev/terms" in order_urls

    store_view = create_store_view("https://store.csky.dev/products/scores-smp", label="View on Store")
    store_urls = [item.url for item in store_view.children if getattr(item, "url", None)]
    assert "https://store.csky.dev/products/scores-smp" in store_urls
    assert "https://store.csky.dev" in store_urls


def test_status_embed():
    emb_ok = make_status_embed([("Website", True, 42, "HTTP 200")])
    assert emb_ok.color.value == 0x16A34A
    assert "Operational" in emb_ok.fields[0].value

    emb_deg = make_status_embed([("Website", True, 42, "HTTP 200"), ("API", False, 5000, "TimeoutError")])
    assert emb_deg.color.value == 0xF59E0B
    assert "Degraded" in emb_deg.fields[1].value


def test_store_formatting_and_embeds():
    assert format_price(0, 0) == "Free"
    assert format_price(9.99, 850) == "$9.99 (₹850)"
    assert format_price(12.0, None) == "$12"

    sample = {
        "title": "Scores SMP",
        "slug": "scores-smp",
        "category": "Plugins",
        "tagline": "Competitive SMP core with elemental scores.",
        "price": 14.99,
        "priceInr": 1299,
        "version": "2.0.0",
        "minecraftVersions": ["1.21.4", "26.3"],
        "testedEngine": "Paper 26.3",
        "features": ["Elemental scores", "Altar trials"],
        "rating": 4.9,
        "reviewsCount": 12,
    }
    search_emb = make_store_search_embed([sample], query="scores")
    assert len(search_emb.fields) == 1
    assert "Scores SMP" in search_emb.fields[0].name
    assert "$14.99 (₹1299)" in search_emb.fields[0].name

    empty_emb = make_store_search_embed([], query="missing")
    assert "No matching products found" in empty_emb.fields[0].name

    detail_emb = make_store_product_embed(sample)
    assert detail_emb.title == "Scores SMP"
    assert detail_emb.url == "https://store.csky.dev/products/scores-smp"


def test_updated_ticket_and_help_embeds():
    help_emb = help_embeds.make_help_embed()
    assert "c!" not in help_emb.description
    assert "/store search" in help_emb.fields[0].value

    order_create = ticket_embeds.make_order_create_embed()
    assert "Killer_Nova" in order_create.description
    assert "csky.dev/terms" in order_create.description


@pytest.mark.asyncio
async def test_buyer_sync_embed_and_role_grant(monkeypatch):
    from bot.config import Config

    monkeypatch.setattr(Config, "BUYER_ROLE_ID", 999)
    monkeypatch.setattr(Config, "INTERNAL_API_SECRET", "test-secret")

    role = MagicMock(spec=discord.Role)
    member = MagicMock(spec=discord.Member)
    member.id = 12345
    member.name = "arsh"
    member.roles = []
    member.guild = MagicMock()
    member.guild.get_role.return_value = role
    member.add_roles = AsyncMock()

    with patch("bot.commands.buyer.fetch_buyer_status", AsyncMock(return_value={
        "linked": True,
        "isBuyer": True,
        "completedOrders": 2,
        "activeLicenses": 1,
        "products": ["Scores SMP"],
    })):
        granted = await sync_buyer_role(member)
        assert granted is True
        member.add_roles.assert_awaited_once()

    emb = make_buyer_sync_embed("Arsh", {
        "completedOrders": 2,
        "activeLicenses": 1,
        "products": ["Scores SMP"],
    }, role_granted=True)
    assert "Buyer role granted!" in emb.description
    assert "Scores SMP" in emb.description
