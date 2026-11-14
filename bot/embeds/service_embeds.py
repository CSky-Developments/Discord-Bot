import discord
from bot.embeds.help_embeds import (
    FOOTER_TEXT,
    FOOTER_ICON,
    CSKY_WEBSITE_URL,
    CSKY_SERVICES_URL,
    CSKY_TERMS_URL,
    CSKY_STORE_URL,
)


def make_service_order_embed(color: int = 0x1A73E8) -> discord.Embed:
    embed = discord.Embed(
        title="Order Service",
        description=(
            "To place an order, click **Place Order** below or submit your specs on our website.\n\n"
            f"• **Request Form:** [csky.dev/contact]({CSKY_WEBSITE_URL}/contact)\n"
            f"• **Services & Stack:** [csky.dev/services]({CSKY_SERVICES_URL})\n"
            f"• **Ready-Made Store:** [store.csky.dev]({CSKY_STORE_URL})\n"
            f"• **Terms & 14-Day Warranty:** [csky.dev/terms]({CSKY_TERMS_URL})"
        ),
        color=color,
    )
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed


def make_custom_work_embed() -> discord.Embed:
    embed = discord.Embed(
        title="Custom Work & Commissions",
        url=f"{CSKY_WEBSITE_URL}/contact",
        description=(
            "Custom Minecraft engineering built for **20.0 TPS** performance.\n"
            f"Click **Place Order** below or submit a brief at **[csky.dev/contact]({CSKY_WEBSITE_URL}/contact)**."
        ),
        color=0x1A73E8,
    )
    embed.add_field(
        name="Services",
        value=(
            "• **Custom Plugins** — Paper 26.3, Purpur, Folia, Velocity (Java 21)\n"
            "• **Resource Packs** — 16x–128x textures, custom GUIs, Format `97.1`\n"
            "• **Optimization** — Spark profiling, JVM/GC & database tuning\n"
            "• **Server Setups** — Complete SMP, PvP, and network architectures"
        ),
        inline=False,
    )
    embed.add_field(
        name="Commission Tracks",
        value=(
            "• **Public Track (40–60% Off)** — Discounted rate; compiled `.jar` with `CLE v1` (CSky retains BuiltByBit rights)\n"
            "• **Private Track (100% Exclusive)** — Full IP exclusivity, uncompiled Java/Kotlin source & private war room"
        ),
        inline=False,
    )
    embed.add_field(
        name="Billing & Warranty",
        value=(
            "50% upfront / 50% on delivery • 14-day bug fix warranty\n"
            "Authorized billing only by **Killer_Nova** or **Arsh** via **Tebex**, **Stripe**, or ticket-verified **UPI**."
        ),
        inline=False,
    )
    embed.set_thumbnail(url=FOOTER_ICON)
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed
