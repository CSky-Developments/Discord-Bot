import discord

FOOTER_TEXT = "・CSky Developments"
FOOTER_ICON = "https://cdn.discordapp.com/attachments/1112390125276631080/1112442565766168808/CSkyDevelopements.png"

def make_help_embed() -> discord.Embed:
    embed = discord.Embed(
        title="CSky Developments - Help Menu",
        description="Below is a list of all available commands for the CSky Developments bot. Use the prefix `c!` to execute these commands.",
        color=0xFF0000,
    )
    embed.add_field(
        name="General Commands",
        value="**c!help** or **c!?** - Displays this help menu.\n**c!not available** - Shows information about unavailable services.",
        inline=False,
    )
    embed.add_field(
        name="Support & Applications",
        value="**c!ticket** or **c!tickets** - Opens a support ticket.\n**c!staff application** or **c!staff app** - Information about staff applications.",
        inline=False,
    )
    embed.add_field(
        name="Orders & Services",
        value="**c!order** - Places a new order.\n**c!plugin development** - Information about custom plugin development.",
        inline=False,
    )
    embed.add_field(
        name="Server Optimizations",
        value="**c!optimization** - Lists all server optimization services.\n**c!bukkit optimization** - Bukkit server optimization.\n**c!spigot optimization** - Spigot server optimization.\n**c!paper optimization** - Paper server optimization.\n**c!purple optimization** - Purpur server optimization.\n**c!bungeecode optimization** - BungeeCord server optimization.\n**c!waterfall optimization** - Waterfall server optimization.\n**c!velocity optimization** - Velocity server optimization.\n**c!forge optimization** - Forge server optimization.\n**c!fabric optimization** - Fabric server optimization.",
        inline=False,
    )
    embed.add_field(
        name="Rewards",
        value="**c!reward** or **c!rewards** - View available rewards.\n**c!invite reward** or **c!invite rewards** - Claim invite-based rewards.\n**c!booster reward** or **c!booster rewards** - Claim server booster rewards.",
        inline=False,
    )
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_not_available_embed() -> discord.Embed:
    embed = discord.Embed(
        title="🚫 Service Unavailable",
        description="**This service is currently not available.** \nPlease check back later or contact us for more information.\n",
        color=0xFF4C4C,
    )
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed
