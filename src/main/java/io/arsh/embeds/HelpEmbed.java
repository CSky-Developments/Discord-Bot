package io.arsh.embeds;

import net.dv8tion.jda.api.EmbedBuilder;

import java.awt.*;

public class HelpEmbed {
    public static final EmbedBuilder helpEmbed = new EmbedBuilder()
            .setColor(new Color(0xFF0000))
            .setTitle("CSky Developments - Help Menu")
            .setDescription("Below is a list of all available commands for the CSky Developments bot. Use the prefix `c!` to execute these commands.")
            .addField("General Commands",
                    "**c!help** or **c!?** - Displays this help menu.\n**c!not available** - Shows information about unavailable services.", false)
            .addField("Support & Applications",
                    "**c!ticket** or **c!tickets** - Opens a support ticket.\n**c!staff application** or **c!staff app** - Information about staff applications.", false)
            .addField("Orders & Services",
                    "**c!order** - Places a new order.\n**c!plugin development** - Information about custom plugin development.", false)
            .addField("Server Optimizations",
                    "**c!optimization** - Lists all server optimization services.\n**c!bukkit optimization** - Bukkit server optimization.\n**c!spigot optimization** - Spigot server optimization.\n**c!paper optimization** - Paper server optimization.\n**c!purple optimization** - Purpur server optimization.\n**c!bungeecode optimization** - BungeeCord server optimization.\n**c!waterfall optimization** - Waterfall server optimization.\n**c!velocity optimization** - Velocity server optimization.\n**c!forge optimization** - Forge server optimization.\n**c!fabric optimization** - Fabric server optimization.", false)
            .addField("Rewards",
                    "**c!reward** or **c!rewards** - View available rewards.\n**c!invite reward** or **c!invite rewards** - Claim invite-based rewards.\n**c!booster reward** or **c!booster rewards** - Claim server booster rewards.", false)
            .setFooter("・CSky Developments", "https://cdn.discordapp.com/attachments/1112390125276631080/1112442565766168808/CSkyDevelopements.png");

    public static final EmbedBuilder notAvailableEmbed = new EmbedBuilder()
            .setColor(new Color(0xFF4C4C))
            .setTitle("🚫 Service Unavailable")
            .setDescription("""
                    **This service is currently not available.** \s
                    Please check back later or contact us for more information.
                   \s""")
            .setFooter("・CSky Developments", "https://cdn.discordapp.com/attachments/1112390125276631080/1112442565766168808/CSkyDevelopements.png");

}
