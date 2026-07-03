package io.arsh.commands.ticket;

import io.arsh.commands.Command;
import io.arsh.ticket.TicketButtons;
import io.arsh.ticket.TicketEmbeds;
import io.arsh.ticket.TicketManager;
import io.arsh.utils.Config;
import net.dv8tion.jda.api.EmbedBuilder;
import net.dv8tion.jda.api.entities.Role;
import net.dv8tion.jda.api.events.interaction.command.SlashCommandInteractionEvent;
import net.dv8tion.jda.api.interactions.commands.OptionType;
import net.dv8tion.jda.api.interactions.commands.build.CommandData;
import net.dv8tion.jda.api.interactions.commands.build.Commands;
import net.dv8tion.jda.api.interactions.commands.build.SubcommandData;

import net.dv8tion.jda.api.entities.Member;

import java.awt.*;
import java.util.concurrent.TimeUnit;

public class OrderCommand extends Command {

    private final TicketManager ticketManager;

    public OrderCommand(TicketManager ticketManager) {
        this.ticketManager = ticketManager;
    }

    @Override
    public String getName() {
        return "order";
    }

    @Override
    public CommandData getCommandData() {
        return Commands.slash("order", "To place a new order.")
                .addSubcommands(
                        new SubcommandData("create", "To place a new order."),
                        new SubcommandData("add", "Add a member to the order")
                                .addOption(OptionType.USER, "member", "The member to add", true),
                        new SubcommandData("remove", "Remove a member from the order")
                                .addOption(OptionType.USER, "member", "The member to remove", true),
                        new SubcommandData("close", "Close the order")
                );
    }

    @Override
    public void execute(SlashCommandInteractionEvent event) {
        String subcommand = event.getSubcommandName();

        if (event.getMember().getRoles().stream()
                .map(Role::getId)
                .noneMatch(id -> id.equals(Config.STAFF_ROLE_ID))) {

            EmbedBuilder noPermissions = new EmbedBuilder()
                    .setColor(new Color(0x0090FF))
                    .setTitle("**NO PERMISSIONS**")
                    .setDescription("**You must be a staff member to do that.**")
                    .setFooter("・CSky Developments", "https://cdn.discordapp.com/attachments/1112390125276631080/1112442565766168808/CSkyDevelopements.png");

            event.replyEmbeds(noPermissions.build())
                    .setEphemeral(true)
                    .queue(success -> success.deleteOriginal().queueAfter(10, TimeUnit.SECONDS));
            return;
        }
        switch (subcommand) {
            case "create":
                event.replyEmbeds(TicketEmbeds.orderEmbed.build()).addComponents(TicketButtons.orderCreateRow).queue();
             break;

            case "add":
                Member memberToAdd = event.getOption("member").getAsMember();
                if (event.getChannel().asTextChannel().getParentCategoryId().equalsIgnoreCase(Config.TICKET_ORDER)) {
                    ticketManager.handleTicketMemberAdd(event.getChannel().asTextChannel(), memberToAdd);
                    event.reply("> **Added " + memberToAdd.getAsMention() + " to the order.**").queue();
                } else event.reply("> **🚫 You can't use this command here!**").setEphemeral(true).queue(success -> success.deleteOriginal().queueAfter(10, TimeUnit.SECONDS));
                break;

            case "remove":
                if (event.getChannel().asTextChannel().getParentCategoryId().equalsIgnoreCase(Config.TICKET_ORDER)) {
                    Member memberToRemove = event.getOption("member").getAsMember();
                    ticketManager.handleTicketMemberRemove(event.getChannel().asTextChannel(), memberToRemove);
                    event.reply("> **Removed " + memberToRemove.getAsMention() + " from the order.**").queue();
                } else event.reply("> **🚫 You can't use this command here!**").setEphemeral(true).queue(success -> success.deleteOriginal().queueAfter(10, TimeUnit.SECONDS));
                break;

            case "close":
                if (event.getChannel().asTextChannel().getParentCategoryId().equalsIgnoreCase(Config.TICKET_ORDER)) {
                    event.replyEmbeds(TicketEmbeds.orderCloseEmbed.build()).addComponents(TicketButtons.orderCloseRow).queue();
                } else event.reply("> **🚫 You can't use this command here!**").setEphemeral(true).queue(success -> success.deleteOriginal().queueAfter(10, TimeUnit.SECONDS));
                break;

            default:
                event.reply("> **Unknown subcommand.**").setEphemeral(true).queue();
        }
    }
}
