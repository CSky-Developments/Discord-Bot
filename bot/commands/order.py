import discord
from discord import app_commands
from bot.config import Config
from bot.ticket import buttons
from bot.embeds import ticket_embeds
from bot.ticket.manager import TicketManager
from bot.commands.ticket import is_staff, make_no_permission_embed

def setup_order_command(tree: app_commands.CommandTree, guild: discord.Object, ticket_manager: TicketManager):
    order_group = app_commands.Group(name="order", description="To place a new order.")

    @order_group.command(name="create", description="To place a new order.")
    async def order_create(interaction: discord.Interaction):
        if not is_staff(interaction.user):
            await interaction.response.send_message(embed=make_no_permission_embed(), ephemeral=True, delete_after=10)
            return
        await interaction.response.send_message(embed=ticket_embeds.make_order_embed(), view=buttons.create_order_create_view())

    @order_group.command(name="add", description="Add a member to the order")
    @app_commands.describe(member="The member to add")
    async def order_add(interaction: discord.Interaction, member: discord.Member):
        if not is_staff(interaction.user):
            await interaction.response.send_message(embed=make_no_permission_embed(), ephemeral=True, delete_after=10)
            return

        channel = interaction.channel
        cat_id = getattr(channel, "category_id", None)
        if cat_id == Config.TICKET_ORDER:
            await ticket_manager.handle_ticket_member_add(channel, member)
            await interaction.response.send_message(f"> **Added {member.mention} to the order.**")
        else:
            await interaction.response.send_message("> **🚫 You can't use this command here!**", ephemeral=True, delete_after=10)

    @order_group.command(name="remove", description="Remove a member from the order")
    @app_commands.describe(member="The member to remove")
    async def order_remove(interaction: discord.Interaction, member: discord.Member):
        if not is_staff(interaction.user):
            await interaction.response.send_message(embed=make_no_permission_embed(), ephemeral=True, delete_after=10)
            return

        channel = interaction.channel
        cat_id = getattr(channel, "category_id", None)
        if cat_id == Config.TICKET_ORDER:
            await ticket_manager.handle_ticket_member_remove(channel, member)
            await interaction.response.send_message(f"> **Removed {member.mention} from the order.**")
        else:
            await interaction.response.send_message("> **🚫 You can't use this command here!**", ephemeral=True, delete_after=10)

    @order_group.command(name="close", description="Close the order")
    async def order_close(interaction: discord.Interaction):
        if not is_staff(interaction.user):
            await interaction.response.send_message(embed=make_no_permission_embed(), ephemeral=True, delete_after=10)
            return

        channel = interaction.channel
        cat_id = getattr(channel, "category_id", None)
        if cat_id == Config.TICKET_ORDER:
            await interaction.response.send_message(embed=ticket_embeds.make_order_close_embed(), view=buttons.create_order_close_view())
        else:
            await interaction.response.send_message("> **🚫 You can't use this command here!**", ephemeral=True, delete_after=10)

    tree.add_command(order_group, guild=guild)
