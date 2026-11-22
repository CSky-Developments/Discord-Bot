import discord
from discord.ui import View, Button
from bot.embeds.help_embeds import (
    CSKY_WEBSITE_URL,
    CSKY_SERVICES_URL,
    CSKY_TERMS_URL,
    CSKY_STORE_URL,
    CSKY_CRAFTER_URL,
    CSKY_AUTH_URL,
)

def get_emoji(name: str, emoji_id: int) -> discord.PartialEmoji:
    return discord.PartialEmoji(name=name, id=emoji_id)

def create_ticket_create_view() -> View:
    view = View(timeout=None)
    view.add_item(Button(
        style=discord.ButtonStyle.success,
        label="Create",
        custom_id="Ticket_Create_Button",
        emoji=get_emoji("Ticket", 1118483344397705237)
    ))
    return view

def create_ticket_close_view() -> View:
    view = View(timeout=None)
    view.add_item(Button(
        style=discord.ButtonStyle.danger,
        label="Close",
        custom_id="Ticket_Close_Button",
        emoji=get_emoji("TicketClose", 1118940954771075174)
    ))
    return view

def create_ticket_close_confirm_view() -> View:
    view = View(timeout=None)
    view.add_item(Button(
        style=discord.ButtonStyle.success,
        label="Confirm",
        custom_id="Ticket_Close_Confirm_Button",
        emoji=get_emoji("CloseConfirm", 1118942133517295757)
    ))
    view.add_item(Button(
        style=discord.ButtonStyle.danger,
        label="Cancel",
        custom_id="Ticket_Close_Cancel_Button",
        emoji=get_emoji("CloseCancel", 1118844964273659924)
    ))
    return view

def create_ticket_delete_view() -> View:
    view = View(timeout=None)
    view.add_item(Button(
        style=discord.ButtonStyle.danger,
        label="Delete",
        custom_id="Ticket_Delete_Button",
        emoji=get_emoji("Delete", 1118844967327113316)
    ))
    return view

def create_order_create_view() -> View:
    view = View(timeout=None)
    view.add_item(Button(
        style=discord.ButtonStyle.success,
        label="Place Order",
        custom_id="Order_Create_Button",
        emoji=get_emoji("Order", 1118978541871181915)
    ))
    view.add_item(Button(
        style=discord.ButtonStyle.link,
        label="Request on Website",
        url=f"{CSKY_WEBSITE_URL}/contact",
    ))
    view.add_item(Button(
        style=discord.ButtonStyle.link,
        label="Services",
        url=CSKY_SERVICES_URL,
    ))
    view.add_item(Button(
        style=discord.ButtonStyle.link,
        label="Terms",
        url=CSKY_TERMS_URL,
    ))
    return view


def create_commission_request_view(disabled: bool = False) -> View:
    view = View(timeout=None)
    view.add_item(Button(
        style=discord.ButtonStyle.success,
        label="Accept & Start Order Ticket",
        custom_id="Commission_Accept_Button",
        disabled=disabled,
    ))
    view.add_item(Button(
        style=discord.ButtonStyle.danger,
        label="Decline",
        custom_id="Commission_Decline_Button",
        disabled=disabled,
    ))
    return view


def create_purchase_view(product_url: str = "https://store.csky.dev", disabled: bool = False) -> View:
    view = View(timeout=None)
    view.add_item(Button(
        style=discord.ButtonStyle.success,
        label="Open Ticket with Buyer",
        custom_id="Purchase_Ticket_Button",
        disabled=disabled,
    ))
    view.add_item(Button(
        style=discord.ButtonStyle.link,
        label="View Product",
        url=product_url,
    ))
    return view

def create_order_close_view() -> View:
    view = View(timeout=None)
    view.add_item(Button(
        style=discord.ButtonStyle.danger,
        label="Cancel",
        custom_id="Order_Cancel_Button",
        emoji=get_emoji("OrderClose", 1118978536557006948)
    ))
    return view

def create_order_close_confirm_view() -> View:
    view = View(timeout=None)
    view.add_item(Button(
        style=discord.ButtonStyle.success,
        label="Confirm",
        custom_id="Order_Cancel_Confirm_Button",
        emoji=get_emoji("CloseConfirm", 1118942133517295757)
    ))
    view.add_item(Button(
        style=discord.ButtonStyle.danger,
        label="Cancel",
        custom_id="Order_Cancel_Cancel_Button",
        emoji=get_emoji("CloseCancel", 1118844964273659924)
    ))
    return view

