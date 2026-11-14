import hmac
from typing import Optional
import discord
from aiohttp import web

from bot.config import Config
from bot.embeds.help_embeds import FOOTER_TEXT, FOOTER_ICON
from bot.logger import BotLogger
from bot.ticket import buttons


def _clean_text(value: object, max_len: int) -> str:
    if not isinstance(value, str):
        return ""
    return value.strip()[:max_len]


def build_commission_embed(data: dict) -> discord.Embed:
    name = _clean_text(data.get("name"), 100) or "Unknown Client"
    contact = _clean_text(data.get("contactHandle"), 150) or "Not provided"
    track = _clean_text(data.get("track"), 150) or "Private Track (100% Exclusive & Full Source)"
    service = _clean_text(data.get("serviceType"), 120) or "Custom Plugin Development"
    budget = _clean_text(data.get("budget"), 60) or "Not specified"
    details = _clean_text(data.get("details"), 1800) or "No specifications provided."

    is_public = "public" in track.lower()
    embed_color = 0x137333 if is_public else 0x1A73E8
    track_badge = (
        "Public Track (40-60% Discounted)"
        if is_public
        else "Private Track (100% Exclusive)"
    )
    safe_details = f"{details[:997]}..." if len(details) > 1000 else details

    embed = discord.Embed(
        title=f"New Commission Request — {service}",
        url="https://csky.dev/contact",
        color=embed_color,
    )
    embed.add_field(name="Client", value=name, inline=True)
    embed.add_field(name="Contact", value=f"`{contact}`", inline=True)
    embed.add_field(name="Estimated Budget", value=f"`{budget}`", inline=True)
    embed.add_field(name="Commission Track", value=track_badge, inline=False)
    embed.add_field(name="Project Specifications & Ideas", value=safe_details, inline=False)
    embed.set_footer(text="CSky Developments • csky.dev/contact", icon_url=FOOTER_ICON)
    embed.timestamp = discord.utils.utcnow()
    return embed


async def start_internal_api(bot: discord.Client) -> Optional[web.AppRunner]:
    async def health(_request: web.Request) -> web.Response:
        return web.json_response({"ok": True})

    async def handle_commission(request: web.Request) -> web.Response:
        expected_secret = Config.INTERNAL_API_SECRET
        if not expected_secret:
            return web.json_response(
                {"error": "INTERNAL_API_SECRET is not configured on bot"},
                status=503,
            )

        provided_secret = request.headers.get("x-csky-internal-secret", "")
        if not provided_secret or not hmac.compare_digest(provided_secret, expected_secret):
            return web.json_response({"error": "Unauthorized"}, status=401)

        try:
            payload = await request.json()
        except Exception:
            return web.json_response({"error": "Invalid JSON body"}, status=400)

        if not isinstance(payload, dict):
            return web.json_response({"error": "JSON object required"}, status=400)

        guild = getattr(bot, "guild_obj", None)
        if not guild:
            return web.json_response({"error": "Bot guild is not ready"}, status=503)

        channel_id = Config.REQUESTS_CHANNEL_ID
        if not channel_id:
            return web.json_response(
                {"error": "REQUESTS_CHANNEL_ID is not configured on bot"},
                status=503,
            )

        channel = guild.get_channel(channel_id)
        if not isinstance(channel, discord.TextChannel):
            return web.json_response(
                {"error": f"Requests channel {channel_id} not found"},
                status=500,
            )

        embed = build_commission_embed(payload)
        msg = await channel.send(embed=embed, view=buttons.create_commission_request_view())
        return web.json_response({"ok": True, "messageId": str(msg.id)})

    app = web.Application()
    app.router.add_get("/health", health)
    app.router.add_post("/internal/commission", handle_commission)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", Config.INTERNAL_HTTP_PORT)
    await site.start()
    BotLogger.info(f"Internal bot API listening on 0.0.0.0:{Config.INTERNAL_HTTP_PORT}", False)
    return runner
