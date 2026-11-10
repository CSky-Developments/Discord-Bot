import discord
from bot.embeds.help_embeds import FOOTER_TEXT, FOOTER_ICON

ARIAL_FOOTER_TEXT = "・ArialNodes"
ARIAL_FOOTER_ICON = "https://cdn.discordapp.com/attachments/1119317556893855826/1384873606021910649/ArialNodes.jpeg?ex=6854038d&is=6852b20d&hm=345f2e4d59144d461cd1c544253c724507849b7e6fe5410a2b96112e4710682b&"

def make_building_embed() -> discord.Embed:
    embed = discord.Embed(
        title="Build・Building",
        description=(
            "**Accepted Versions:** `1.8.8`, `1.16`–`1.21.5`\n\n"
            "**Build pricing is based on (but not limited to):**\n"
            "● **Size** — e.g., `1000x1000`, larger scale may increase cost. \n"
            "● **Time Required** — How long the build will take. \n"
            "● **Version Compatibility** — Specific version requests may affect pricing. \n"
            "● Additional factors depending on your request.\n\n"
            "**Minimum Price:** `119 INR/build`\n "
        ),
        color=0xF35A46,
    )
    embed.set_thumbnail(url="https://media.forgecdn.net/avatars/308/39/637390518902846753.png")
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_server_setup_embed() -> discord.Embed:
    embed = discord.Embed(
        title="Server・Setup",
        description=(
            "**Accepted Versions:** `1.8.8`, `1.16`–`1.21.5`\n \n"
            "**Setup pricing is based on (but not limited to):**\n"
            "● **Type of Server** — e.g. Game, Network, Modded, SMP, etc. \n"
            "● **Software** — Type of server software (e.g., Paper, Velocity, BungeeCord, Forge). \n"
            "● **Version Compatibility** — Specific version requirements may affect pricing. \n"
            "● **Features** — Number of features, custom systems, and level of personalization. \n"
            "● **Sounds & Effects** — Quantity and complexity of sound or particle effects. \n"
            "● **Time Required** — How long the setup will take to develop. \n"
            "● Other factors depending on the project scope.\n \n"
            "**Minimum Price:** `179 INR/setup`\n "
        ),
        color=0x4DAEE1,
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1111724820086915158/1387109204774490192/setup.png?ex=685c259d&is=685ad41d&hm=5e5738eea1e0e143f0017681faa814c8a35ba854aa9081ee6630901723f2b59f&")
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_texture_pack_embed() -> discord.Embed:
    embed = discord.Embed(
        title="Texture・Pack",
        description=(
            "**Supported Versions:** `1.8`, `1.16`–`1.21.5`\n \n"
            "**Texture Pack pricing is based on (but not limited to):**\n"
            "● **Resolution** — e.g., `16x`, `32x`, `64x`, `128x`, etc. \n"
            "● **Pack Type** — PvP, Custom UI, RPG, Realistic, Vanilla+, etc. \n"
            "● **Assets Required** — Number of items, blocks, GUIs, entities, and other custom elements. \n"
            "● **Style & Complexity** — Level of detail, animations, or visual effects. \n"
            "● **Version Compatibility** — Whether you want it to support multiple versions. \n"
            "● **Time Required** — How long the project will take. \n"
            "● Other specific requests or branding needs.\n \n"
            "**Minimum Price:** `119 INR/pack`\n "
        ),
        color=0x6AAFB8,
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1111724820086915158/1387105728023629895/14685847-logo_l.webp?ex=685c2260&is=685ad0e0&hm=8cc279d2d9b649b1801f94f1b1b0b4554fd0c3da3543c9ae4969506c9acc7374&")
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_hosting_plan_embed(name: str, ram: str, cpu: str, disk: str, price: str, icon_file: str) -> discord.Embed:
    embed = discord.Embed(
        title=f"{name} Plan",
        description=(
            "**Specifications:** \n"
            f"● <:ram:1387022203039645816> `{ram} RAM` \n"
            f"● <:cpu:1387022883213283399> `{cpu}` \n"
            f"● <:disk:1387022200522932285> `{disk} DISK`\n \n"
            "**Billing:** Monthly (long-term options available) \n"
            f"**Price:** `{price}`\n "
        ),
        color=0x068DE9,
    )
    embed.set_thumbnail(url=f"https://cdn.discordapp.com/attachments/1111724820086915158/{icon_file}")
    embed.set_footer(text=ARIAL_FOOTER_TEXT, icon_url=ARIAL_FOOTER_ICON)
    return embed

def make_dirt_plan_embed() -> discord.Embed:
    return make_hosting_plan_embed("Dirt", "2GB", "100% CPU (1 vCore)", "10GB", "69 INR/month", "1387128485767675934/dirt.png?ex=685c3792&is=685ae612&hm=6f506de246b368e89993d03cb686f3778eab67ed7f467e9c2c271efe3d88edd5&")

def make_wood_plan_embed() -> discord.Embed:
    return make_hosting_plan_embed("Wood", "4GB", "200% CPU (2 vCores)", "20GB", "149 INR/month", "1387128486128390315/wood.png?ex=685c3792&is=685ae612&hm=6e0e5e1b5667d33cefd1e77a41c9a1ad6bf701127d2f15752a98bf3fda6b4e02&")

def make_coal_plan_embed() -> discord.Embed:
    return make_hosting_plan_embed("Coal", "5GB", "200% CPU (2 vCores)", "20GB", "169 INR/month", "1387128485327142912/coal.png?ex=685c3792&is=685ae612&hm=0234b78196466d96d2698684b8929ca17c9adb1830cacfb3c650451e0cf65e79&")

def make_stone_plan_embed() -> discord.Embed:
    return make_hosting_plan_embed("Stone", "6GB", "200% CPU (2 vCores)", "30GB", "199 INR/month", "1387128486463930564/stone.png?ex=685c3792&is=685ae612&hm=104da46e0ec0e84cb00e3c01540ce6642231ca8075c5f1c985827d0dc3bed9bf&")

def make_iron_plan_embed() -> discord.Embed:
    return make_hosting_plan_embed("Iron", "8GB", "300% CPU (3 vCores)", "40GB", "299 / month", "1387128484991860747/iron.png?ex=685c3792&is=685ae612&hm=2a819b76b031edf3d4a07bf46f98a59e08feba9d77a1846d338ad87d92a3e6f2&")

def make_gold_plan_embed() -> discord.Embed:
    return make_hosting_plan_embed("Gold", "10GB", "300% CPU (3 vCores)", "40GB", "349 INR/month", "1387128487642402918/gold.png?ex=685c3793&is=685ae613&hm=87b48ef2f624722168dcdb8dddf1e291ac208fde2be3c3976f24a00fb75d0dfe&")

def make_diamond_plan_embed() -> discord.Embed:
    return make_hosting_plan_embed("Diamond", "12GB", "300% CPU (3 vCores)", "50GB", "399 INR/month", "1387128487243939850/diamond.png?ex=685c3792&is=685ae612&hm=a7327b35dbdfc035871ba241df9829f8f565c7f476e4a80bdff05e443a88f14d&")

def make_netherite_plan_embed() -> discord.Embed:
    return make_hosting_plan_embed("Netherite", "16GB", "400% CPU (4 vCores)", "50GB", "499 INR/month", "1387128486854004736/Netherite.png?ex=685c3792&is=685ae612&hm=b1bd41d612a0372762ad5fca61fa2780c8d2a24bea267e103a7ddd8caed04a08&")

def make_locations_payments_embed() -> discord.Embed:
    embed = discord.Embed(
        title="Locations & Payment Methods",
        description=(
            "**🌎 Server Locations:** \n"
            "● `India` :flag_in: \n"
            "● `Germany` :flag_de: \n \n"
            "**💳 Accepted Payment Methods:** \n"
            "● `UPI` <:upi:1384893594065834127> \n"
            "● `PayPal` <:paypal:1384893599837061130> *(Extra Charges Apply)* \n"
            "● `Crypto (Litecoin)` <:ltc:1384893606829101189> *(10% Extra Fee)*\n \n"
            "To place an order, simply click on the **Place Order** button below. \n"
            "It will send you link to ArialNode's discord where you can create ticket to order your server.\" \n "
        ),
        color=0x068DE9,
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1119317556893855826/1384873606021910649/ArialNodes.jpeg?ex=6854038d&is=6852b20d&hm=345f2e4d59144d461cd1c544253c724507849b7e6fe5410a2b96112e4710682b&")
    embed.set_footer(text=ARIAL_FOOTER_TEXT, icon_url=ARIAL_FOOTER_ICON)
    return embed

def make_server_optimization_embed() -> discord.Embed:
    embed = discord.Embed(
        title="Server・Optimization",
        description=(
            "**Supported Versions:** `1.8.8`, `1.16`–`1.21.5`\n \n"
            "**Optimization pricing is based on (but not limited to):**\n"
            "● **Server Type** — SMP, PvP, Modded, Network, etc. \n"
            "● **Software** — Paper, Purpur, Velocity, BungeeCord, Fabric, Forge, etc. \n"
            "● **Performance Goals** — TPS stability, lower RAM usage, improved CPU efficiency. \n"
            "● **Plugin/Mod Count** — Number of plugins or mods that need profiling/tuning. \n"
            "● **World Size & Player Capacity** — Impacts memory, chunk handling, and GC behavior. \n"
            "● **Time Required** — How long optimization will take (profiling, testing, tuning). \n"
            "● Other factors like hosting limitations, version-specific fixes, and custom requests.\n \n"
            "**Minimum Price:** `99 INR/setup`\n "
        ),
        color=0xE5B432,
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1119317556893855826/1384898863264960603/optimization.png?ex=68541b13&is=6852c993&hm=651f2b15ee15398bbdd52a063bd7cb793e65d87bfea2ae79d931aeb0131d12d0&")
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_plugin_development_embed() -> discord.Embed:
    embed = discord.Embed(
        title="Plugin・Development",
        description=(
            "**Supported Versions:** `1.8.8`, `1.16`–`1.21.5`\n\n"
            "**Plugin pricing is based on (but not limited to):**\n"
            "● **Type of Plugin** — Simple utilities, minigames, core systems, APIs, etc.  \n"
            "● **Complexity** — Amount of logic, conditions, and feature depth.  \n"
            "● **Commands & GUIs** — Number of commands, menus, and custom interfaces.  \n"
            "● **Performance Requirements** — Asynchronous handling, optimization goals, etc.  \n"
            "● **External Integrations** — MySQL, MongoDB, APIs, Discord bots, Bungee support, etc.  \n"
            "● **Time Required** — How long the project will take to plan, code, and test.  \n"
            "● Other custom requests or scalability considerations.\n\n"
            "**Minimum Price:** `179 INR/plugin`\n"
        ),
        color=0x938FF1,
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1119317556893855826/1384899272666910833/plug-in.png?ex=68541b74&is=6852c9f4&hm=d3c64877d9b7da3d6aca443501118afdc6632fd6d92a92eb475cd97cbf6e8d45&")
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_service_order_embed(color: int = 0x4482FF) -> discord.Embed:
    embed = discord.Embed(
        title="**Order Service**",
        description="To place an order, simply click on the **Place Order** button below.\nOur team will review your request and get back to you as soon as possible.",
        color=color,
    )
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed
