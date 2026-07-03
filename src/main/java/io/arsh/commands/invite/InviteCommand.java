package io.arsh.commands.invite;

import io.arsh.commands.Command;
import io.arsh.invite.InviteManager;
import io.arsh.utils.Config;
import io.arsh.utils.Logger;
import net.dv8tion.jda.api.entities.Member;
import net.dv8tion.jda.api.events.interaction.command.SlashCommandInteractionEvent;
import net.dv8tion.jda.api.interactions.commands.OptionType;
import net.dv8tion.jda.api.interactions.commands.build.CommandData;
import net.dv8tion.jda.api.interactions.commands.build.Commands;
import net.dv8tion.jda.api.interactions.commands.build.SubcommandData;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CompletableFuture;

public class InviteCommand extends Command {

    private final InviteManager inviteManager;

    public InviteCommand(InviteManager inviteManager) {
        this.inviteManager = inviteManager;
    }

    @Override
    public String getName() {
        return "invite";
    }

    public CommandData getCommandData() {
        return Commands.slash("invite", "Use to get your invites.")
                .addSubcommands(
                        new SubcommandData("count", "Get the number of invites for a member.")
                                .addOption(OptionType.USER, "member", "Select member to get their invites.", false),
                        new SubcommandData("list", "To get all members that you invited.")
                                .addOption(OptionType.USER, "member", "Select member to reset their invites."),
                        new SubcommandData("reset", "Use to reset player invites.")
                                .addOption(OptionType.USER, "member", "Select member to reset their invites.")
                );
    }

    @Override
    public void execute(SlashCommandInteractionEvent event) {
        String subcommand = event.getSubcommandName();
        Member memberOption = event.getOption("member") != null ? event.getOption("member").getAsMember() : null;
        Member executor = event.getMember();

        if (subcommand == null) {
            event.reply("You currently have `" + inviteManager.getInvites(executor) + "` invites.").setEphemeral(true).queue();
            return;
        }

        switch (subcommand) {
            case "count":
                if (memberOption == null) {
                    if (inviteManager.getInvites(executor) == 0) {
                        event.reply("You don't have any invites yet.").setEphemeral(true).queue();
                        return;
                    }
                    event.reply("You currently have `" + inviteManager.getInvites(executor) + "` invites.").setEphemeral(true).queue();
                    return;
                }
                if (!executor.getRoles().contains(event.getGuild().getRoleById(Config.STAFF_ROLE_ID))) {
                    event.reply("> **🚫 You don't have permission to use this command!**").setEphemeral(true).queue();
                    return;
                }
                if (inviteManager.getInvites(memberOption) == 0) {
                    event.reply("Member `" + memberOption.getUser().getName() + "` don't have any invites yet.").queue();
                    return;
                }
                event.reply("Member `" + memberOption.getUser().getName() + "` has `" + inviteManager.getInvites(memberOption) + "` invites.").queue();
                break;

            case "list":
                if (memberOption != null) {
                    if (!executor.getRoles().contains(event.getGuild().getRoleById(Config.STAFF_ROLE_ID))) {
                        event.reply("> **🚫 You don't have permission to use this command!**").setEphemeral(true).queue();
                        return;
                    }
                    if (inviteManager.getInvites(memberOption) == 0) {
                        event.reply("You don't have any invites yet.").setEphemeral(true).queue();
                        return;
                    }
                    List<String> ids = inviteManager.getInviteRecord(memberOption).invitedUserIds();
                    List<CompletableFuture<String>> futures = new ArrayList<>();
                    for (String id : ids) {
                        CompletableFuture<String> future = new CompletableFuture<>();
                        event.getGuild().retrieveMemberById(id).queue(
                                member -> future.complete(member.getEffectiveName()),
                                error -> future.complete("Unknown user")
                        );
                        futures.add(future);
                    }
                    CompletableFuture.allOf(futures.toArray(new CompletableFuture[0])).thenRun(() -> {
                        StringBuilder list = new StringBuilder("```");
                        for (CompletableFuture<String> future : futures) {
                            list.append(future.join()).append("\n");
                        }
                        list.append("```");
                        event.reply(list.toString()).queue();
                    });
                    return;
                }
                if (inviteManager.getInvites(executor) == 0) {
                    event.reply("You don't have any invites yet.").setEphemeral(true).queue();
                    return;
                }
                List<String> ids = inviteManager.getInviteRecord(executor).invitedUserIds();
                List<CompletableFuture<String>> futures = new ArrayList<>();
                for (String id : ids) {
                    CompletableFuture<String> future = new CompletableFuture<>();
                    event.getGuild().retrieveMemberById(id).queue(
                            member -> future.complete(member.getEffectiveName()),
                            error -> future.complete("Unknown user")
                    );
                    futures.add(future);
                }
                CompletableFuture.allOf(futures.toArray(new CompletableFuture[0])).thenRun(() -> {
                    StringBuilder list = new StringBuilder("```");
                    for (CompletableFuture<String> future : futures) {
                        list.append(future.join()).append("\n");
                    }
                    list.append("```");
                    event.reply(list.toString()).setEphemeral(true).queue();
                });
                break;

            case "reset":
                if (!executor.getRoles().contains(event.getGuild().getRoleById(Config.STAFF_ROLE_ID))) {
                    event.reply("> **🚫 You don't have permission to use this command!**").setEphemeral(true).queue();
                    return;
                }
                if (memberOption == null) {
                    event.reply("> **🚫 Please provide a member whose invites is to be reset.**").setEphemeral(true).queue();
                    return;
                }
                if (inviteManager.getInvites(memberOption) == 0) {
                    event.reply("Member `" + memberOption.getUser().getName() + "` don't have any invites yet.").queue();
                    return;
                }
                inviteManager.resetInvites(memberOption);
                event.reply("Invites for member `" + memberOption.getUser().getName() + "` have been reset!").queue();
                Logger.warn("Invites for member `" + memberOption.getUser().getName() + "` have been reset by `" + executor.getUser().getName() + "`. ", true);
                break;
        }
    }


}
