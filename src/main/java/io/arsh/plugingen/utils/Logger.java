package io.arsh.plugingen.utils;

public class Logger {

    private static boolean debug;

    public static void log(Level level, String message) {
        switch (level) {
            case INFO -> info(message);
            case WARN -> warn(message);
            case ERROR -> error(message);
            case DEBUG -> debug(message);
        }
    }

    public static void info(String message) {
        System.out.println(
                Color.WHITE +
                        "" +
                        Color.DARK_GRAY_BACKGROUND +
                        " INFO " +
                        Color.RESET +
                        Color.WHITE +
                        " " +
                        message +
                        Color.RESET);
    }

    public static void warn(String message) {
        System.out.println(
                Color.WHITE +
                        "" +
                        Color.YELLOW_BACKGROUND +
                        " WARN " +
                        Color.RESET +
                        Color.YELLOW_BRIGHT +
                        " " +
                        message +
                        Color.RESET);
    }

    public static void error(String message) {
        System.out.println(
                Color.WHITE +
                        "" +
                        Color.RED_BACKGROUND +
                        " EROR " +
                        Color.RESET +
                        Color.RED_BRIGHT +
                        " " +
                        message + Color.RESET);
    }

    public static void debug(String message) {
        if (debug) System.out.println(
                    Color.WHITE +
                            "" +
                            Color.BLUE_BACKGROUND +
                            " DBUG " +
                            Color.RESET +
                            Color.BLUE_BRIGHT +
                            " " +

                            message +
                            Color.RESET
            );
    }

    public static void debug(boolean debug) {
        Logger.debug = debug;
    }

    public enum Level {
        INFO,
        WARN,
        ERROR,
        DEBUG
    }

    private enum Color {

        RESET("\033[0m"),
        WHITE("\033[0;37m"),
        RED_BACKGROUND("\033[41m"),
        YELLOW_BACKGROUND("\033[43m"),
        BLUE_BACKGROUND("\033[44m"),
        DARK_GRAY_BACKGROUND("\033[48;5;238m"),

        RED_BRIGHT("\033[0;91m"),
        YELLOW_BRIGHT("\033[0;93m"),
        BLUE_BRIGHT("\033[0;94m");

        private final String code;

        Color(String code) {
            this.code = code;
        }

        @Override
        public String toString() {
            return code;
        }
    }

}
