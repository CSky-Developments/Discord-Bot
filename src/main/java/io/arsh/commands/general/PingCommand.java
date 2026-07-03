package io.arsh.commands.general;

import io.arsh.commands.Command;
import net.dv8tion.jda.api.events.interaction.command.SlashCommandInteractionEvent;
import net.dv8tion.jda.api.interactions.commands.build.CommandData;
import net.dv8tion.jda.api.interactions.commands.build.Commands;

public class PingCommand extends Command {
    @Override
    public String getName() {
        return "ping";
    }

    @Override
    public CommandData getCommandData() {
        return Commands.slash("ping", "Replies with Pong!");
    }

    @Override
    public void execute(SlashCommandInteractionEvent event) {
        event.reply("🏓 **Pong!**").queue();
    }
}
