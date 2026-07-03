package io.arsh.commands.ticket;

import io.arsh.commands.Command;
import io.arsh.ticket.TicketButtons;
import io.arsh.ticket.TicketEmbeds;
import io.arsh.ticket.TicketManager;
import io.arsh.utils.Config;
import net.dv8tion.jda.api.EmbedBuilder;
import net.dv8tion.jda.api.entities.Member;
import net.dv8tion.jda.api.entities.Role;
import net.dv8tion.jda.api.events.interaction.command.SlashCommandInteractionEvent;
import net.dv8tion.jda.api.interactions.commands.OptionType;
import net.dv8tion.jda.api.interactions.commands.build.CommandData;
import net.dv8tion.jda.api.interactions.commands.build.Commands;
import net.dv8tion.jda.api.interactions.commands.build.SubcommandData;

import java.awt.*;
import java.util.concurrent.TimeUnit;

public class PluginGenCommand extends Command {

    private final TicketManager ticketManager;

    public PluginGenCommand(TicketManager ticketManager) {
        this.ticketManager = ticketManager;
    }

    @Override
    public String getName() {
        return "plugin";
    }

    @Override
    public CommandData getCommandData() {
        return Commands.slash("plugin", "Manage plugin generation requests.")
                .addSubcommands(
                        new SubcommandData("generate", "Start a new plugin generation request"),
                        new SubcommandData("add", "Add a member to the plugin ticket")
                                .addOption(OptionType.USER, "member", "The member to add", true),
                        new SubcommandData("remove", "Remove a member from the plugin ticket")
                                .addOption(OptionType.USER, "member", "The member to remove", true),
                        new SubcommandData("cancel", "Cancel the plugin generation request"));
    }

    @Override
    public void execute(SlashCommandInteractionEvent event) {
        String sub = event.getSubcommandName();

        if (sub == null) {
            event.reply("> **Please use a subcommand.**").setEphemeral(true).queue();
            return;
        }

        if (sub.equals("generate")) {
            if (event.getMember().getRoles().stream()
                    .map(Role::getId)
                    .noneMatch(id -> id.equals(Config.PLUGIN_GEN_ACCESS_ROLE_ID))) {

                EmbedBuilder noAccess = new EmbedBuilder()
                        .setColor(new Color(0xE74C3C))
                        .setTitle("**Access Denied**")
                        .setDescription(
                                "**You need the Plugin Generation subscription to use this service.**\n" +
                                        "This is a premium feature. Please create a ticket to subscribe.")
                        .setFooter("・CSky Developments",
                                "https://cdn.discordapp.com/attachments/1112390125276631080/1112442565766168808/CSkyDevelopements.png");

                event.replyEmbeds(noAccess.build())
                        .setEphemeral(true)
                        .queue(success -> success.deleteOriginal().queueAfter(15, TimeUnit.SECONDS));
                return;
            }
        }

        switch (sub) {
            case "generate":
                event.getChannel().asTextChannel().sendMessageEmbeds(TicketEmbeds.pluginGenEmbed.build())
                        .addComponents(TicketButtons.pluginGenerateRow)
                        .queue();
                break;

            case "add":
                if (!isStaff(event.getMember())) {
                    replyNoPermission(event);
                    return;
                }
                Member addMember = event.getOption("member").getAsMember();
                if (isInPluginCategory(event)) {
                    ticketManager.handleTicketMemberAdd(event.getChannel().asTextChannel(), addMember);
                    event.reply("> **Added " + addMember.getAsMention() + " to the plugin ticket.**").queue();
                } else {
                    event.reply("> **You can't use this command here!**").setEphemeral(true)
                            .queue(s -> s.deleteOriginal().queueAfter(10, TimeUnit.SECONDS));
                }
                break;

            case "remove":
                if (!isStaff(event.getMember())) {
                    replyNoPermission(event);
                    return;
                }
                Member removeMember = event.getOption("member").getAsMember();
                if (isInPluginCategory(event)) {
                    ticketManager.handleTicketMemberRemove(event.getChannel().asTextChannel(), removeMember);
                    event.reply("> **Removed " + removeMember.getAsMention() + " from the plugin ticket.**").queue();
                } else {
                    event.reply("> **You can't use this command here!**").setEphemeral(true)
                            .queue(s -> s.deleteOriginal().queueAfter(10, TimeUnit.SECONDS));
                }
                break;

            case "cancel":
                if (!isStaff(event.getMember())) {
                    replyNoPermission(event);
                    return;
                }
                if (isInPluginCategory(event)) {
                    event.replyEmbeds(TicketEmbeds.pluginGenCloseEmbed.build())
                            .addComponents(TicketButtons.pluginCancelConfirmRow)
                            .queue();
                } else {
                    event.reply("> **You can't use this command here!**").setEphemeral(true)
                            .queue(s -> s.deleteOriginal().queueAfter(10, TimeUnit.SECONDS));
                }
                break;

            default:
                event.reply("> **Unknown subcommand.**").setEphemeral(true)
                        .queue(s -> s.deleteOriginal().queueAfter(10, TimeUnit.SECONDS));
        }
    }

    private boolean isStaff(Member member) {
        return member.getRoles().stream()
                .map(Role::getId)
                .anyMatch(id -> id.equals(Config.STAFF_ROLE_ID));
    }

    private boolean isInPluginCategory(SlashCommandInteractionEvent event) {
        try {
            return event.getChannel().asTextChannel().getParentCategoryId().equalsIgnoreCase(Config.TICKET_PLUGIN_GEN);
        } catch (Exception e) {
            return false;
        }
    }

    private void replyNoPermission(SlashCommandInteractionEvent event) {
        EmbedBuilder noPermissions = new EmbedBuilder()
                .setColor(new Color(0x0090FF))
                .setTitle("**NO PERMISSIONS**")
                .setDescription("**You must be a staff member to do that.**")
                .setFooter("・CSky Developments",
                        "https://cdn.discordapp.com/attachments/1112390125276631080/1112442565766168808/CSkyDevelopements.png");

        event.replyEmbeds(noPermissions.build())
                .setEphemeral(true)
                .queue(success -> success.deleteOriginal().queueAfter(10, TimeUnit.SECONDS));
    }
}
