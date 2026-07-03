package io.arsh.invite;

import io.arsh.utils.Config;
import io.arsh.utils.Logger;
import net.dv8tion.jda.api.entities.Guild;
import net.dv8tion.jda.api.entities.Invite;
import net.dv8tion.jda.api.entities.Member;
import net.dv8tion.jda.api.entities.Role;
import net.dv8tion.jda.api.entities.channel.concrete.VoiceChannel;
import net.dv8tion.jda.api.events.guild.member.GuildMemberJoinEvent;
import net.dv8tion.jda.api.events.guild.member.GuildMemberRemoveEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;
import net.dv8tion.jda.api.managers.channel.concrete.VoiceChannelManager;
import org.jetbrains.annotations.NotNull;

public class InviteTracker extends ListenerAdapter {

    private final Guild guild;
    private final InviteManager inviteManager;

    public InviteTracker(Guild guild, InviteManager inviteManager) {
        this.guild = guild;
        this.inviteManager = inviteManager;
        updateMemberCount();
        this.guild.retrieveInvites().queue(inviteManager::cacheInvites);
    }

    @Override
    public void onGuildMemberJoin(@NotNull GuildMemberJoinEvent event) {
        Member newMember = event.getMember();
        if (newMember.getUser().isBot()) {
            Logger.warn("Bot `" + newMember.getUser().getName() + "` joined the server.", true);
            return;
        }

        this.guild.retrieveInvites().queue(currentInvites -> {
            Invite usedInvite = inviteManager.getUsedInvite(currentInvites);
            inviteManager.cacheInvites(currentInvites);

            if (usedInvite != null && usedInvite.getInviter() != null) {
                Member inviter = this.guild.getMember(usedInvite.getInviter());
                if (inviter != null) {
                    Logger.info("`" + newMember.getUser().getName() + "` joined using invite from `" + inviter.getUser().getName() + "`.", true);
                    inviteManager.addInvite(inviter, newMember);
                } else {
                    Logger.info("`" + newMember.getUser().getName() + "` joined via a now-invalid invite (inviter left).", true);
                }
            } else {
                Logger.info("`" + newMember.getUser().getName() + "` joined the server (invite source unknown or expired).", true);
            }

            addMemberRole(newMember);
            updateMemberCount();
        }, throwable -> {
            Logger.error("Failed to retrieve invites: " + throwable.getMessage(), false);
            addMemberRole(newMember);
            updateMemberCount();
        });
    }

    @Override
    public void onGuildMemberRemove(@NotNull GuildMemberRemoveEvent event) {
        String leavingUserEffectiveName = event.getUser().getEffectiveName();
        String leavingUserId = event.getUser().getId();

        if (event.getUser().isBot()) {
            Logger.warn("Bot `" + leavingUserEffectiveName + "` left the server.", true);
            return;
        }

        Member inviter = inviteManager.getInviter(leavingUserId);

        if (inviter != null) {
            Member inviterMemberInGuild = this.guild.getMemberById(inviter.getId());
            if (inviterMemberInGuild != null) {
                inviteManager.removeInvite(inviterMemberInGuild.getId(), leavingUserId);
                Logger.info("Member `" + leavingUserEffectiveName + "` left the server. They were invited by `" + inviterMemberInGuild.getUser().getEffectiveName() + "`.", true);
            } else {
                inviteManager.removeInvite(inviter.getId(), leavingUserId);
                Logger.info("Member `" + leavingUserEffectiveName + "` left the server. Their inviter `"+ inviter.getId() +"` is no longer in this guild.", true);
            }
        } else {
            Logger.info("Member `" + leavingUserEffectiveName + "` left the server. Inviter unknown or not tracked.", true);
        }
        updateMemberCount();
    }

    private void addMemberRole(Member member) {
        if (Config.MEMBER_ROLE_ID == null || Config.MEMBER_ROLE_ID.isEmpty()) {
            Logger.warn("MEMBER_ROLE_ID is not configured. Cannot add role.", false);
            return;
        }
        Role memberRole = this.guild.getRoleById(Config.MEMBER_ROLE_ID);
        if (memberRole != null) {
            this.guild.addRoleToMember(member, memberRole).queue(
                    success -> Logger.info("Added role '" + memberRole.getName() + "' to " + member.getEffectiveName() + ".", false),
                    throwable -> Logger.error("Failed to add role '" + memberRole.getName() + "' to " + member.getEffectiveName() + ": " + throwable.getMessage(), true)
            );
        } else {
            Logger.error("Could not find role with ID: " + Config.MEMBER_ROLE_ID + ".", true);
        }
    }

    private void updateMemberCount() {
        if (Config.MEMBER_COUNT_CHANNEL_ID == null || Config.MEMBER_COUNT_CHANNEL_ID.isEmpty()) {
            Logger.warn("MEMBER_COUNT_CHANNEL_ID is not configured. Cannot update member count channel.", false);
            return;
        }

        VoiceChannel voiceChannel = this.guild.getVoiceChannelById(Config.MEMBER_COUNT_CHANNEL_ID);
        if (voiceChannel == null) {
            Logger.error("Member count voice channel with ID " + Config.MEMBER_COUNT_CHANNEL_ID + " not found.", false);
            return;
        }

        int count = this.guild.getMemberCount();
        String newName = "😎・Members: " + count;

        Logger.info("Attempting to update member count channel '" + voiceChannel.getName() + "' to '" + newName + "'.", false);

        if (voiceChannel.getName().equals(newName)) {
            Logger.info("Member count channel name is already up-to-date.", false);
            return;
        }

        VoiceChannelManager manager = voiceChannel.getManager().setName(newName);
        manager.queue(
                success -> Logger.info("Member count updated successfully to '" + newName + "'.", false),
                throwable -> Logger.error("Failed to update member count: " + throwable.getMessage(), true)
        );
    }
}