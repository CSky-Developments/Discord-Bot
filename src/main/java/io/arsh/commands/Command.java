package io.arsh.commands;

import net.dv8tion.jda.api.events.interaction.command.SlashCommandInteractionEvent;
import net.dv8tion.jda.api.interactions.commands.build.CommandData;

public abstract class Command {
    public abstract String getName();
    public abstract CommandData getCommandData();
    public abstract void execute(SlashCommandInteractionEvent event);
}
