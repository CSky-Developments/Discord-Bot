from urllib.parse import urlencode
import aiohttp
import discord
from discord import app_commands

from bot.config import Config
from bot.commands.ticket import is_staff, make_no_permission_embed
from bot.embeds.help_embeds import FOOTER_ICON


def _format_display_amount(amount: float, currency: str) -> str:
    if currency.upper() == "INR":
        return f"₹{amount:,.0f}" if float(amount).is_integer() else f"₹{amount:,.2f}"
    return f"${amount:,.2f}"


class PayLinkView(discord.ui.View):
    def __init__(self, pay_url: str):
        super().__init__(timeout=None)
        self.add_item(
            discord.ui.Button(
                label="Pay Now",
                style=discord.ButtonStyle.link,
                url=pay_url,
            )
        )


def setup_pay_command(tree: app_commands.CommandTree, guild: discord.Object):
    pay_group = app_commands.Group(
        name="pay",
        description="CSky Payment Gateway commands & invoice links",
    )

    @pay_group.command(name="link", description="Get the public CSky Payment Gateway link")
    async def pay_link(interaction: discord.Interaction):
        url = Config.PAYMENT_GATEWAY_URL.rstrip("/")
        embed = discord.Embed(
            title="CSky Payment Gateway",
            description=(
                "Send payments securely via UPI, Cards, or NetBanking on our official gateway.\n"
                f"**Gateway:** {url}"
            ),
            color=0x1A73E8,
        )
        embed.set_footer(text="CSky Payment Gateway • payment.csky.dev", icon_url=FOOTER_ICON)
        await interaction.response.send_message(embed=embed, view=PayLinkView(url))

    @pay_group.command(name="create", description="Create a tracked payment link for a client (Staff)")
    @app_commands.describe(
        amount="Amount to request (e.g. 500 for INR or 15 for USD)",
        currency="Currency code (INR or USD)",
        note="Purpose / commission / invoice note",
        client="Optional Discord member to tag",
    )
    @app_commands.choices(
        currency=[
            app_commands.Choice(name="INR (₹)", value="INR"),
            app_commands.Choice(name="USD ($)", value="USD"),
        ]
    )
    async def pay_create(
        interaction: discord.Interaction,
        amount: float,
        currency: str = "INR",
        note: str = "CSky Studio Payment",
        client: discord.Member | None = None,
    ):
        if not is_staff(interaction.user):
            await interaction.response.send_message(
                embed=make_no_permission_embed(), ephemeral=True, delete_after=10
            )
            return

        if amount < 1:
            await interaction.response.send_message(
                "Amount must be at least 1.", ephemeral=True, delete_after=10
            )
            return

        await interaction.response.defer()
        curr = currency.upper()
        base_url = Config.PAYMENT_GATEWAY_URL.rstrip("/")
        pay_url = f"{base_url}/?{urlencode({'amount': str(amount), 'currency': curr, 'note': note})}"
        reference = "DIRECT"

        backend_url = Config.BACKEND_API_URL.rstrip("/")
        secret = Config.INTERNAL_API_SECRET
        if backend_url and secret:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        f"{backend_url}/api/pay/link",
                        headers={
                            "Content-Type": "application/json",
                            "x-csky-internal-secret": secret,
                        },
                        json={
                            "amount": amount,
                            "currency": curr,
                            "title": "CSky Studio Invoice",
                            "note": note,
                            "discordUserId": str(client.id) if client else None,
                            "discordTag": str(client) if client else None,
                            "discordChannelId": str(interaction.channel_id) if interaction.channel_id else None,
                        },
                        timeout=aiohttp.ClientTimeout(total=8),
                    ) as resp:
                        if resp.status in (200, 201):
                            data = await resp.json()
                            if data.get("url"):
                                pay_url = data["url"]
                            if data.get("reference"):
                                reference = data["reference"]
            except Exception:
                pass

        amount_display = _format_display_amount(amount, curr)
        embed = discord.Embed(
            title=f"Payment Request — {amount_display} {curr}",
            url=pay_url,
            description=(
                f"**Purpose:** {note}\n"
                f"**Reference:** `{reference}`\n\n"
                "Click **Pay Now** below to complete your payment securely via Razorpay. "
                "Confirmation will be posted automatically once verified."
            ),
            color=0x1A73E8,
        )
        if client:
            embed.add_field(name="Requested From", value=client.mention, inline=True)
        embed.add_field(name="Amount", value=f"`{amount_display} {curr}`", inline=True)
        embed.set_footer(text="CSky Payment Gateway • payment.csky.dev", icon_url=FOOTER_ICON)
        embed.timestamp = discord.utils.utcnow()

        content = client.mention if client else None
        await interaction.followup.send(
            content=content,
            embed=embed,
            view=PayLinkView(pay_url),
        )

    @pay_group.command(name="status", description="Check payment status by reference ID (Staff)")
    @app_commands.describe(reference="Gateway reference ID (e.g. CSKY-PAY-A1B2C3D4)")
    async def pay_status(interaction: discord.Interaction, reference: str):
        if not is_staff(interaction.user):
            await interaction.response.send_message(
                embed=make_no_permission_embed(), ephemeral=True, delete_after=10
            )
            return

        await interaction.response.defer(ephemeral=True)
        ref = reference.strip()
        backend_url = Config.BACKEND_API_URL.rstrip("/")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{backend_url}/api/pay/status/{ref}",
                    timeout=aiohttp.ClientTimeout(total=8),
                ) as resp:
                    if resp.status == 404:
                        await interaction.followup.send(f"No payment found for `{ref}`.", ephemeral=True)
                        return
                    if resp.status != 200:
                        await interaction.followup.send(f"Lookup failed (HTTP {resp.status}).", ephemeral=True)
                        return
                    data = await resp.json()
                    p = data.get("payment") or {}
        except Exception as exc:
            await interaction.followup.send(f"Could not reach payment backend: `{exc}`", ephemeral=True)
            return

        status = str(p.get("status", "unknown")).upper()
        curr = str(p.get("currency", "INR")).upper()
        amt = float(p.get("displayAmount", 0))
        color = 0x16A34A if status == "PAID" else 0xF59E0B
        embed = discord.Embed(
            title=f"Payment Status — {ref}",
            color=color,
        )
        embed.add_field(name="Status", value=f"`{status}`", inline=True)
        embed.add_field(name="Amount", value=f"`{_format_display_amount(amt, curr)} {curr}`", inline=True)
        if p.get("razorpayPaymentId"):
            embed.add_field(name="Razorpay ID", value=f"`{p['razorpayPaymentId']}`", inline=True)
        if p.get("note"):
            embed.add_field(name="Note", value=str(p["note"]), inline=False)
        embed.set_footer(text="CSky Payment Gateway • payment.csky.dev", icon_url=FOOTER_ICON)
        await interaction.followup.send(embed=embed, ephemeral=True)

    tree.add_command(pay_group, guild=guild)
