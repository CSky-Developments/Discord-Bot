package io.arsh.utils;


import net.dv8tion.jda.api.entities.channel.concrete.TextChannel;
import org.slf4j.LoggerFactory;

public class Logger {

    private static final org.slf4j.Logger log = LoggerFactory.getLogger("discord-bot");
    private static TextChannel logChannel = null;

    public static void setLogChannel(TextChannel channel) {
        logChannel = channel;
    }

    public static void info(String message, boolean sendToDiscord) {
        log.info(message.replace("`", "").replace("*", ""));
        if (sendToDiscord) sendToDiscord("**INFO** " + message);
    }

    public static void warn(String message, boolean sendToDiscord) {
        log.warn(message);
        if (sendToDiscord) sendToDiscord("**WARN** " + message);
    }

    public static void error(String message, boolean sendToDiscord) {
        log.error(message);
        if (sendToDiscord)  sendToDiscord("**ERROR** " + message);
    }

    public static void info(String message) {
        log.info(message.replace("`", "").replace("*", ""));
    }

    public static void warn(String message) {
        log.warn(message);
    }

    public static void error(String message) {
        log.error(message);
    }

    public static void debug(String message) {
        log.debug(message);
    }

    private static void sendToDiscord(String message) {
        if (logChannel != null) {
            logChannel.sendMessage(message).queue();
        }
    }
}
