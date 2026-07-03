package io.arsh.commands.general;

import io.arsh.commands.Command;
import io.arsh.license.Generator;
import io.arsh.license.models.License;
import io.arsh.utils.Config;
import io.arsh.utils.Logger;
import net.dv8tion.jda.api.events.interaction.command.SlashCommandInteractionEvent;
import net.dv8tion.jda.api.interactions.commands.OptionType;
import net.dv8tion.jda.api.interactions.commands.build.CommandData;
import net.dv8tion.jda.api.interactions.commands.build.Commands;
import net.dv8tion.jda.api.interactions.commands.build.OptionData;
import net.dv8tion.jda.api.utils.FileUpload;
import net.dv8tion.jda.api.Permission;
import net.dv8tion.jda.api.interactions.commands.DefaultMemberPermissions;

import java.io.File;
import java.util.List;

public class LicenseCommand extends Command {

    @Override
    public String getName() {
        return "license";
    }

    @Override
    public CommandData getCommandData() {
        OptionData pluginOption = new OptionData(OptionType.STRING, "plugin", "Select the plugin", true);
        for (License license : License.values()) {
            pluginOption.addChoice(license.name() ,license.name());
        }

        return Commands.slash("license", "Generate a plugin license key")
                .setDefaultPermissions(DefaultMemberPermissions.enabledFor(Permission.ADMINISTRATOR))
                .addOptions(pluginOption)
                .addOption(OptionType.STRING, "uuid", "Server UUID", true)
                .addOption(OptionType.STRING, "ip", "Server IP Address", true)
                .addOption(OptionType.INTEGER, "port", "Server port", true);
    }

    @Override
    public void execute(SlashCommandInteractionEvent event) {
        event.deferReply(false).queue();

        String pluginName = event.getOption("plugin").getAsString();
        String uuid = event.getOption("uuid").getAsString();
        String ip = event.getOption("ip").getAsString();
        int port = event.getOption("port").getAsInt();

        if (!Config.LICENSE_GEN_ACCESS_ID_LIST.contains(event.getMember().getId())) {

            List<String> mentions = Config.LICENSE_GEN_ACCESS_ID_LIST.stream()
                    .map(id -> {
                        var member = event.getGuild().getMemberById(id);
                        return member != null ? member.getAsMention() : "`Unknown Member`";
                    })
                    .toList();

            String message;

            if (mentions.isEmpty()) {
                message = "No one is authorized to generate the license for " + pluginName + "!";
            } else if (mentions.size() == 1) {
                message = "Only " + mentions.get(0) + " can generate the license for " + pluginName + "!";
            } else {
                String all = String.join(", ", mentions.subList(0, mentions.size() - 1));
                message = "Only " + all + " and " + mentions.get(mentions.size() - 1) +
                        " can generate the license for " + pluginName + "!";
            }

            event.reply(message).setEphemeral(true).queue();
            return;
        }

        Logger.info("License generation request received.", true);
        Logger.info(String.format("""
                ───────── License Request Details ─────────
                Plugin: %s
                UUID: %s
                IP: %s
                Port: %d
                Requested By: %s
                ───────────────────────────────────────────
                """, pluginName, uuid, ip, port, event.getMember().getUser().getAsTag()), true);

        License license;
        try {
            license = License.valueOf(pluginName);
        } catch (IllegalArgumentException e) {
            Logger.warn("Invalid plugin name: " + pluginName, true);
            event.getHook().sendMessage("❌ Invalid plugin name.").setEphemeral(true).queue();
            return;
        }

        File licenseFile;
        try {
            Logger.info("Starting license file generation...", true);
            licenseFile = generateLicenseFile(license, ip, port, uuid);
        } catch (Exception e) {
            Logger.error("License generation failed: " + e.getMessage(), true);
            e.printStackTrace();
            event.getHook().sendMessage("⚠️ Failed to generate license. Check server logs for details.").setEphemeral(true).queue();
            return;
        }

        if (licenseFile != null && licenseFile.exists()) {
            Logger.info(String.format("License generated successfully for %s (%s)", pluginName, uuid), true);
            event.getHook()
                    .sendMessage("✅ License successfully generated for **" + pluginName + "**!")
                    .addFiles(FileUpload.fromData(licenseFile))
                    .setEphemeral(false)
                    .queue();
        } else {
            Logger.error("License file not found after generation process.", true);
            event.getHook().sendMessage("❌ Something went wrong while generating the license file. Please check the console.").setEphemeral(true).queue();
        }
    }

    private File generateLicenseFile(License license, String ip, int port, String uuid) throws Exception {
        var method = Generator.class.getDeclaredMethod("getLicenseFile", License.class, String.class, int.class, String.class);
        method.setAccessible(true);
        return (File) method.invoke(null, license, ip, port, uuid);
    }
}

