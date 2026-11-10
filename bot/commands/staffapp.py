import discord
from discord import app_commands
from bot.config import Config
from bot.ticket import buttons
from bot.embeds import ticket_embeds
from bot.commands.ticket import is_staff, make_no_permission_embed

def setup_staffapp_command(tree: app_commands.CommandTree, guild: discord.Object):
    staffapp_group = app_commands.Group(name="staffapp", description="Create a staff application.")

    @staffapp_group.command(name="apply", description="Create a staff application.")
    async def staffapp_apply(interaction: discord.Interaction):
        if not is_staff(interaction.user):
            await interaction.response.send_message(embed=make_no_permission_embed(), ephemeral=True, delete_after=10)
            return
        await interaction.response.send_message(embed=ticket_embeds.make_staff_app_embed(), view=buttons.create_app_create_view())

    @staffapp_group.command(name="close", description="Close staff application ticket")
    async def staffapp_close(interaction: discord.Interaction):
        if not is_staff(interaction.user):
            await interaction.response.send_message(embed=make_no_permission_embed(), ephemeral=True, delete_after=10)
            return

        channel = interaction.channel
        cat_id = getattr(channel, "category_id", None)
        if cat_id == Config.TICKET_STAFF_APP:
            await interaction.response.send_message(embed=ticket_embeds.make_staff_app_close_embed(), view=buttons.create_app_delete_view())
        else:
            await interaction.response.send_message("> **🚫 You can't use this command here!**", ephemeral=True, delete_after=10)

    tree.add_command(staffapp_group, guild=guild)
