import discord
from discord.ui import View, Button

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

def create_plugin_generate_view() -> View:
    view = View(timeout=None)
    view.add_item(Button(
        style=discord.ButtonStyle.success,
        label="Generate",
        custom_id="Plugin_Generate_Button",
        emoji=get_emoji("Developer", 1117845118154711112)
    ))
    return view

def create_plugin_cancel_view() -> View:
    view = View(timeout=None)
    view.add_item(Button(
        style=discord.ButtonStyle.danger,
        label="Cancel",
        custom_id="Plugin_Cancel_Button",
        emoji=get_emoji("Developer_Cancel", 1123522806815129680)
    ))
    return view

def create_plugin_cancel_confirm_view() -> View:
    view = View(timeout=None)
    view.add_item(Button(
        style=discord.ButtonStyle.success,
        label="Confirm",
        custom_id="Plugin_Cancel_Confirm_Button",
        emoji=get_emoji("CloseConfirm", 1118942133517295757)
    ))
    view.add_item(Button(
        style=discord.ButtonStyle.danger,
        label="Abort",
        custom_id="Plugin_Cancel_Abort_Button",
        emoji=get_emoji("CloseCancel", 1118844964273659924)
    ))
    return view

def create_plugin_delete_view() -> View:
    view = View(timeout=None)
    view.add_item(Button(
        style=discord.ButtonStyle.danger,
        label="Delete",
        custom_id="Plugin_Delete_Button",
        emoji=get_emoji("Delete", 1118844967327113316)
    ))
    return view

def create_reward_claim_view() -> View:
    view = View(timeout=None)
    view.add_item(Button(
        style=discord.ButtonStyle.success,
        label="Claim",
        custom_id="Reward_Claim_Button",
        emoji=get_emoji("Gift", 1118971206515818568)
    ))
    return view

def create_reward_close_view() -> View:
    view = View(timeout=None)
    view.add_item(Button(
        style=discord.ButtonStyle.danger,
        label="Close",
        custom_id="Reward_Close_Button",
        emoji=get_emoji("GiftClose", 1118971201818202213)
    ))
    return view

def create_reward_close_confirm_view() -> View:
    view = View(timeout=None)
    view.add_item(Button(
        style=discord.ButtonStyle.success,
        label="Confirm",
        custom_id="Reward_Close_Confirm_Button",
        emoji=get_emoji("CloseConfirm", 1118942133517295757)
    ))
    view.add_item(Button(
        style=discord.ButtonStyle.danger,
        label="Cancel",
        custom_id="Reward_Close_Cancel_Button",
        emoji=get_emoji("CloseCancel", 1118844964273659924)
    ))
    return view

def create_reward_delete_view() -> View:
    view = View(timeout=None)
    view.add_item(Button(
        style=discord.ButtonStyle.danger,
        label="Delete",
        custom_id="Reward_Delete_Button",
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

def create_server_order_create_view() -> View:
    view = View(timeout=None)
    view.add_item(Button(
        style=discord.ButtonStyle.success,
        label="Place Order",
        custom_id="Server_Order_Create_Button",
        emoji=get_emoji("Order", 1118978541871181915)
    ))
    return view
