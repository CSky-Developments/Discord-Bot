import hmac
from typing import Optional
import discord
from aiohttp import web

from bot.config import Config
from bot.embeds.help_embeds import FOOTER_TEXT, FOOTER_ICON
from bot.logger import BotLogger
from bot.ticket import buttons


def _clean_text(value: object, max_len: int) -> str:
    if not isinstance(value, str):
        return ""
    return value.strip()[:max_len]


def build_commission_embed(data: dict) -> discord.Embed:
    name = _clean_text(data.get("name"), 100) or "Unknown Client"
    contact = _clean_text(data.get("contactHandle"), 150) or "Not provided"
    track = _clean_text(data.get("track"), 150) or "Private Track (100% Exclusive & Full Source)"
    service = _clean_text(data.get("serviceType"), 120) or "Custom Plugin Development"
    budget = _clean_text(data.get("budget"), 60) or "Not specified"
    details = _clean_text(data.get("details"), 1800) or "No specifications provided."

    is_public = "public" in track.lower()
    embed_color = 0x137333 if is_public else 0x1A73E8
    track_badge = (
        "Public Track (40-60% Discounted)"
        if is_public
        else "Private Track (100% Exclusive)"
    )
    safe_details = f"{details[:997]}..." if len(details) > 1000 else details

    embed = discord.Embed(
        title=f"New Commission Request — {service}",
        url="https://csky.dev/contact",
        color=embed_color,
    )
    embed.add_field(name="Client", value=name, inline=True)
    embed.add_field(name="Contact", value=f"`{contact}`", inline=True)
    embed.add_field(name="Estimated Budget", value=f"`{budget}`", inline=True)
    embed.add_field(name="Commission Track", value=track_badge, inline=False)
    embed.add_field(name="Project Specifications & Ideas", value=safe_details, inline=False)
    embed.set_footer(text="CSky Developments • csky.dev/contact", icon_url=FOOTER_ICON)
    embed.timestamp = discord.utils.utcnow()
    return embed


def _format_money(amount: float, currency: str) -> str:
    if currency.upper() == "INR":
        return f"₹{amount:.0f}"
    return f"${amount:.2f}"


def _resolve_cover_url(product: Optional[dict]) -> Optional[str]:
    if not product:
        return None
    raw = _clean_text(product.get("imageUrl"), 500)
    if raw:
        if raw.startswith("http://") or raw.startswith("https://"):
            return raw
        normalized = raw if raw.startswith("/") else f"/{raw}"
        return f"https://store.csky.dev{normalized}"
    slug = _clean_text(product.get("slug"), 200)
    return f"https://store.csky.dev/products/{slug}/opengraph-image" if slug else None


def build_purchase_embed(data: dict) -> tuple[discord.Embed, str]:
    order_number = _clean_text(data.get("orderNumber"), 60) or "ORDER"
    currency = (_clean_text(data.get("currency"), 10) or "USD").upper()
    total_amount = float(data.get("totalAmount") or 0)
    discount_amount = float(data.get("discountAmount") or 0)
    payment_display = _clean_text(data.get("paymentMethod") or data.get("paymentGateway"), 60) or "Stripe"

    user = data.get("user") if isinstance(data.get("user"), dict) else {}
    provider = _clean_text(user.get("provider"), 40)
    provider_id = _clean_text(user.get("providerId"), 40)
    discord_tag = _clean_text(user.get("discordTag"), 100)
    user_name = _clean_text(user.get("name"), 100)
    user_email = _clean_text(user.get("email"), 150)

    if provider == "discord" and provider_id:
        buyer_display = f"<@{provider_id}> ({discord_tag or user_name or user_email})"
    else:
        buyer_display = discord_tag or (f"{user_name} ({user_email})" if user_name and user_email else user_name or user_email or "Customer")

    amount_str = f"`{_format_money(total_amount, currency)} {currency}`"
    if discount_amount > 0:
        amount_str += f" (Discount: -{_format_money(discount_amount, currency)})"

    products = data.get("products") if isinstance(data.get("products"), list) else []
    primary = products[0] if products and isinstance(products[0], dict) else None
    primary_slug = _clean_text(primary.get("slug"), 200) if primary else ""
    primary_title = _clean_text(primary.get("title"), 150) if primary else "Store Order"
    product_url = f"https://store.csky.dev/products/{primary_slug}" if primary_slug else "https://store.csky.dev/orders"

    product_lines = []
    for p in products:
        if not isinstance(p, dict):
            continue
        title = _clean_text(p.get("title"), 150) or "Product"
        slug = _clean_text(p.get("slug"), 200)
        meta = [x for x in [
            _clean_text(p.get("category"), 60),
            f"v{_clean_text(p.get('version'), 30)}" if _clean_text(p.get("version"), 30) else "",
            _clean_text(p.get("testedEngine"), 60),
        ] if x]
        meta_suffix = f" — {' • '.join(meta)}" if meta else ""
        link = f"**[{title}](https://store.csky.dev/products/{slug})**" if slug else f"**{title}**"
        product_lines.append(f"• {link}{meta_suffix}")

    embed = discord.Embed(
        title=f"{primary_title} — {order_number}",
        url=product_url,
        color=0x16A34A,
    )
    embed.set_author(name="CSky Store • New Purchase", url="https://store.csky.dev", icon_url=FOOTER_ICON)
    embed.add_field(name="Buyer", value=buyer_display, inline=True)
    embed.add_field(name="Amount Paid", value=amount_str, inline=True)
    embed.add_field(name="Payment", value=f"`{payment_display}`", inline=True)
    embed.add_field(
        name=f"Products ({len(product_lines)})" if len(product_lines) > 1 else "Product Details",
        value="\n".join(product_lines) if product_lines else "• Store Order",
        inline=False,
    )
    embed.add_field(
        name="Order Reference",
        value=f"Order `{order_number}` • [View Product]({product_url}) • [Store Orders](https://store.csky.dev/orders)",
        inline=False,
    )

    cover_url = _resolve_cover_url(primary)
    if cover_url:
        embed.set_image(url=cover_url)

    embed.set_footer(text="CSky Store • store.csky.dev", icon_url=FOOTER_ICON)
    embed.timestamp = discord.utils.utcnow()
    return embed, product_url


