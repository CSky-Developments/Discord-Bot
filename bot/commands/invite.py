from typing import Optional
import discord
from discord import app_commands
from bot.config import Config
from bot.logger import BotLogger
from bot.invite.manager import InviteManager

def setup_invite_command(tree: app_commands.CommandTree, guild: discord.Object, invite_manager: InviteManager):
    invite_group = app_commands.Group(name="invite", description="Use to get your invites.")

    @invite_group.command(name="count", description="Get the number of invites for a member.")
    @app_commands.describe(member="Select member to get their invites.")
    async def invite_count(interaction: discord.Interaction, member: Optional[discord.Member] = None):
        executor = interaction.user

        if member is None:
            count = invite_manager.get_invites(executor.id)
            if count == 0:
                await interaction.response.send_message("You don't have any invites yet.", ephemeral=True)
                return
            await interaction.response.send_message(f"You currently have `{count}` invites.", ephemeral=True)
            return

        has_staff_role = any(r.id == Config.STAFF_ROLE_ID for r in executor.roles) if isinstance(executor, discord.Member) else False
        if not has_staff_role:
            await interaction.response.send_message("> **🚫 You don't have permission to use this command!**", ephemeral=True)
            return

        count = invite_manager.get_invites(member.id)
        if count == 0:
            await interaction.response.send_message(f"Member `{member.name}` don't have any invites yet.")
            return

        await interaction.response.send_message(f"Member `{member.name}` has `{count}` invites.")

    @invite_group.command(name="list", description="To get all members that you invited.")
    @app_commands.describe(member="Select member to view their invited members.")
    async def invite_list(interaction: discord.Interaction, member: Optional[discord.Member] = None):
        executor = interaction.user
        target_member = member or executor
        is_targeted = member is not None

        if is_targeted:
            has_staff_role = any(r.id == Config.STAFF_ROLE_ID for r in executor.roles) if isinstance(executor, discord.Member) else False
            if not has_staff_role:
                await interaction.response.send_message("> **🚫 You don't have permission to use this command!**", ephemeral=True)
                return

        count = invite_manager.get_invites(target_member.id)
        if count == 0:
            await interaction.response.send_message("You don't have any invites yet.", ephemeral=True)
            return

        record = invite_manager.get_invite_record(target_member.id)
        user_ids = record.invited_user_ids if record else []

        names = []
        for uid in user_ids:
            m = interaction.guild.get_member(int(uid)) if interaction.guild else None
            names.append(m.display_name if m else "Unknown user")

        list_str = "```\n" + "\n".join(names) + "\n```"
        await interaction.response.send_message(list_str, ephemeral=(not is_targeted))

    @invite_group.command(name="reset", description="Use to reset player invites.")
    @app_commands.describe(member="Select member to reset their invites.")
    async def invite_reset(interaction: discord.Interaction, member: discord.Member):
        executor = interaction.user
        has_staff_role = any(r.id == Config.STAFF_ROLE_ID for r in executor.roles) if isinstance(executor, discord.Member) else False
        if not has_staff_role:
            await interaction.response.send_message("> **🚫 You don't have permission to use this command!**", ephemeral=True)
            return

        count = invite_manager.get_invites(member.id)
        if count == 0:
            await interaction.response.send_message(f"Member `{member.name}` don't have any invites yet.")
            return

        invite_manager.reset_invites(member.id)
        await interaction.response.send_message(f"Invites for member `{member.name}` have been reset!")
        BotLogger.warn(f"Invites for member `{member.name}` have been reset by `{executor.name}`.", True)

    tree.add_command(invite_group, guild=guild)
