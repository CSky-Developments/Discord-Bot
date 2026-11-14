"""Web ecosystem links and live platform health commands (/links, /status)."""

import time
import aiohttp
import discord
from discord import app_commands

from bot.embeds.help_embeds import (
    FOOTER_ICON,
    FOOTER_TEXT,
    CSKY_ANNOUNCEMENTS_URL,
    CSKY_API_URL,
    CSKY_AUTH_URL,
    CSKY_CRAFTER_URL,
    CSKY_SERVICES_URL,
    CSKY_STORE_URL,
    CSKY_TERMS_URL,
    CSKY_WEBSITE_URL,
)
from bot.ticket.buttons import create_links_view


HEALTH_ENDPOINTS = [
    ("Website (csky.dev)", f"{CSKY_WEBSITE_URL}/api/health"),
    ("Store (store.csky.dev)", f"{CSKY_STORE_URL}/api/health"),
    ("CSky Studio (crafter.csky.dev)", CSKY_CRAFTER_URL),
    ("Backend & CLE API (api.csky.dev)", f"{CSKY_API_URL}/health"),
]


def make_links_embed() -> discord.Embed:
    embed = discord.Embed(
        title="CSky Developments — Web Ecosystem",
        description=(
            "Explore our official platforms, store, and AI plugin studio:\n\n"
            f"• **Agency & Services:** [{CSKY_WEBSITE_URL}]({CSKY_WEBSITE_URL}) ([Services]({CSKY_SERVICES_URL}))\n"
            f"• **Digital Store:** [{CSKY_STORE_URL}]({CSKY_STORE_URL})\n"
            f"• **CSky Studio (AI Builder):** [{CSKY_CRAFTER_URL}]({CSKY_CRAFTER_URL})\n"
            f"• **Account & SSO Portal:** [{CSKY_AUTH_URL}]({CSKY_AUTH_URL})\n"
            f"• **Announcements:** [csky.dev/announcements]({CSKY_ANNOUNCEMENTS_URL})\n"
            f"• **Terms & Policies:** [csky.dev/terms]({CSKY_TERMS_URL})"
        ),
        color=0x2563EB,
    )
    embed.set_thumbnail(url=FOOTER_ICON)
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed


async def check_endpoint_health(session: aiohttp.ClientSession, name: str, url: str) -> tuple[str, bool, int, str]:
    start = time.monotonic()
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
            elapsed_ms = int((time.monotonic() - start) * 1000)
            ok = 200 <= resp.status < 400
            return (name, ok, elapsed_ms, f"HTTP {resp.status}")
    except Exception as exc:
        elapsed_ms = int((time.monotonic() - start) * 1000)
        return (name, False, elapsed_ms, type(exc).__name__)


def make_status_embed(results: list[tuple[str, bool, int, str]]) -> discord.Embed:
    all_ok = all(ok for _, ok, _, _ in results)
    embed = discord.Embed(
        title="CSky Platform Status",
        description="Live health check across CSky Developments web services:",
        color=0x16A34A if all_ok else 0xF59E0B,
    )
    for name, ok, elapsed_ms, detail in results:
        icon = "🟢" if ok else "🔴"
        state = "Operational" if ok else "Degraded"
        embed.add_field(
            name=f"{icon} {name}",
            value=f"`{state}` • `{elapsed_ms}ms` ({detail})",
            inline=False,
        )
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed


def setup_links_command(tree: app_commands.CommandTree, guild: discord.Object):
    @tree.command(name="links", description="View official CSky Developments websites, store, and studio links.", guild=guild)
    async def links_cmd(interaction: discord.Interaction):
        await interaction.response.send_message(embed=make_links_embed(), view=create_links_view())

    @tree.command(name="status", description="Check live uptime of CSky Developments web services.", guild=guild)
    async def status_cmd(interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        async with aiohttp.ClientSession() as session:
            results = []
            for name, url in HEALTH_ENDPOINTS:
                results.append(await check_endpoint_health(session, name, url))
        await interaction.followup.send(embed=make_status_embed(results))
