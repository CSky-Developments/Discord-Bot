import discord
from discord import app_commands
from bot.config import Config
from bot.ticket import buttons
from bot.embeds import ticket_embeds
from bot.ticket.manager import TicketManager
from bot.commands.ticket import is_staff, make_no_permission_embed

def setup_reward_command(tree: app_commands.CommandTree, guild: discord.Object, ticket_manager: TicketManager):
    reward_group = app_commands.Group(name="reward", description="Use to claim your reward.", guild=guild)

    @reward_group.command(name="claim", description="Use to claim your reward.")
    async def reward_claim(interaction: discord.Interaction):
        if not is_staff(interaction.user):
            await interaction.response.send_message(embed=make_no_permission_embed(), ephemeral=True, delete_after=10)
            return
        await interaction.response.send_message(embed=ticket_embeds.make_reward_embed(), view=buttons.create_reward_claim_view())

    @reward_group.command(name="add", description="Add a member to reward ticket")
    @app_commands.describe(member="The member to add")
    async def reward_add(interaction: discord.Interaction, member: discord.Member):
        if not is_staff(interaction.user):
            await interaction.response.send_message(embed=make_no_permission_embed(), ephemeral=True, delete_after=10)
            return

        channel = interaction.channel
        cat_id = getattr(channel, "category_id", None)
        if cat_id == Config.TICKET_REWARD:
            await ticket_manager.handle_ticket_member_add(channel, member)
            await interaction.response.send_message(f"> **Added {member.mention} to reward ticket.**")
        else:
            await interaction.response.send_message("> **🚫 You can't use this command here!**", ephemeral=True, delete_after=10)

    @reward_group.command(name="remove", description="Remove a member from reward ticket")
    @app_commands.describe(member="The member to remove")
    async def reward_remove(interaction: discord.Interaction, member: discord.Member):
        if not is_staff(interaction.user):
            await interaction.response.send_message(embed=make_no_permission_embed(), ephemeral=True, delete_after=10)
            return

        channel = interaction.channel
        cat_id = getattr(channel, "category_id", None)
        if cat_id == Config.TICKET_REWARD:
            await ticket_manager.handle_ticket_member_remove(channel, member)
            await interaction.response.send_message(f"> **Removed {member.mention} from reward ticket.**")
        else:
            await interaction.response.send_message("> **🚫 You can't use this command here!**", ephemeral=True, delete_after=10)

    @reward_group.command(name="close", description="Close the reward ticket")
    async def reward_close(interaction: discord.Interaction):
        if not is_staff(interaction.user):
            await interaction.response.send_message(embed=make_no_permission_embed(), ephemeral=True, delete_after=10)
            return

        channel = interaction.channel
        cat_id = getattr(channel, "category_id", None)
        if cat_id == Config.TICKET_REWARD:
            await interaction.response.send_message(embed=ticket_embeds.make_reward_close_embed(), view=buttons.create_reward_close_view())
        else:
            await interaction.response.send_message("> **🚫 You can't use this command here!**", ephemeral=True, delete_after=10)

    tree.add_command(reward_group, guild=guild)