def create_order_delete_view() -> View:
    view = View(timeout=None)
    view.add_item(Button(
        style=discord.ButtonStyle.danger,
        label="Delete",
        custom_id="Order_Delete_Button",
        emoji=get_emoji("Delete", 1118844967327113316)
    ))
    return view

def create_app_create_view() -> View:
    view = View(timeout=None)
    view.add_item(Button(
        style=discord.ButtonStyle.danger,
        label="Developer",
        custom_id="Developer_Button",
        emoji=get_emoji("Developer", 1117845118154711112)
    ))
    view.add_item(Button(
        style=discord.ButtonStyle.success,
        label="Moderator",
        custom_id="Moderator_Button",
        emoji=get_emoji("Moderator", 1117846138935066738)
    ))
    view.add_item(Button(
        style=discord.ButtonStyle.primary,
        label="Supporter",
        custom_id="Supporter_Button",
        emoji=get_emoji("Supporter", 1117847120565776444)
    ))
    view.add_item(Button(
        style=discord.ButtonStyle.secondary,
        label="Marketing",
        custom_id="Marketing_Button",
        emoji="📣",
    ))
    view.add_item(Button(
        style=discord.ButtonStyle.secondary,
        label="Creator",
        custom_id="Creator_Button",
        emoji="🎥",
    ))
    return view

def create_marketing_close_view() -> View:
    view = View(timeout=None)
    view.add_item(Button(
        style=discord.ButtonStyle.danger,
        label="Close",
        custom_id="Marketing_Close_Button",
    ))
    return view

def create_creator_close_view() -> View:
    view = View(timeout=None)
    view.add_item(Button(
        style=discord.ButtonStyle.danger,
        label="Close",
        custom_id="Creator_Close_Button",
    ))
    return view

def create_developer_close_view() -> View:
    view = View(timeout=None)
    view.add_item(Button(
        style=discord.ButtonStyle.danger,
        label="Close",
        custom_id="Developer_Close_Button",
        emoji=get_emoji("Developer_Cancel", 1123522806815129680)
    ))
    return view

def create_moderator_close_view() -> View:
    view = View(timeout=None)
    view.add_item(Button(
        style=discord.ButtonStyle.danger,
        label="Close",
        custom_id="Moderator_Close_Button",
        emoji=get_emoji("Moderator_Cancel", 1123522816780800001)
    ))
    return view

def create_supporter_close_view() -> View:
    view = View(timeout=None)
    view.add_item(Button(
        style=discord.ButtonStyle.danger,
        label="Close",
        custom_id="Supporter_Close_Button",
        emoji=get_emoji("Supporter_Cancel", 1123522822313087046)
    ))
    return view

def create_app_close_confirm_view() -> View:
    view = View(timeout=None)
    view.add_item(Button(
        style=discord.ButtonStyle.success,
        label="Confirm",
        custom_id="App_Close_Confirm_Button",
        emoji=get_emoji("CloseConfirm", 1118942133517295757)
    ))
    view.add_item(Button(
        style=discord.ButtonStyle.danger,
        label="Cancel",
        custom_id="App_Close_Cancel_Button",
        emoji=get_emoji("CloseCancel", 1118844964273659924)
    ))
    return view

def create_app_delete_view() -> View:
    view = View(timeout=None)
    view.add_item(Button(
        style=discord.ButtonStyle.danger,
        label="Delete",
        custom_id="App_Delete_Button",
        emoji=get_emoji("Delete", 1118844967327113316)
    ))
    return view

def create_links_view() -> View:
    view = View(timeout=None)
    view.add_item(Button(style=discord.ButtonStyle.link, label="Website", url=CSKY_WEBSITE_URL))
    view.add_item(Button(style=discord.ButtonStyle.link, label="Store", url=CSKY_STORE_URL))
    view.add_item(Button(style=discord.ButtonStyle.link, label="CSky Studio", url=CSKY_CRAFTER_URL))
    view.add_item(Button(style=discord.ButtonStyle.link, label="Account SSO", url=CSKY_AUTH_URL))
    view.add_item(Button(style=discord.ButtonStyle.link, label="Terms", url=CSKY_TERMS_URL))
    return view
