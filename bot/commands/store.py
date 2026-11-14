"""Live CSky Store catalog search and product lookup commands (/store)."""

from typing import Optional
import aiohttp
import discord
from discord import app_commands

from bot.embeds.help_embeds import CSKY_STORE_URL, FOOTER_ICON, FOOTER_TEXT


STORE_CATEGORIES = ["Plugins", "Configs", "Resource Packs", "Setups"]


def format_price(price: float | int | None, price_inr: float | int | None) -> str:
    if price is None or float(price) == 0:
        return "Free"
    usd = f"${float(price):.2f}".rstrip("0").rstrip(".")
    if price_inr is not None and float(price_inr) > 0:
        inr = f"₹{int(round(float(price_inr)))}"
        return f"{usd} ({inr})"
    return usd


def make_store_search_embed(
    products: list[dict],
    query: Optional[str] = None,
    category: Optional[str] = None,
) -> discord.Embed:
    filter_parts = []
    if category:
        filter_parts.append(f"Category: `{category}`")
    if query:
        filter_parts.append(f"Query: `{query}`")
    subtitle = " • ".join(filter_parts) if filter_parts else "Latest releases from `store.csky.dev`"

    embed = discord.Embed(
        title="CSky Store — Catalog",
        description=f"{subtitle}\nBrowse all products at [store.csky.dev]({CSKY_STORE_URL})",
        color=0x2563EB,
    )
    if not products:
        embed.add_field(
            name="No matching products found",
            value="Try a different search term or browse the full catalog on `store.csky.dev`.",
            inline=False,
        )
    else:
        for item in products[:6]:
            title = item.get("title", "Untitled")
            slug = item.get("slug", "")
            tagline = item.get("tagline", "")
            price_str = format_price(item.get("price"), item.get("priceInr"))
            engine = item.get("testedEngine") or "Paper"
            rating = item.get("rating")
            reviews_count = item.get("reviewsCount", 0)
            rating_str = f"⭐ {rating:.1f} ({reviews_count})" if rating and reviews_count else "New"
            url = f"{CSKY_STORE_URL}/products/{slug}" if slug else CSKY_STORE_URL
            embed.add_field(
                name=f"{title} — `{price_str}`",
                value=f"{tagline}\n`{engine}` • {rating_str} • [View Product]({url})",
                inline=False,
            )

    embed.set_thumbnail(url=FOOTER_ICON)
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed


def make_store_product_embed(product: dict) -> discord.Embed:
    title = product.get("title", "Product")
    slug = product.get("slug", "")
    url = f"{CSKY_STORE_URL}/products/{slug}" if slug else CSKY_STORE_URL
    price_str = format_price(product.get("price"), product.get("priceInr"))
    description = product.get("tagline") or product.get("description") or ""

    embed = discord.Embed(
        title=title,
        url=url,
        description=description[:400],
        color=0x2563EB,
    )
    embed.add_field(name="Price", value=f"`{price_str}`", inline=True)
    embed.add_field(name="Category", value=f"`{product.get('category', 'Plugins')}`", inline=True)
    embed.add_field(name="Version", value=f"`{product.get('version', '1.0.0')}`", inline=True)

    mc_versions = product.get("minecraftVersions") or []
    if mc_versions:
        embed.add_field(name="Minecraft Versions", value=", ".join(f"`{v}`" for v in mc_versions[:6]), inline=True)

    if product.get("testedEngine"):
        embed.add_field(name="Tested Engine", value=f"`{product['testedEngine']}`", inline=True)

    features = product.get("features") or []
    if features:
        embed.add_field(
            name="Key Features",
            value="\n".join(f"• {f}" for f in features[:5]),
            inline=False,
        )

    image_url = product.get("imageUrl")
    if isinstance(image_url, str) and image_url.startswith("http"):
        embed.set_thumbnail(url=image_url)
    else:
        embed.set_thumbnail(url=FOOTER_ICON)

    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed


def create_store_view(product_url: str = CSKY_STORE_URL, label: str = "Open CSky Store") -> discord.ui.View:
    view = discord.ui.View(timeout=None)
    view.add_item(discord.ui.Button(style=discord.ButtonStyle.link, label=label, url=product_url))
    if product_url != CSKY_STORE_URL:
        view.add_item(discord.ui.Button(style=discord.ButtonStyle.link, label="All Products", url=CSKY_STORE_URL))
    return view


def setup_store_command(tree: app_commands.CommandTree, guild: discord.Object):
    store_group = app_commands.Group(name="store", description="Browse and search products on store.csky.dev.")

    @store_group.command(name="search", description="Search or browse products from store.csky.dev")
    @app_commands.describe(
        query="Optional search keyword",
        category="Optional product category",
    )
    @app_commands.choices(category=[app_commands.Choice(name=c, value=c) for c in STORE_CATEGORIES])
    async def store_search(
        interaction: discord.Interaction,
        query: Optional[str] = None,
        category: Optional[app_commands.Choice[str]] = None,
    ):
        await interaction.response.defer(thinking=True)
        params: dict[str, str] = {}
        if query:
            params["q"] = query
        if category:
            params["category"] = category.value

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{CSKY_STORE_URL}/api/products",
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=8),
                ) as resp:
                    if resp.status != 200:
                        await interaction.followup.send(
                            f"⚠️ Store API returned `HTTP {resp.status}`. Browse directly at {CSKY_STORE_URL}",
                            ephemeral=True,
                        )
                        return
                    data = await resp.json()
        except Exception:
            await interaction.followup.send(
                f"⚠️ Could not reach `store.csky.dev` right now. Visit {CSKY_STORE_URL} directly.",
                ephemeral=True,
            )
            return

        products = data.get("products", [])
        embed = make_store_search_embed(products, query=query, category=category.value if category else None)
        await interaction.followup.send(embed=embed, view=create_store_view())

    @store_group.command(name="product", description="View details for a specific store product by slug")
    @app_commands.describe(slug="Product slug (e.g., scores-smp)")
    async def store_product(interaction: discord.Interaction, slug: str):
        await interaction.response.defer(thinking=True)
        clean_slug = slug.strip().lower()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{CSKY_STORE_URL}/api/products/{clean_slug}",
                    timeout=aiohttp.ClientTimeout(total=8),
                ) as resp:
                    if resp.status == 404:
                        await interaction.followup.send(
                            f"❌ No product found for slug `{clean_slug}`. Try `/store search` or visit {CSKY_STORE_URL}.",
                            ephemeral=True,
                        )
                        return
                    if resp.status != 200:
                        await interaction.followup.send(
                            f"⚠️ Store API returned `HTTP {resp.status}`. Visit {CSKY_STORE_URL}.",
                            ephemeral=True,
                        )
                        return
                    data = await resp.json()
        except Exception:
            await interaction.followup.send(
                f"⚠️ Could not reach `store.csky.dev` right now. Visit {CSKY_STORE_URL}.",
                ephemeral=True,
            )
            return

        product = data.get("product")
        if not product:
            await interaction.followup.send(f"❌ Product `{clean_slug}` not found.", ephemeral=True)
            return

        product_url = f"{CSKY_STORE_URL}/products/{product.get('slug', clean_slug)}"
        await interaction.followup.send(
            embed=make_store_product_embed(product),
            view=create_store_view(product_url=product_url, label="View on Store"),
        )

    tree.add_command(store_group, guild=guild)
