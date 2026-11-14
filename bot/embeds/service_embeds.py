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
            "Production-grade Minecraft engineering built for **20.0 TPS** stability.\n"
            f"Submit a brief at **[csky.dev/contact]({CSKY_WEBSITE_URL}/contact)** or click **Place Order** below.\n\n"
            "### What We Build\n"
            "> **Custom Plugins** — Paper 26.3, Purpur, Folia & Velocity (`Java 21 LTS`)\n"
            "> **Resource Packs** — 16x–128x textures, GUIs & `Format 97.1`\n"
            "> **Optimization** — Spark profiling, JVM/GC & database tuning\n"
            "> **Server Setups** — Complete SMP, PvP & network architectures\n\n"
            "### Commission Tracks\n"
            "> **Public Track (40%–60% Off)** — Discounted rate; compiled `.jar` with `CLE v1` *(CSky retains BuiltByBit rights)*\n"
            "> **Private Track (100% Exclusive)** — Full IP ownership, uncompiled Java/Kotlin source & private war room\n\u200b"
        ),
        color=0x1A73E8,
    )
    embed.set_author(
        name="CSky Developments",
        url=CSKY_SERVICES_URL,
        icon_url=FOOTER_ICON,
    )
    embed.add_field(
        name="Workflow",
        value=(
            "1. Quote (`< 24h`)\n"
            "2. 50% Deposit\n"
            "3. Staging Test\n"
            "4. 50% Handoff"
        ),
        inline=True,
    )
    embed.add_field(
        name="Tech Stack",
        value=(
            "Paper 26.3 / Purpur\n"
            "Folia & Velocity\n"
            "Java 21 / Kotlin\n"
            "Postgres & Redis"
        ),
        inline=True,
    )
    embed.add_field(
        name="Guarantees",
        value=(
            "20.0 TPS Target\n"
            "14-Day Warranty\n"
            "Tebex / Stripe / UPI\n"
            "Killer_Nova & Arsh"
        ),
        inline=True,
    )
    embed.set_image(url=f"{CSKY_WEBSITE_URL}/og-cover.png")
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed
