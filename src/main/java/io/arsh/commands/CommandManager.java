package io.arsh.commands;

import io.arsh.commands.general.*;
import io.arsh.commands.invite.*;
import io.arsh.commands.ticket.*;
import io.arsh.invite.InviteManager;
import io.arsh.ticket.TicketManager;
import io.arsh.utils.Logger;
import net.dv8tion.jda.api.entities.Guild;
import net.dv8tion.jda.api.events.interaction.command.SlashCommandInteractionEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;
import net.dv8tion.jda.api.interactions.commands.build.CommandData;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class CommandManager extends ListenerAdapter {
    private final Guild guild;
    private final TicketManager ticketManager;
    private final InviteManager inviteManager;
    private final Map<String, Command> commandMap = new HashMap<>();

    public CommandManager(Guild guild, TicketManager ticketManager, InviteManager inviteManager) {
        this.guild = guild;
        this.ticketManager = ticketManager;
        this.inviteManager = inviteManager;
        registerCommands();
    }

    private void registerCommands() {
        List<Command> commands = new ArrayList<>();
        commands.add(new PingCommand());
        commands.add(new EmbedCommand());
        commands.add(new InviteCommand(inviteManager));
        commands.add(new TicketCommand(ticketManager));
        commands.add(new OrderCommand(ticketManager));
        commands.add(new PluginGenCommand(ticketManager));
        commands.add(new RewardCommand(ticketManager));
        commands.add(new StaffAppCommand());
        commands.add(new LicenseCommand());

        List<CommandData> commandDataList = new ArrayList<>();
        for (Command command : commands) {
            commandMap.put(command.getName(), command);
            commandDataList.add(command.getCommandData());
            Logger.info("Preparing to register command: /" + command.getName(), true);
        }

        guild.updateCommands()
                .addCommands(commandDataList)
                .queue(
                        c -> Logger.info("Successfully registered " + commandDataList.size() + " commands for guild " + guild.getName(), false),
                        error -> Logger.error("Failed to register commands for guild " + guild.getName() + ": " + error.getMessage(), false)
                );
    }

    @Override
    public void onSlashCommandInteraction(SlashCommandInteractionEvent event) {
        Command command = commandMap.get(event.getName());
        if (command != null) {
                command.execute(event);
                Logger.info(event.getUser().getAsMention() + " executed command /" + command.getName(), false);
        } else {
            event.reply("Unknown command.").setEphemeral(true).queue();
            Logger.error("Unknown command executed: /" + event.getName(), true);
        }
    }

}