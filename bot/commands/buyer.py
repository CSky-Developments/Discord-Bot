"""Automatic Discord Buyer role synchronization on member join."""

from typing import Any
import aiohttp
import discord

from bot.config import Config
from bot.embeds.help_embeds import CSKY_STORE_URL
from bot.logger import BotLogger


async def fetch_buyer_status(discord_id: int, discord_tag: str) -> dict[str, Any] | None:
    if not Config.INTERNAL_API_SECRET:
        return None

    base_url = (Config.STORE_API_URL or CSKY_STORE_URL).rstrip("/")
    params = {"discordId": str(discord_id), "discordTag": discord_tag}
    headers = {"x-csky-internal-secret": Config.INTERNAL_API_SECRET}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{base_url}/api/internal/buyer",
                params=params,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=6),
            ) as resp:
                if resp.status != 200:
                    return None
                return await resp.json()
    except Exception as exc:
        BotLogger.warn(f"Buyer status check failed for {discord_id}: {exc}", False)
        return None


async def sync_buyer_role(member: discord.Member) -> bool:
    """Silently check store.csky.dev and grant the Buyer role if verified."""
    if not Config.BUYER_ROLE_ID or not Config.INTERNAL_API_SECRET:
        return False

    role = member.guild.get_role(Config.BUYER_ROLE_ID)
    if not role or role in member.roles:
        return False

    data = await fetch_buyer_status(member.id, member.name)
    if not data or not data.get("isBuyer"):
        return False

    try:
        await member.add_roles(role, reason="Automatic CSky Store buyer sync")
        BotLogger.info(f"Granted Buyer role to {member.name} ({member.id})", True)
        return True
    except Exception as exc:
        BotLogger.warn(f"Failed to add Buyer role to {member.id}: {exc}", False)
        return False
