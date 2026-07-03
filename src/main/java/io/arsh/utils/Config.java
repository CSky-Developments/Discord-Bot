package io.arsh.utils;

import org.yaml.snakeyaml.Yaml;

import java.io.InputStream;
import java.util.List;
import java.util.Map;

public class Config {

    public static String TOKEN;
    public static String GUILD_ID;
    public static String LOG_CHANNEL_ID;
    public static String MEMBER_COUNT_CHANNEL_ID;
    public static String COUNTING_CHANNEL_ID;
    public static String STAFF_ROLE_ID;
    public static String MEMBER_ROLE_ID;

    public static String TICKET_NORMAL;
    public static String TICKET_ORDER;
    public static String TICKET_PLUGIN_GEN;
    public static String TICKET_REWARD;
    public static String TICKET_STAFF_APP;
    public static String AI_KEY;
    public static String TICKET_CHANNEL_ID;
    public static String SUPPORT_CATEGORY_ID;

    public static String PLUGIN_GEN_ACCESS_ROLE_ID;

    public static List<String> LICENSE_GEN_ACCESS_ID_LIST;

    public static void load() {
        Yaml yaml = new Yaml();
        Map<String, Object> data = null;
        
        try (InputStream in = Config.class.getResourceAsStream("/config.yml")) {
            if (in != null) {
                data = yaml.load(in);
                Logger.info("Loaded config.yml for local development fallback.", false);
            } else {
                Logger.info("No config.yml found. Relying strictly on Environment Variables.", false);
            }
        } catch (Exception e) {
            Logger.info("Failed to read config.yml, relying strictly on Environment Variables.", false);
        }

        TOKEN = getValue(data, "Token", "DISCORD_TOKEN");
        GUILD_ID = getValue(data, "Guild-ID", "GUILD_ID");
        LOG_CHANNEL_ID = getValue(data, "Log-Channel-ID", "LOG_CHANNEL_ID");
        MEMBER_COUNT_CHANNEL_ID = getValue(data, "Member-Count-Channel-ID", "MEMBER_COUNT_CHANNEL_ID");
        COUNTING_CHANNEL_ID = getValue(data, "Counting-Channel-ID", "COUNTING_CHANNEL_ID");
        STAFF_ROLE_ID = getValue(data, "Staff-Role-ID", "STAFF_ROLE_ID");
        MEMBER_ROLE_ID = getValue(data, "Member-Role-ID", "MEMBER_ROLE_ID");
        AI_KEY = getValue(data, "AI-Key", "AI_KEY");
        SUPPORT_CATEGORY_ID = getValue(data, "Support-Category-ID", "SUPPORT_CATEGORY_ID");
        TICKET_CHANNEL_ID = getValue(data, "Ticket-Channel-ID", "TICKET_CHANNEL_ID");
        TICKET_NORMAL = getValue(data, "Ticket-Normal-Category", "TICKET_NORMAL_CATEGORY");
        TICKET_ORDER = getValue(data, "Ticket-Order-Category", "TICKET_ORDER_CATEGORY");
        TICKET_PLUGIN_GEN = getValue(data, "Ticket-Plugin-Generation-Category", "TICKET_PLUGIN_GEN_CATEGORY");
        TICKET_REWARD = getValue(data, "Ticket-Reward-Category", "TICKET_REWARD_CATEGORY");
        TICKET_STAFF_APP = getValue(data, "Ticket-Staff-App-Category", "TICKET_STAFF_APP_CATEGORY");
        PLUGIN_GEN_ACCESS_ROLE_ID = getValue(data, "Plugin-Gen-Access-Role-ID", "PLUGIN_GEN_ACCESS_ROLE_ID");
        
        LICENSE_GEN_ACCESS_ID_LIST = getListValue(data, "License-Gen-Access-IDs", "LICENSE_GEN_ACCESS_IDS");

        Logger.info("Configuration loaded successfully.", false);
    }

    private static String getValue(Map<String, Object> data, String yamlKey, String envKey) {
        String envValue = System.getenv(envKey);
        if (envValue != null && !envValue.trim().isEmpty()) {
            return envValue.trim();
        }
        
        if (data != null && data.containsKey(yamlKey)) {
            Object value = data.get(yamlKey);
            if (value != null) {
                return value.toString();
            }
        }
        
        Logger.error("Missing required config value. Please set ENV: '" + envKey + "' (or '" + yamlKey + "' in config.yml)", false);
        System.exit(1);
        return null;
    }

    private static List<String> getListValue(Map<String, Object> data, String yamlKey, String envKey) {
        String envValue = System.getenv(envKey);
        if (envValue != null && !envValue.trim().isEmpty()) {
            return java.util.Arrays.asList(envValue.split(","));
        }
        
        if (data != null && data.containsKey(yamlKey)) {
            Object value = data.get(yamlKey);
            if (value != null) {
                return (List<String>) value;
            }
        }
        
        Logger.error("Missing required config value. Please set ENV: '" + envKey + "' (or '" + yamlKey + "' in config.yml)", false);
        System.exit(1);
        return null;
    }
}
