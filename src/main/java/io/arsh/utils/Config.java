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

        try (InputStream in = Config.class.getResourceAsStream("/config.yml")) {
            if (in == null) {
                Logger.error("Configuration file 'config.yml' not found in resources.", false);
                System.exit(1);
            }

            Map<String, Object> data = yaml.load(in);

            TOKEN = getValue(data, "Token");
            GUILD_ID = getValue(data, "Guild-ID");
            LOG_CHANNEL_ID = getValue(data, "Log-Channel-ID");
            MEMBER_COUNT_CHANNEL_ID = getValue(data, "Member-Count-Channel-ID");
            COUNTING_CHANNEL_ID = getValue(data, "Counting-Channel-ID");
            STAFF_ROLE_ID = getValue(data, "Staff-Role-ID");
            MEMBER_ROLE_ID = getValue(data, "Member-Role-ID");
            AI_KEY = getValue(data, "AI-Key");
            SUPPORT_CATEGORY_ID = getValue(data, "Support-Category-ID");
            TICKET_CHANNEL_ID = getValue(data, "Ticket-Channel-ID");
            TICKET_NORMAL = getValue(data, "Ticket-Normal-Category");
            TICKET_ORDER = getValue(data, "Ticket-Order-Category");
            TICKET_PLUGIN_GEN = getValue(data, "Ticket-Plugin-Generation-Category");
            TICKET_REWARD = getValue(data, "Ticket-Reward-Category");
            TICKET_STAFF_APP = getValue(data, "Ticket-Staff-App-Category");
            LICENSE_GEN_ACCESS_ID_LIST = (List<String>) getValueObject(data, "License-Gen-Access-IDs");
            PLUGIN_GEN_ACCESS_ROLE_ID = getValue(data, "Plugin-Gen-Access-Role-ID");
            Logger.info("Configuration loaded successfully.", false);

        } catch (Exception e) {
            Logger.error("Failed to load configuration: " + e.getMessage(), false);
            System.exit(1);
        }
    }

    private static String getValue(Map<String, Object> data, String key) {
        Object value = data.get(key);
        if (value == null) {
            Logger.error("Missing required config value for key: '" + key + "'", false);
            System.exit(1);
        }
        return value.toString();
    }

    private static Object getValueObject(Map<String, Object> data, String key) {
        Object value = data.get(key);
        if (value == null) {
            Logger.error("Missing required config value for key: '" + key + "'", false);
            System.exit(1);
        }
        return value;
    }
}
