from typing import Any
import aiohttp
import discord
from discord import app_commands

from bot.config import Config
from bot.embeds.help_embeds import CSKY_AUTH_URL, CSKY_STORE_URL, FOOTER_ICON, FOOTER_TEXT
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


def make_buyer_sync_embed(member_name: str, data: dict[str, Any], role_granted: bool) -> discord.Embed:
    products = data.get("products") or []
    product_list = ", ".join(f"`{p}`" for p in products[:8]) if products else "Verified Store Order"
    status_line = "Buyer role granted!" if role_granted else "Your Buyer role is already active."

    embed = discord.Embed(
        title="CSky Store — Buyer Verified",
        description=(
            f"{status_line}\n\n"
            f"• **Account:** `{member_name}`\n"
            f"• **Completed Orders:** `{data.get('completedOrders', 0)}`\n"
            f"• **Active Licenses:** `{data.get('activeLicenses', 0)}`\n"
            f"• **Products:** {product_list}"
        ),
        color=0x16A34A,
    )
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed


def setup_buyer_command(tree: app_commands.CommandTree, guild: discord.Object):
    @tree.command(
        name="claim-buyer",
        description="Sync your store.csky.dev purchases and claim your Discord Buyer role.",
        guild=guild,
    )
    async def claim_buyer_cmd(interaction: discord.Interaction):
        if not Config.BUYER_ROLE_ID or not Config.INTERNAL_API_SECRET:
            await interaction.response.send_message(
                "⚠️ Buyer role sync is not configured on this server yet. Please contact staff in a ticket.",
                ephemeral=True,
            )
            return

        if not isinstance(interaction.user, discord.Member) or not interaction.guild:
            await interaction.response.send_message("❌ This command can only be used inside the server.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True, thinking=True)
        data = await fetch_buyer_status(interaction.user.id, interaction.user.name)

        if data is None:
            await interaction.followup.send(
                f"⚠️ Could not reach `store.csky.dev` right now. Please try again shortly.",
                ephemeral=True,
            )
            return

        if not data.get("linked"):
            await interaction.followup.send(
                f"❌ No `store.csky.dev` account is linked to your Discord yet.\n"
                f"Sign in with **Discord** at {CSKY_AUTH_URL} or {CSKY_STORE_URL}, then run `/claim-buyer` again.",
                ephemeral=True,
            )
            return

        if not data.get("isBuyer"):
            await interaction.followup.send(
                f"ℹ️ Your account is linked, but no completed orders or active licenses were found yet.\n"
                f"Browse plugins & setups at {CSKY_STORE_URL}.",
                ephemeral=True,
            )
            return

        role = interaction.guild.get_role(Config.BUYER_ROLE_ID)
        if not role:
            await interaction.followup.send(
                "⚠️ Configured Buyer role was not found in this server. Please notify staff.",
                ephemeral=True,
            )
            return

        role_granted = False
        if role not in interaction.user.roles:
            try:
                await interaction.user.add_roles(role, reason="Self-service /claim-buyer sync")
                role_granted = True
            except Exception:
                await interaction.followup.send(
                    "⚠️ I don't have permission to assign the Buyer role. Please notify staff.",
                    ephemeral=True,
                )
                return

        await interaction.followup.send(
            embed=make_buyer_sync_embed(interaction.user.display_name, data, role_granted),
            ephemeral=True,
        )
