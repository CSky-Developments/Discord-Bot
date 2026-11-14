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
            "Production-grade Minecraft plugins, resource packs, and network setups engineered for **20.0 TPS** stability.\n\n"
            f"Submit a project brief at **[csky.dev/contact]({CSKY_WEBSITE_URL}/contact)** or click **Place Order** below to start a private ticket.\n\u200b"
        ),
        color=0x1A73E8,
    )
    embed.set_author(
        name="CSky Developments • csky.dev/services",
        url=CSKY_SERVICES_URL,
        icon_url=FOOTER_ICON,
    )
    embed.add_field(
        name="Core Engineering Services",
        value=(
            "• **Custom Plugin Development**\n"
            "  Paper 26.3, Purpur, Folia, and Velocity plugins in Java 21 LTS with async I/O, HikariCP/Redis sync, and zero main-thread stalls.\n\n"
            "• **Texture & Resource Packs**\n"
            "  Custom `16x`–`128x` item art, GUIs, and `Pack Format 97.1` bundles (`CustomModelData`, Oraxen / ItemsAdder ready).\n\n"
            "• **Server Optimization & Profiling**\n"
            "  Spark profiling audits, JVM & GC flag tuning, chunk/entity balancing, and database query optimization.\n\n"
            "• **Complete Server Setups**\n"
            "  End-to-end SMP, PvP, and multi-server network architectures configured and stress-tested for launch.\n\u200b"
        ),
        inline=False,
    )
    embed.add_field(
        name="Dual-Track Commission Model",
        value=(
            "• **Public Track (40%–60% Discounted)**\n"
            "  Subsidized upfront fee; delivered as a compiled `.jar` with `CLE v1` licensing while CSky retains BuiltByBit marketplace rights.\n\n"
            "• **Private Track (100% Exclusive)**\n"
            "  Complete IP exclusivity, full uncompiled Java 21 / Kotlin source repository access, and a dedicated Discord war room.\n\u200b"
        ),
        inline=False,
    )
    embed.add_field(
        name="Delivery Workflow",
        value=(
            "1. Scope & Quote (`< 24h`)\n"
            "2. 50% Deposit & Kickoff\n"
            "3. Staging Test & Review\n"
            "4. Final 50% & Handoff"
        ),
        inline=True,
    )
    embed.add_field(
        name="Supported Stack",
        value=(
            "• Paper 26.3 / Purpur\n"
            "• Folia & Velocity\n"
            "• Java 21 LTS / Kotlin\n"
            "• PostgreSQL, MySQL, Redis"
        ),
        inline=True,
    )
    embed.add_field(
        name="\u200b\nBilling, Warranty & Links",
        value=(
            "• **Warranty:** 14-day complimentary post-delivery bug fix warranty included.\n"
            "• **Authorized Billing:** Handled only in tickets by **Killer_Nova** or **Arsh** via **Tebex**, **Stripe**, or ticket-verified **UPI**.\n"
            f"• **Explore:** [Services]({CSKY_SERVICES_URL}) • [Request Form]({CSKY_WEBSITE_URL}/contact) • [Store]({CSKY_STORE_URL}) • [Terms]({CSKY_TERMS_URL})"
        ),
        inline=False,
    )
    embed.set_thumbnail(url=FOOTER_ICON)
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed
