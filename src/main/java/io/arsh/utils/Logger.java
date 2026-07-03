package io.arsh.utils;


import net.dv8tion.jda.api.entities.channel.concrete.TextChannel;

import java.time.LocalTime;
import java.time.format.DateTimeFormatter;

public class Logger {

    private static final String RED = "\u001B[31m";
    private static final String YELLOW = "\u001B[33m";
    private static final String RESET = "\u001B[0m";

    private static TextChannel logChannel = null;

    public static void setLogChannel(TextChannel channel) {
        logChannel = channel;
    }

    public static String getTimeStamp() {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("HH:mm:ss");
        return "[" + LocalTime.now().format(formatter) + "]";
    }

    public static void info(String message, boolean sendToDiscord) {
        String log = getTimeStamp() + " [INFO] " + message.replace("`", "").replace("*", "");
        System.out.println(RESET + log + RESET);
        if (sendToDiscord) sendToDiscord("**INFO** " + message);
    }

    public static void warn(String message, boolean sendToDiscord) {
        String log = getTimeStamp() + " [WARN] " + message;
        System.out.println(YELLOW + log + RESET);
        if (sendToDiscord) sendToDiscord("**WARN** " + message);
    }

    public static void error(String message, boolean sendToDiscord) {
        String log = getTimeStamp() + " [ERROR] " + message;
        System.out.println(RED + log + RESET);
        if (sendToDiscord)  sendToDiscord("**ERROR** " + message);
    }

    private static void sendToDiscord(String message) {
        if (logChannel != null) {
            logChannel.sendMessage(message).queue();
        }
    }
}
