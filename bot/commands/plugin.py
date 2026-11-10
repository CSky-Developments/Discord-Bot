import discord
from discord import app_commands
from bot.config import Config
from bot.ticket import buttons
from bot.embeds import ticket_embeds, help_embeds
from bot.ticket.manager import TicketManager
from bot.commands.ticket import is_staff, make_no_permission_embed

def setup_plugin_command(tree: app_commands.CommandTree, guild: discord.Object, ticket_manager: TicketManager):
    plugin_group = app_commands.Group(name="plugin", description="Manage plugin generation requests.")

    @plugin_group.command(name="generate", description="Start a new plugin generation request")
    async def plugin_generate(interaction: discord.Interaction):
        user = interaction.user
        has_role = any(r.id == Config.PLUGIN_GEN_ACCESS_ROLE_ID for r in getattr(user, "roles", []))
        if not has_role:
            no_access = discord.Embed(
                title="**Access Denied**",
                description=(
                    "**You need the Plugin Generation subscription to use this service.**\n"
                    "This is a premium feature. Please create a ticket to subscribe."
                ),
                color=0xE74C3C
            )
            no_access.set_footer(text=help_embeds.FOOTER_TEXT, icon_url=help_embeds.FOOTER_ICON)
            await interaction.response.send_message(embed=no_access, ephemeral=True, delete_after=15)
            return

        await interaction.response.send_message(embed=ticket_embeds.make_plugin_gen_embed(), view=buttons.create_plugin_generate_view())

    @plugin_group.command(name="add", description="Add a member to the plugin ticket")
    @app_commands.describe(member="The member to add")
    async def plugin_add(interaction: discord.Interaction, member: discord.Member):
        if not is_staff(interaction.user):
            await interaction.response.send_message(embed=make_no_permission_embed(), ephemeral=True, delete_after=10)
            return

        channel = interaction.channel
        cat_id = getattr(channel, "category_id", None)
        if cat_id == Config.TICKET_PLUGIN_GEN:
            await ticket_manager.handle_ticket_member_add(channel, member)
            await interaction.response.send_message(f"> **Added {member.mention} to the plugin ticket.**")
        else:
            await interaction.response.send_message("> **You can't use this command here!**", ephemeral=True, delete_after=10)

    @plugin_group.command(name="remove", description="Remove a member from the plugin ticket")
    @app_commands.describe(member="The member to remove")
    async def plugin_remove(interaction: discord.Interaction, member: discord.Member):
        if not is_staff(interaction.user):
            await interaction.response.send_message(embed=make_no_permission_embed(), ephemeral=True, delete_after=10)
            return

        channel = interaction.channel
        cat_id = getattr(channel, "category_id", None)
        if cat_id == Config.TICKET_PLUGIN_GEN:
            await ticket_manager.handle_ticket_member_remove(channel, member)
            await interaction.response.send_message(f"> **Removed {member.mention} from the plugin ticket.**")
        else:
            await interaction.response.send_message("> **You can't use this command here!**", ephemeral=True, delete_after=10)

    @plugin_group.command(name="cancel", description="Cancel the plugin generation request")
    async def plugin_cancel(interaction: discord.Interaction):
        if not is_staff(interaction.user):
            await interaction.response.send_message(embed=make_no_permission_embed(), ephemeral=True, delete_after=10)
            return

        channel = interaction.channel
        cat_id = getattr(channel, "category_id", None)
        if cat_id == Config.TICKET_PLUGIN_GEN:
            await interaction.response.send_message(embed=ticket_embeds.make_plugin_gen_close_embed(), view=buttons.create_plugin_cancel_confirm_view())
        else:
            await interaction.response.send_message("> **You can't use this command here!**", ephemeral=True, delete_after=10)

    tree.add_command(plugin_group, guild=guild)
