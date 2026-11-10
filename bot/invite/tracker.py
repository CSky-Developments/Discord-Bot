import discord
from typing import Optional
from bot.config import Config
from bot.logger import BotLogger
from bot.invite.manager import InviteManager

class InviteTracker:
    def __init__(self, guild: discord.Guild, invite_manager: InviteManager):
        self.guild = guild
        self.invite_manager = invite_manager

    async def initialize(self):
        await self.update_member_count()
        try:
            invites = await self.guild.invites()
            self.invite_manager.cacheInvites(invites) if hasattr(self.invite_manager, "cacheInvites") else self.invite_manager.cache_invites(invites)
        except Exception as e:
            BotLogger.error(f"Failed to retrieve initial invites: {e}", False)

    async def on_member_join(self, member: discord.Member):
        if member.guild.id != self.guild.id:
            return

        if member.bot:
            BotLogger.warn(f"Bot `{member.name}` joined the server.", True)
            return

        used_invite = None
        try:
            current_invites = await self.guild.invites()
            used_invite = self.invite_manager.get_used_invite(current_invites)
            self.invite_manager.cache_invites(current_invites)
        except Exception as e:
            BotLogger.error(f"Failed to retrieve invites: {e}", False)

        if used_invite and used_invite.inviter:
            inviter = self.guild.get_member(used_invite.inviter.id)
            if inviter:
                BotLogger.info(f"`{member.name}` joined using invite from `{inviter.name}`.", True)
                self.invite_manager.add_invite(inviter.id, member.id)
            else:
                BotLogger.info(f"`{member.name}` joined via a now-invalid invite (inviter left).", True)
        else:
            BotLogger.info(f"`{member.name}` joined the server (invite source unknown or expired).", True)

        await self.add_member_role(member)
        await self.update_member_count()

    async def on_member_remove(self, member: discord.Member):
        if member.guild.id != self.guild.id:
            return

        leaving_user_effective_name = member.display_name
        leaving_user_id = str(member.id)

        if member.bot:
            BotLogger.warn(f"Bot `{leaving_user_effective_name}` left the server.", True)
            return

        inviter_id = self.invite_manager.get_inviter_id(leaving_user_id)
        if inviter_id:
            inviter_member = self.guild.get_member(int(inviter_id))
            if inviter_member:
                self.invite_manager.remove_invite(inviter_id, leaving_user_id)
                BotLogger.info(f"Member `{leaving_user_effective_name}` left the server. They were invited by `{inviter_member.display_name}`.", True)
            else:
                self.invite_manager.remove_invite(inviter_id, leaving_user_id)
                BotLogger.info(f"Member `{leaving_user_effective_name}` left the server. Their inviter `{inviter_id}` is no longer in this guild.", True)
        else:
            BotLogger.info(f"Member `{leaving_user_effective_name}` left the server. Inviter unknown or not tracked.", True)

        await self.update_member_count()

    async def add_member_role(self, member: discord.Member):
        if not Config.MEMBER_ROLE_ID:
            BotLogger.warn("MEMBER_ROLE_ID is not configured. Cannot add role.", False)
            return

        member_role = self.guild.get_role(Config.MEMBER_ROLE_ID)
        if member_role:
            try:
                await member.add_roles(member_role)
                BotLogger.info(f"Added role '{member_role.name}' to {member.display_name}.", False)
            except Exception as e:
                BotLogger.error(f"Failed to add role '{member_role.name}' to {member.display_name}: {e}", True)
        else:
            BotLogger.error(f"Could not find role with ID: {Config.MEMBER_ROLE_ID}.", True)

    async def update_member_count(self):
        if not Config.MEMBER_COUNT_CHANNEL_ID:
            BotLogger.warn("MEMBER_COUNT_CHANNEL_ID is not configured. Cannot update member count channel.", False)
            return

        voice_channel = self.guild.get_channel(Config.MEMBER_COUNT_CHANNEL_ID)
        if not voice_channel or not isinstance(voice_channel, discord.VoiceChannel):
            BotLogger.error(f"Member count voice channel with ID {Config.MEMBER_COUNT_CHANNEL_ID} not found.", False)
            return

        count = self.guild.member_count or len(self.guild.members)
        new_name = f"😎・Members: {count}"

        BotLogger.info(f"Attempting to update member count channel '{voice_channel.name}' to '{new_name}'.", False)

        if voice_channel.name == new_name:
            BotLogger.info("Member count channel name is already up-to-date.", False)
            return

        try:
            await voice_channel.edit(name=new_name)
            BotLogger.info(f"Member count updated successfully to '{new_name}'.", False)
        except Exception as e:
            BotLogger.error(f"Failed to update member count: {e}", True)
