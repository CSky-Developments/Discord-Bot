import discord

FOOTER_TEXT = "・CSky Developments"
FOOTER_ICON = "https://cdn.discordapp.com/attachments/1112390125276631080/1112442565766168808/CSkyDevelopements.png"

CSKY_WEBSITE_URL = "https://csky.dev"
CSKY_SERVICES_URL = "https://csky.dev/services"
CSKY_TERMS_URL = "https://csky.dev/terms"
CSKY_ANNOUNCEMENTS_URL = "https://csky.dev/announcements"
CSKY_STORE_URL = "https://store.csky.dev"
CSKY_CRAFTER_URL = "https://crafter.csky.dev"
CSKY_AUTH_URL = "https://auth.csky.dev"
CSKY_LICENSE_URL = "https://license.csky.dev"

def make_help_embed() -> discord.Embed:
    embed = discord.Embed(
        title="CSky Developments - Help Menu",
        description=(
            "Below is a list of all available slash commands for the **CSky Developments** bot.\n"
            f"Visit our web ecosystem: [Website]({CSKY_WEBSITE_URL}) • [Store]({CSKY_STORE_URL}) • [CSky Studio]({CSKY_CRAFTER_URL})"
        ),
        color=0x2563EB,
    )
    embed.add_field(
        name="Web & Store",
        value=(
            "**/links** — Official links for Website, Store, CSky Studio & Terms.\n"
            "**/store search** — Browse or search live products from `store.csky.dev`.\n"
            "**/store product** — View detailed info & pricing for a store product.\n"
            "**/status** — Check live uptime of CSky web services & APIs."
        ),
        inline=False,
    )
    embed.add_field(
        name="Support, Orders & Applications",
        value=(
            "**/ticket** — Open or manage a support ticket.\n"
            "**/order** — Place a custom commission or service order.\n"
            "**/staffapp** — View staff application info and open an application."
        ),
        inline=False,
    )
    embed.add_field(
        name="Utilities",
        value="**/ping** — Check bot latency.",
        inline=False,
    )
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_not_available_embed() -> discord.Embed:
    embed = discord.Embed(
        title="Service Unavailable",
        description="This service is currently unavailable.\nPlease check back later or open a support ticket for more information.",
        color=0xDC2626,
    )
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed
