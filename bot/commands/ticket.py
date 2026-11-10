import discord
from discord import app_commands
from bot.config import Config
from bot.ticket import buttons
from bot.embeds import ticket_embeds, help_embeds
from bot.ticket.manager import TicketManager

def is_staff(member: discord.Member) -> bool:
    return any(r.id == Config.STAFF_ROLE_ID for r in getattr(member, "roles", []))

def make_no_permission_embed() -> discord.Embed:
    embed = discord.Embed(
        title="**NO PERMISSIONS**",
        description="**You must be a staff member to do that.**",
        color=0x0090FF
    )
    embed.set_footer(text=help_embeds.FOOTER_TEXT, icon_url=help_embeds.FOOTER_ICON)
    return embed

def setup_ticket_command(tree: app_commands.CommandTree, guild: discord.Object, ticket_manager: TicketManager):
    ticket_group = app_commands.Group(name="ticket", description="Create a new support ticket.")

    @ticket_group.command(name="create", description="Create a new support ticket")
    async def ticket_create(interaction: discord.Interaction):
        if not is_staff(interaction.user):
            await interaction.response.send_message(embed=make_no_permission_embed(), ephemeral=True, delete_after=10)
            return
        await interaction.response.send_message(embed=ticket_embeds.make_ticket_embed(), view=buttons.create_ticket_create_view())

    @ticket_group.command(name="add", description="Add a member to the ticket")
    @app_commands.describe(member="The member to add")
    async def ticket_add(interaction: discord.Interaction, member: discord.Member):
        if not is_staff(interaction.user):
            await interaction.response.send_message(embed=make_no_permission_embed(), ephemeral=True, delete_after=10)
            return

        channel = interaction.channel
        cat_id = getattr(channel, "category_id", None)
        if cat_id == Config.TICKET_NORMAL:
            await ticket_manager.handle_ticket_member_add(channel, member)
            await interaction.response.send_message(f"> **Added {member.mention} to the ticket.**")
        else:
            await interaction.response.send_message("> **🚫 You can't use this command here!**", ephemeral=True, delete_after=10)

    @ticket_group.command(name="remove", description="Remove a member from the ticket")
    @app_commands.describe(member="The member to remove")
    async def ticket_remove(interaction: discord.Interaction, member: discord.Member):
        if not is_staff(interaction.user):
            await interaction.response.send_message(embed=make_no_permission_embed(), ephemeral=True, delete_after=10)
            return

        channel = interaction.channel
        cat_id = getattr(channel, "category_id", None)
        if cat_id == Config.TICKET_NORMAL:
            await ticket_manager.handle_ticket_member_remove(channel, member)
            await interaction.response.send_message(f"> **Removed {member.mention} from the ticket.**")
        else:
            await interaction.response.send_message("> **🚫 You can't use this command here!**", ephemeral=True, delete_after=10)

    @ticket_group.command(name="close", description="Close the ticket")
    async def ticket_close(interaction: discord.Interaction):
        if not is_staff(interaction.user):
            await interaction.response.send_message(embed=make_no_permission_embed(), ephemeral=True, delete_after=10)
            return

        channel = interaction.channel
        cat_id = getattr(channel, "category_id", None)
        if cat_id == Config.TICKET_NORMAL:
            await interaction.response.send_message(embed=ticket_embeds.make_ticket_close_embed(), view=buttons.create_ticket_close_view())
        else:
            await interaction.response.send_message("> **🚫 You can't use this command here!**", ephemeral=True, delete_after=10)

    tree.add_command(ticket_group, guild=guild)
