import discord
from discord import app_commands

from bot.commands.pay import _format_display_amount, setup_pay_command
from bot.internal_api import build_payment_embed


def test_format_display_amount():
    assert _format_display_amount(500.0, "INR") == "₹500"
    assert _format_display_amount(25.5, "USD") == "$25.50"


def test_build_payment_embed():
    embed, url = build_payment_embed(
        {
            "reference": "CSKY-PAY-1234ABCD",
            "displayAmount": 999,
            "currency": "INR",
            "paymentMethod": "upi",
            "razorpayPaymentId": "pay_Test123456",
            "title": "Custom Plugin Commission",
            "note": "AltarBosses Deposit",
            "discordUserId": "123456789012345678",
            "discordTag": "arsh#0001",
        }
    )
    assert embed.title == "Payment Received — CSKY-PAY-1234ABCD"
    assert "CSKY-PAY-1234ABCD" in url
    field_map = {f.name: f.value for f in embed.fields}
    assert "₹999 INR" in field_map["Amount Paid"]
    assert "`UPI`" in field_map["Method"]
    assert "<@123456789012345678>" in field_map["Payer"]
    assert field_map["Note / Purpose"] == "AltarBosses Deposit"


def test_setup_pay_command_registers_group():
    intents = discord.Intents.none()
    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client)
    guild = discord.Object(id=1234567890)
    setup_pay_command(tree, guild)
    cmd = tree.get_command("pay", guild=guild)
    assert cmd is not None
    assert isinstance(cmd, app_commands.Group)
    sub_names = {c.name for c in cmd.commands}
    assert {"link", "create", "status"}.issubset(sub_names)
