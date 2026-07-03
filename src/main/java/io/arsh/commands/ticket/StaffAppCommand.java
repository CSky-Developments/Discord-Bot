package io.arsh.commands.ticket;

import io.arsh.commands.Command;
import io.arsh.ticket.TicketButtons;
import io.arsh.ticket.TicketEmbeds;
import io.arsh.utils.Config;
import net.dv8tion.jda.api.EmbedBuilder;
import net.dv8tion.jda.api.entities.Role;
import net.dv8tion.jda.api.events.interaction.command.SlashCommandInteractionEvent;
import net.dv8tion.jda.api.interactions.commands.build.CommandData;
import net.dv8tion.jda.api.interactions.commands.build.Commands;
import net.dv8tion.jda.api.interactions.commands.build.SubcommandData;


import java.awt.*;
import java.util.concurrent.TimeUnit;

public class StaffAppCommand extends Command {

    @Override
    public String getName() {
        return "staffapp";
    }

    @Override
    public CommandData getCommandData() {
        return Commands.slash("staffapp", "Create a staff application.")
                .addSubcommands(
                        new SubcommandData("apply", "Create a staff application."),
                        new SubcommandData("close", "Close staff application ticket")
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
            case "apply":
                event.replyEmbeds(TicketEmbeds.staffAppEmbed.build()).addComponents(TicketButtons.appCreateRow).queue();
                 break;

            case "close":
                if (event.getChannel().asTextChannel().getParentCategoryId().equalsIgnoreCase(Config.TICKET_STAFF_APP)) {
                    event.replyEmbeds(TicketEmbeds.staffAppCloseEmbed.build()).addComponents(TicketButtons.appDeleteRow).queue();
                } else event.reply("> **🚫 You can't use this command here!**").setEphemeral(true).queue(success -> success.deleteOriginal().queueAfter(10, TimeUnit.SECONDS));
                break;

            default:
                event.reply("> **Unknown subcommand.**").setEphemeral(true).queue(success -> success.deleteOriginal().queueAfter(10, TimeUnit.SECONDS));
        }
    }
}