async def start_internal_api(bot: discord.Client) -> Optional[web.AppRunner]:
    async def health(_request: web.Request) -> web.Response:
        return web.json_response({"ok": True})

    async def handle_commission(request: web.Request) -> web.Response:
        expected_secret = Config.INTERNAL_API_SECRET
        if not expected_secret:
            return web.json_response(
                {"error": "INTERNAL_API_SECRET is not configured on bot"},
                status=503,
            )

        provided_secret = request.headers.get("x-csky-internal-secret", "")
        if not provided_secret or not hmac.compare_digest(provided_secret, expected_secret):
            return web.json_response({"error": "Unauthorized"}, status=401)

        try:
            payload = await request.json()
        except Exception:
            return web.json_response({"error": "Invalid JSON body"}, status=400)

        if not isinstance(payload, dict):
            return web.json_response({"error": "JSON object required"}, status=400)

        guild = getattr(bot, "guild_obj", None)
        if not guild:
            return web.json_response({"error": "Bot guild is not ready"}, status=503)

        channel_id = Config.REQUESTS_CHANNEL_ID
        if not channel_id:
            return web.json_response(
                {"error": "REQUESTS_CHANNEL_ID is not configured on bot"},
                status=503,
            )

        channel = guild.get_channel(channel_id)
        if not isinstance(channel, discord.TextChannel):
            return web.json_response(
                {"error": f"Requests channel {channel_id} not found"},
                status=500,
            )

        embed = build_commission_embed(payload)
        msg = await channel.send(embed=embed, view=buttons.create_commission_request_view())
        return web.json_response({"ok": True, "messageId": str(msg.id)})

    async def handle_purchase(request: web.Request) -> web.Response:
        expected_secret = Config.INTERNAL_API_SECRET
        if not expected_secret:
            return web.json_response(
                {"error": "INTERNAL_API_SECRET is not configured on bot"},
                status=503,
            )

        provided_secret = request.headers.get("x-csky-internal-secret", "")
        if not provided_secret or not hmac.compare_digest(provided_secret, expected_secret):
            return web.json_response({"error": "Unauthorized"}, status=401)

        try:
            payload = await request.json()
        except Exception:
            return web.json_response({"error": "Invalid JSON body"}, status=400)

        if not isinstance(payload, dict):
            return web.json_response({"error": "JSON object required"}, status=400)

        guild = getattr(bot, "guild_obj", None)
        if not guild:
            return web.json_response({"error": "Bot guild is not ready"}, status=503)

        channel_id = Config.SALES_CHANNEL_ID
        if not channel_id:
            return web.json_response(
                {"error": "SALES_CHANNEL_ID is not configured on bot"},
                status=503,
            )

        channel = guild.get_channel(channel_id)
        if not isinstance(channel, discord.TextChannel):
            return web.json_response(
                {"error": f"Sales channel {channel_id} not found"},
                status=500,
            )

        embed, product_url = build_purchase_embed(payload)
        msg = await channel.send(embed=embed, view=buttons.create_purchase_view(product_url))
        return web.json_response({"ok": True, "messageId": str(msg.id)})

    app = web.Application()
    app.router.add_get("/health", health)
    app.router.add_post("/internal/commission", handle_commission)
    app.router.add_post("/internal/purchase", handle_purchase)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", Config.INTERNAL_HTTP_PORT)
    await site.start()
    BotLogger.info(f"Internal bot API listening on 0.0.0.0:{Config.INTERNAL_HTTP_PORT}", False)
    return runner
