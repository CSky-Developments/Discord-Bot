package io.arsh.ticket;

import com.fasterxml.jackson.databind.ObjectMapper;
import io.arsh.plugingen.Builder;
import io.arsh.plugingen.models.Project;
import io.arsh.plugingen.services.GeminiService;
import io.arsh.utils.Config;
import io.arsh.utils.Logger;
import net.dv8tion.jda.api.EmbedBuilder;
import net.dv8tion.jda.api.Permission;
import net.dv8tion.jda.api.entities.Guild;
import net.dv8tion.jda.api.entities.Member;
import net.dv8tion.jda.api.entities.Message;
import net.dv8tion.jda.api.entities.Role;
import net.dv8tion.jda.api.entities.channel.concrete.Category;
import net.dv8tion.jda.api.entities.channel.concrete.TextChannel;
import net.dv8tion.jda.api.events.interaction.ModalInteractionEvent;
import net.dv8tion.jda.api.events.interaction.component.ButtonInteractionEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;
import net.dv8tion.jda.api.interactions.components.ActionRow;
import net.dv8tion.jda.api.interactions.components.text.TextInput;
import net.dv8tion.jda.api.interactions.components.text.TextInputStyle;
import net.dv8tion.jda.api.interactions.modals.Modal;
import net.dv8tion.jda.api.utils.FileUpload;
import org.jetbrains.annotations.NotNull;

import java.awt.*;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.time.Instant;
import java.util.*;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class TicketManager extends ListenerAdapter {

    private final Guild guild;

    private static final File TICKET_DATA_FILE = new File("./data/ticket_data.json");
    private static final ObjectMapper mapper = new ObjectMapper();
    private TicketData ticketData;

    public TicketManager(Guild guild) {
        Logger.info("Initializing ticket manager...", false);
        this.guild = guild;
        Logger.info("Loading ticket data...", false);
        loadTicketData();
        Logger.info("Successfully initialized ticket manager!", false);
    }

    public void loadTicketData() {
        if (!TICKET_DATA_FILE.exists()) {
            File parentDir = TICKET_DATA_FILE.getParentFile();
            if (parentDir != null && !parentDir.exists()) {
                parentDir.mkdirs();
            }
            ticketData = new TicketData();
            saveTicketData();
            return;
        }
        try {
            ticketData = mapper.readValue(TICKET_DATA_FILE, TicketData.class);
            Logger.info("Successfully Loaded ticket data!", false);
        } catch (IOException ex) {
            Logger.error("An error occurred while loading ticket data. Error: " + ex.getMessage(), false);
            ticketData = new TicketData();
        }
    }

    public void saveTicketData() {
        try {
            File parentDir = TICKET_DATA_FILE.getParentFile();
            if (parentDir != null && !parentDir.exists()) {
                parentDir.mkdirs();
            }
            mapper.writerWithDefaultPrettyPrinter().writeValue(TICKET_DATA_FILE, ticketData);
        } catch (IOException ex) {
            Logger.info("An error occurred while saving ticket data. Error: " + ex.getMessage(), false);
        }
    }

    @Override
    public void onButtonInteraction(ButtonInteractionEvent event) {
        String buttonId = event.getComponentId();
        Member member = event.getMember();
        TextChannel channel = event.getChannel().asTextChannel();

        switch (buttonId) {
            case "Ticket_Create_Button":
                handleCreateTicket(event, member, TicketType.NORMAL);
                break;
            case "Ticket_Close_Button":
                event.replyEmbeds(TicketEmbeds.ticketCloseEmbed.build())
                        .addComponents(TicketButtons.ticketCloseConfirmRow)
                        .setEphemeral(true)
                        .queue();
                break;
            case "Ticket_Close_Confirm_Button":
                handleCloseConfirm(event, member, channel, TicketType.NORMAL);
                break;
            case "Ticket_Close_Cancel_Button":
                event.replyEmbeds(TicketEmbeds.ticketCloseCancelEmbed.build())
                        .setEphemeral(true)
                        .queue(success -> success.deleteOriginal().queueAfter(10, TimeUnit.SECONDS));
                break;
            case "Ticket_Delete_Button":
                handleDeleteTicket(event, member, channel, TicketType.NORMAL);
                break;

            case "Order_Create_Button":
                handleCreateTicket(event, member, TicketType.ORDER);
                break;
            case "Order_Cancel_Button":
                event.replyEmbeds(TicketEmbeds.orderCloseEmbed.build())
                        .addComponents(TicketButtons.orderCloseConfirmRow)
                        .setEphemeral(true)
                        .queue();
                break;
            case "Server_Order_Create_Button":
                event.reply("Continue at https://discord.gg/Cftg5GT7vd")
                        .setEphemeral(true)
                        .queue();
                Logger.info("A server hosting order is requested by `" + event.getMember().getUser().getName() + "`.", true);
                break;
            case "Order_Cancel_Confirm_Button":
                handleCloseConfirm(event, member, channel, TicketType.ORDER);
                break;
            case "Order_Cancel_Cancel_Button":
                event.replyEmbeds(TicketEmbeds.orderCloseCancelEmbed.build())
                        .setEphemeral(true)
                        .queue(success -> success.deleteOriginal().queueAfter(10, TimeUnit.SECONDS));
                break;
            case "Order_Delete_Button":
                handleDeleteTicket(event, member, channel, TicketType.ORDER);
                break;

            case "Plugin_Generate_Button":
                handleCreateTicket(event, member, TicketType.PLUGIN_GEN);
                break;

            case "Plugin_Cancel_Button":
                event.replyEmbeds(TicketEmbeds.pluginGenCloseEmbed.build())
                        .addComponents(TicketButtons.pluginCancelConfirmRow)
                        .setEphemeral(true)
                        .queue();
                break;

            case "Plugin_Cancel_Confirm_Button":
                handleCloseConfirm(event, member, channel, TicketType.PLUGIN_GEN);
                break;

            case "Plugin_Cancel_Abort_Button":
                event.replyEmbeds(TicketEmbeds.pluginGenCloseCancelEmbed.build())
                        .setEphemeral(true)
                        .queue(success -> success.deleteOriginal().queueAfter(10, TimeUnit.SECONDS));
                break;

            case "Plugin_Delete_Button":
                handleDeleteTicket(event, member, channel, TicketType.PLUGIN_GEN);
                break;

            case "Reward_Claim_Button":
                handleCreateTicket(event, member, TicketType.REWARD);
                break;
            case "Reward_Close_Button":
                event.replyEmbeds(TicketEmbeds.rewardCloseEmbed.build())
                        .addComponents(TicketButtons.rewardCloseConfirmRow)
                        .setEphemeral(true)
                        .queue();
                break;
            case "Reward_Close_Confirm_Button":
                handleCloseConfirm(event, member, channel, TicketType.REWARD);
                break;
            case "Reward_Close_Cancel_Button":
                event.replyEmbeds(TicketEmbeds.rewardCloseCancelEmbed.build())
                        .setEphemeral(true)
                        .queue(success -> success.deleteOriginal().queueAfter(10, TimeUnit.SECONDS));
                break;
            case "Reward_Delete_Button":
                handleDeleteTicket(event, member, channel, TicketType.REWARD);
                break;

            case "Developer_Button":
            case "Moderator_Button":
            case "Supporter_Button":
                handleCreateTicket(event, member, TicketType.STAFF_APP);
                break;
            case "Developer_Close_Button":
            case "Moderator_Close_Button":
            case "Supporter_Close_Button":
                event.replyEmbeds(TicketEmbeds.staffAppCloseEmbed.build())
                        .addComponents(TicketButtons.appCloseConfirmRow)
                        .setEphemeral(true)
                        .queue();
                break;
            case "App_Close_Confirm_Button":
                handleCloseConfirm(event, member, channel, TicketType.STAFF_APP);
                break;
            case "App_Close_Cancel_Button":
                event.replyEmbeds(TicketEmbeds.staffAppCloseCancelEmbed.build())
                        .setEphemeral(true)
                        .queue(success -> success.deleteOriginal().queueAfter(10, TimeUnit.SECONDS));
                break;
            case "App_Delete_Button":
                handleDeleteTicket(event, member, channel, TicketType.STAFF_APP);
                break;
        }
    }

    public void handleTicketMemberAdd(TextChannel ticketChannel, Member member) {
        ticketChannel.getManager().putPermissionOverride(member, EnumSet.of(Permission.VIEW_CHANNEL), null).queue();
    }

    public void handleTicketMemberRemove(TextChannel ticketChannel, Member member) {
        ticketChannel.getManager().putPermissionOverride(member, null, EnumSet.of(Permission.VIEW_CHANNEL)).queue();
    }

    public void handleCreateTicket(ButtonInteractionEvent event, Member member, TicketType ticketType) {
        if (ticketType == TicketType.PLUGIN_GEN) {
            if (event.getMember().getRoles().stream()
                    .map(Role::getId)
                    .noneMatch(id -> id.equals(Config.PLUGIN_GEN_ACCESS_ROLE_ID))) {

                EmbedBuilder noAccess = new EmbedBuilder()
                        .setColor(new Color(0xE74C3C))
                        .setTitle("**Access Denied**")
                        .setDescription(
                                "**You need the Plugin Generation subscription to use this service.**\n" +
                                        "This is a premium feature. Please create a ticket to subscribe.")
                        .setFooter("・CSky Developments",
                                "https://cdn.discordapp.com/attachments/1112390125276631080/1112442565766168808/CSkyDevelopements.png");

                event.replyEmbeds(noAccess.build())
                        .setEphemeral(true)
                        .queue(success -> success.deleteOriginal().queueAfter(15, TimeUnit.SECONDS));
                return;
            }
            promptForm(event);
            return;
        }
        String ticketEmoji = switch (ticketType) {
            case NORMAL -> "🎫・";
            case ORDER -> "🛒・";
            case PLUGIN_GEN -> "✨️・";
            case REWARD -> "🎁・";
            case STAFF_APP -> "🎓・";
        };
        Category category = switch (ticketType) {
            case NORMAL -> guild.getCategoryById(Config.TICKET_NORMAL);
            case ORDER -> guild.getCategoryById(Config.TICKET_ORDER);
            case PLUGIN_GEN -> guild.getCategoryById(Config.TICKET_PLUGIN_GEN);
            case REWARD -> guild.getCategoryById(Config.TICKET_REWARD);
            case STAFF_APP -> guild.getCategoryById(Config.TICKET_STAFF_APP);
        };
        String ticketName = switch (ticketType) {
            case NORMAL -> "ticket";
            case ORDER -> "order";
            case PLUGIN_GEN -> "plugin generation";
            case REWARD -> "reward ticket";
            case STAFF_APP -> "staff application";
        };
        Logger.info("Creating a new `" + ticketName + "` for `" + member.getUser().getName() + "`...", true);
        guild.createTextChannel(ticketEmoji + getTicketID(ticketType), category)
                .addPermissionOverride(guild.getPublicRole(), null, EnumSet.of(Permission.VIEW_CHANNEL))
                .addPermissionOverride(member, EnumSet.of(Permission.VIEW_CHANNEL), null)
                .addPermissionOverride(guild.getRoleById(Config.STAFF_ROLE_ID), EnumSet.of(Permission.VIEW_CHANNEL),
                        null)
                .queue(channel -> {
                    EmbedBuilder replayEmbed = switch (ticketType) {
                        case NORMAL -> new EmbedBuilder()
                                .setColor(new Color(0x4482FF))
                                .setDescription("Your ticket has been successfully created in " + channel.getAsMention()
                                        + ". We appreciate your patience while we address your request.")
                                .setFooter("・CSky Developments",
                                        "https://cdn.discordapp.com/attachments/1112390125276631080/1112442565766168808/CSkyDevelopements.png");
                        case ORDER -> new EmbedBuilder()
                                .setColor(new Color(0x4482FF))
                                .setDescription("Your order has been successfully placed in " + channel.getAsMention()
                                        + ". We appreciate your patience while our team reviews your request.")
                                .setFooter("・CSky Developments",
                                        "https://cdn.discordapp.com/attachments/1112390125276631080/1112442565766168808/CSkyDevelopements.png");
                        case PLUGIN_GEN -> new EmbedBuilder()
                                .setColor(new Color(0x4482FF))
                                .setDescription("Your plugin generation request has been successfully created in "
                                        + channel.getAsMention() + ". Please wait while we process your generation.")
                                .setFooter("・CSky Developments",
                                        "https://cdn.discordapp.com/attachments/1112390125276631080/1112442565766168808/CSkyDevelopements.png");
                        case REWARD -> new EmbedBuilder()
                                .setColor(new Color(0x4482FF))
                                .setDescription("Your reward claim ticket has been successfully created in "
                                        + channel.getAsMention()
                                        + ". Please wait for our team to process your request.")
                                .setFooter("・CSky Developments",
                                        "https://cdn.discordapp.com/attachments/1112390125276631080/1112442565766168808/CSkyDevelopements.png");
                        case STAFF_APP -> new EmbedBuilder()
                                .setColor(new Color(0x4482FF))
                                .setDescription("Your application has been successfully created in "
                                        + channel.getAsMention()
                                        + ". We sincerely appreciate your interest in pursuing a position at CSky Developments.")
                                .setFooter("・CSky Developments",
                                        "https://cdn.discordapp.com/attachments/1112390125276631080/1112442565766168808/CSkyDevelopements.png");
                    };

                    Logger.info("Successfully created a new `" + ticketName + "`: `" + channel.getName() + "`", true);
                    event.replyEmbeds(replayEmbed.build()).setEphemeral(true)
                            .queue(success -> success.deleteOriginal().queueAfter(10, TimeUnit.SECONDS));

                    EmbedBuilder replayCreateEmbed = switch (ticketType) {
                        case NORMAL -> TicketEmbeds.ticketCreateEmbed;
                        case ORDER -> TicketEmbeds.orderCreateEmbed;
                        case PLUGIN_GEN -> TicketEmbeds.pluginGenEmbed;
                        case REWARD -> TicketEmbeds.rewardCreateEmbed;
                        case STAFF_APP -> TicketEmbeds.staffAppCreateEmbed;
                    };

                    ActionRow replayActionRow = switch (ticketType) {
                        case NORMAL -> TicketButtons.ticketCloseRow;
                        case ORDER -> TicketButtons.orderCloseRow;
                        case PLUGIN_GEN -> TicketButtons.pluginCancelRow;
                        case REWARD -> TicketButtons.rewardCloseRow;
                        case STAFF_APP -> {
                            String buttonId = event.getButton().getId();
                            if ("Developer_Button".equalsIgnoreCase(buttonId)) {
                                yield TicketButtons.developerCloseRow;
                            } else if ("Moderator_Button".equalsIgnoreCase(buttonId)) {
                                yield TicketButtons.moderatorCloseRow;
                            } else if ("Supporter_Button".equalsIgnoreCase(buttonId)) {
                                yield TicketButtons.supporterCloseRow;
                            } else {
                                yield TicketButtons.developerCloseRow;
                            }
                        }
                    };

                    channel.sendMessageEmbeds(replayCreateEmbed.build())
                            .addComponents(replayActionRow)
                            .queue();
                    if (ticketType.equals(TicketType.STAFF_APP)) {
                        if (event.getButton().getId().equalsIgnoreCase("Developer_Button")) {
                            channel.sendMessageEmbeds(TicketEmbeds.developerQuestionsEmbed.build()).queue();
                        }
                        if (event.getButton().getId().equalsIgnoreCase("Moderator_Button")) {
                            channel.sendMessageEmbeds(TicketEmbeds.moderatorQuestionsEmbed.build()).queue();
                        }
                        if (event.getButton().getId().equalsIgnoreCase("Supporter_Button")) {
                            channel.sendMessageEmbeds(TicketEmbeds.supporterQuestionsEmbed.build()).queue();
                        }
                    }
                }, error -> {
                    Logger.error("An error occurred while creating a `" + ticketName + "` for `"
                            + member.getUser().getName() + "`: " + error.getMessage(), false);
                });
    }

    private record PluginGenData(String apiKey, Project project) {
    }

    private void promptForm(ButtonInteractionEvent event) {
        TextInput apiKey = TextInput.create("api_key", "Gemini API Key", TextInputStyle.SHORT)
                .setPlaceholder("Your Gemini API Key")
                .setRequired(true)
                .build();

        TextInput name = TextInput.create("plugin_name", "Plugin Name", TextInputStyle.SHORT)
                .setPlaceholder("Name")
                .setRequired(true)
                .build();

        TextInput version = TextInput.create("plugin_version", "Minecraft Version", TextInputStyle.SHORT)
                .setPlaceholder("Plugin Version (e.g. 1.21.4)")
                .setRequired(true)
                .build();

        TextInput description = TextInput.create("plugin_description", "Description", TextInputStyle.PARAGRAPH)
                .setPlaceholder("Describe your plugin features...")
                .setRequired(true)
                .build();

        Modal modal = Modal.create("plugin_gen_modal", "Generate Plugin")
                .addActionRow(apiKey)
                .addActionRow(name)
                .addActionRow(version)
                .addActionRow(description)
                .build();
        event.replyModal(modal).queue();
    }

    @Override
    public void onModalInteraction(ModalInteractionEvent event) {
        if (!event.getModalId().equals("plugin_gen_modal"))
            return;

        String apiKey = event.getValue("api_key").getAsString();
        String name = event.getValue("plugin_name").getAsString();
        String version = event.getValue("plugin_version").getAsString();
        String description = event.getValue("plugin_description").getAsString();

        Member member = event.getMember();

        Project project = new Project(name, version, description);
        PluginGenData data = new PluginGenData(apiKey, project);
        EmbedBuilder responseEmbed = new EmbedBuilder()
                .setTitle("Plugin Generation")
                .setColor(new Color(0x4482FF))
                .setDescription("Creating your Work Space, Please wait while we process your generation.\n")
                .setFooter("・CSky Developments",
                        "https://cdn.discordapp.com/attachments/1112390125276631080/1112442565766168808/CSkyDevelopements.png");
        event.replyEmbeds(responseEmbed.build())
                .queue(success -> success.deleteOriginal().queueAfter(15, TimeUnit.SECONDS));
        Logger.info("Plugin generation requested by `" + member.getUser().getName() + "` for plugin: `" + name
                + "` Creating workspace for it...", true);
        createWorkSpace(member, data);
    }

    private void createWorkSpace(Member member, PluginGenData data) {
        String ticketID = getTicketID(TicketType.PLUGIN_GEN);
        Category category = guild.getCategoryById(Config.TICKET_PLUGIN_GEN);

        guild.createTextChannel("✨️・" + ticketID, category)
                .addPermissionOverride(guild.getPublicRole(), null, EnumSet.of(Permission.VIEW_CHANNEL))
                .addPermissionOverride(member, EnumSet.of(Permission.VIEW_CHANNEL), null)
                .addPermissionOverride(guild.getRoleById(Config.STAFF_ROLE_ID), EnumSet.of(Permission.VIEW_CHANNEL),
                        null)
                .queue(channel -> {
                    EmbedBuilder responseEmbed = new EmbedBuilder()
                            .setTitle("Plugin・Generation")
                            .setColor(new Color(0x4482FF))
                            .setDescription("Your plugin generation Work Space has been successfully created in "
                                    + channel.getAsMention() + ". \nPlease wait while we process your generation.\n")
                            .setFooter("・CSky Developments",
                                    "https://cdn.discordapp.com/attachments/1112390125276631080/1112442565766168808/CSkyDevelopements.png");

                    member.getUser().openPrivateChannel()
                            .queue(dm -> dm.sendMessageEmbeds(responseEmbed.build()).queue());
                    Logger.info("Successfully created a new `WorkSpace`:" + channel.getName() + "`", true);

                    Project project = data.project;
                    EmbedBuilder genEmbed = new EmbedBuilder()
                            .setColor(new Color(0xE67E22))
                            .setTitle("Plugin・Generation")
                            .setDescription(
                                    """
                                            We're generating your plugin using CSky Development's advance AI build tool.
                                            > For safety and compatibility, we recommend testing generated builds on a **non-production server** before using them live.
                                            """)
                            .addField(
                                    "Project Info:",
                                    "Name: " + project.getName() +
                                            "\nVersion: `" + project.getVersion() +
                                            "`\nDescription: `" + truncate(project.getDescription(), 200) +
                                            "`\nStatus: `Initializing...`",
                                    false)
                            .addField("Console:", "```\nInitializing...\n```", false)
                            .setFooter("CSky Developments • Requested by " + member.getUser().getName(),
                                    "https://cdn.discordapp.com/attachments/1112390125276631080/1112442565766168808/CSkyDevelopements.png")
                            .setTimestamp(Instant.now());

                    channel.sendMessageEmbeds(genEmbed.build())
                            .addComponents(TicketButtons.pluginCancelRow)
                            .queue(message -> {
                                CompletableFuture.runAsync(() -> {
                                    generate(genEmbed, message, channel, data);
                                });
                            });
                });
    }

    private void generate(EmbedBuilder genEmbed, Message message, TextChannel channel, PluginGenData data) {
        GeminiService gemini = new GeminiService(data.apiKey);
        Project project = data.project;
        Builder builder = new Builder(gemini);

        TextChannel logChannel = guild.getTextChannelById(Config.LOG_CHANNEL_ID);

        LinkedList<String> logBuffer = new LinkedList<>();
        LinkedList<String> fullLogBuffer = new LinkedList<>();

        AtomicReference<String> currentPhase = new AtomicReference<>("Initializing");
        AtomicReference<String> currentActivity = new AtomicReference<>("Starting system...");
        AtomicInteger currentBatch = new AtomicInteger(0);
        AtomicInteger totalBatches = new AtomicInteger(0);
        AtomicInteger filesProcessed = new AtomicInteger(0);
        AtomicInteger totalFiles = new AtomicInteger(0);
        AtomicInteger phaseNum = new AtomicInteger(0);

        builder.build(project, log -> {
            logBuffer.add(log);
            fullLogBuffer.add(log);
            if (logBuffer.size() > 10) {
                logBuffer.removeFirst();
            }

            if (log.contains("Processing Batch")) {
                Matcher m = Pattern.compile("Batch (\\d+)/(\\d+)").matcher(log);
                if (m.find()) {
                    currentBatch.set(Integer.parseInt(m.group(1)));
                    totalBatches.set(Integer.parseInt(m.group(2)));
                }
            }

            if (log.contains("Orchestrating")) {
                Matcher m = Pattern.compile("Orchestrating (\\d+) modules").matcher(log);
                if (m.find()) {
                    totalFiles.set(Integer.parseInt(m.group(1)));
                }
            }

            if (log.contains("[B] +")) {
                filesProcessed.incrementAndGet();
                String pathPart = log.replaceAll("\\[.*?\\]", "").replace("+", "").trim();
                String fileName = pathPart.contains("/") ? pathPart.substring(pathPart.lastIndexOf("/") + 1) : pathPart;
                fileName = fileName.split("\\s+")[0];
                currentActivity.set("Generated: " + fileName);
            }

            if (log.contains("[PHASE")) {
                Matcher m = Pattern.compile("\\[PHASE (\\d+)\\] (.*)").matcher(log);
                if (m.find()) {
                    phaseNum.set(Integer.parseInt(m.group(1)));
                    currentPhase.set(m.group(2).trim());
                }
            }

            if (log.contains("Compilation attempt")) {
                currentActivity.set("Compiling source code...");
            } else if (log.contains("AI-assisted fix attempt")) {
                currentActivity.set("Fixing compilation errors...");
            } else if (log.contains("Generating documentation")) {
                currentActivity.set("Writing README.md...");
            }

            double percent = 0;
            if (phaseNum.get() == 1)
                percent = 10;
            else if (phaseNum.get() == 2) {
                double batchBase = 15;
                double batchWeight = 65;
                if (totalBatches.get() > 0) {
                    percent = batchBase + ((double) (currentBatch.get() - 1) / totalBatches.get() * batchWeight);
                } else {
                    percent = 20;
                }
            } else if (phaseNum.get() == 3)
                percent = 85;
            else if (phaseNum.get() == 4)
                percent = 90;

            if (log.contains("successfully"))
                percent = 100;

            String progressBar = getProgressBar((int) percent);

            StringBuilder logsDisplay = new StringBuilder();
            for (String l : logBuffer) {
                logsDisplay.append(l.length() > 80 ? l.substring(0, 77) + "..." : l).append("\n");
            }

            genEmbed.setColor(new Color(0x4482FF));
            genEmbed.clearFields();

            genEmbed.addField("Project Info",
                    "**Name:** " + project.getName() +
                            "\n**Version:** `" + project.getVersion() + "`" +
                            "\n**Phase:** `" + currentPhase.get() + "`",
                    true);

            genEmbed.addField("Forge Progress",
                    "**Status:** " + (int) percent + "%\n" +
                            progressBar + "\n" +
                            "**Activity:** `" + currentActivity.get() + "`",
                    false);

            genEmbed.addField("Console Output", "```ml\n" + logsDisplay + "```", false);

            message.editMessageEmbeds(genEmbed.build()).queue();
        });

        File releaseDir = project.getPath().resolve("releases").toFile();
        File[] jarFiles = releaseDir.listFiles((dir, filename) -> filename.endsWith(".jar"));
        File readmeFile = project.getPath().resolve("sourcecode").resolve(project.getName()).resolve("README.md")
                .toFile();

        File buildLogFile = new File("build.log");
        try (PrintWriter writer = new PrintWriter(buildLogFile)) {
            for (String l : fullLogBuffer) {
                writer.println(l);
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }

        if (jarFiles != null && jarFiles.length > 0) {
            File jarFile = jarFiles[0];
            String readme = "No documentation provided.";

            if (readmeFile.exists()) {
                try {
                    readme = cleanMarkdown(Files.readString(readmeFile.toPath()));
                    if (readme.length() > 1000)
                        readme = readme.substring(0, 1000) + "...";
                } catch (Exception ex) {
                    readme = "README details currently unavailable.";
                }
            }
            genEmbed
                    .setColor(new Color(0x2ECC71))
                    .setDescription(
                            """
                                        Your plugin has been successfully generated!
                                        > **Reminder:** Please test generated builds on a **non-production server** before deploying them live.
                                        > **Security Note:** This ticket will be **automatically deleted in 6 hours**.
                                    """)
                    .clearFields()
                    .addField("Project Info",
                            "**Name:** " + project.getName() +
                                    "\n**Version:** `" + project.getVersion() + "`",
                            true)
                    .addField("Forge Status",
                            "**Status:** `✔ COMPLETED`" +
                                    "\n**Artifact:** `" + jarFile.getName() + "`",
                            true)
                    .addField("Documentation",
                            "```ml\n" + (readme.length() > 500 ? readme.substring(0, 497) + "..." : readme) + "\n```",
                            false)
                    .setTimestamp(Instant.now());

            message.editMessageEmbeds(genEmbed.build()).setComponents().queue();
            channel.sendFiles(FileUpload.fromData(jarFile, jarFile.getName())).queue();
            if (logChannel != null) {
                Logger.info("Artifact Forge Completed for **" + project.getName() + "**", true);
                logChannel.sendFiles(FileUpload.fromData(buildLogFile, "build.log")).queue();
                logChannel.sendFiles(FileUpload.fromData(readmeFile, "README.md")).queue();
                logChannel.sendFiles(FileUpload.fromData(jarFile, jarFile.getName())).queue();
            }
            channel.delete().queueAfter(6, TimeUnit.HOURS);
        } else {
            genEmbed.setTitle("Generation Failed")
                    .setColor(new Color(0xE74C3C))
                    .setDescription(
                            """
                                            The build process was unable to complete and no JAR file was generated.
                                            This may occur due to configuration issues or invalid source output. Please try generating again.
                                    """)
                    .clearFields()
                    .addField("Project Info",
                            "**Name:** " + project.getName() +
                                    "\n**Version:** `" + project.getVersion() + "`",
                            true)
                    .addField("Forge Status",
                            "**Status:** `❌ FAILED`" +
                                    "\n**Error:** `Critical systems failure during synthesis`",
                            true)
                    .setTimestamp(Instant.now());
            message.editMessageEmbeds(genEmbed.build()).queue();
            Logger.info("Generation failed for " + project.getName() + "** — No JAR produced.", true);
        }
    }

    private static String getProgressBar(int percent) {
        int length = 12;
        int filled = (int) (length * (percent / 100.0));
        StringBuilder sb = new StringBuilder();
        sb.append("`[");
        for (int i = 0; i < length; i++) {
            if (i < filled)
                sb.append("█");
            else
                sb.append("░");
        }
        sb.append("]`");
        return sb.toString();
    }

    private String truncate(String text, int max) {
        return (text.length() > max) ? text.substring(0, max) + "..." : text;
    }

    private String cleanMarkdown(String text) {
        if (text == null)
            return "";
        return text.replaceAll("[#*_`~>\\-]", "").replaceAll("\\[.*?\\]\\(.*?\\)", "").trim();
    }

    private void handleCloseConfirm(ButtonInteractionEvent event, Member member, TextChannel channel,
            TicketType ticketType) {
        channel.getManager()
                .putPermissionOverride(guild.getPublicRole(), null, EnumSet.of(Permission.VIEW_CHANNEL))
                .putPermissionOverride(member, null, EnumSet.of(Permission.VIEW_CHANNEL))
                .putPermissionOverride(guild.getRoleById(Config.STAFF_ROLE_ID), EnumSet.of(Permission.VIEW_CHANNEL),
                        null)
                .queue();

        EmbedBuilder replayEmbed = switch (ticketType) {
            case NORMAL -> new EmbedBuilder()
                    .setColor(new Color(0x4482FF))
                    .setDescription("The ticket has been closed by " + event.getMember().getAsMention()
                            + "! Please click on the **Delete** button below to delete the ticket permanently.")
                    .setFooter("・CSky Developments",
                            "https://cdn.discordapp.com/attachments/1112390125276631080/1112442565766168808/CSkyDevelopements.png");
            case ORDER -> new EmbedBuilder()
                    .setColor(new Color(0x4482FF))
                    .setDescription("The order has been canceled by " + event.getMember().getAsMention()
                            + "! Please click on the **Delete** button below to remove the order permanently.")
                    .setFooter("・CSky Developments",
                            "https://cdn.discordapp.com/attachments/1112390125276631080/1112442565766168808/CSkyDevelopements.png");
            case PLUGIN_GEN -> new EmbedBuilder()
                    .setColor(new Color(0x4482FF))
                    .setDescription(
                            "The plugin generation ticket has been canceled by " + event.getMember().getAsMention()
                                    + "! Click the **Delete** button below to delete the generation permanently.")
                    .setFooter("・CSky Developments",
                            "https://cdn.discordapp.com/attachments/1112390125276631080/1112442565766168808/CSkyDevelopements.png");

            case REWARD -> new EmbedBuilder()
                    .setColor(new Color(0x4482FF))
                    .setDescription("The reward claim ticket has been closed by " + event.getMember().getAsMention()
                            + "! Click on the **Delete** button below to delete the ticket permanently.")
                    .setFooter("・CSky Developments",
                            "https://cdn.discordapp.com/attachments/1112390125276631080/1112442565766168808/CSkyDevelopements.png");
            case STAFF_APP -> new EmbedBuilder()
                    .setColor(new Color(0x4482FF))
                    .setDescription("The application has been closed by " + event.getMember().getAsMention()
                            + "! Please click on the **Delete** button below to delete the application permanently.")
                    .setFooter("・CSky Developments",
                            "https://cdn.discordapp.com/attachments/1112390125276631080/1112442565766168808/CSkyDevelopements.png");
        };
        ActionRow replayActionRow = switch (ticketType) {
            case NORMAL -> TicketButtons.ticketDeleteRow;
            case ORDER -> TicketButtons.orderDeleteRow;
            case PLUGIN_GEN -> TicketButtons.pluginDeleteRow;
            case REWARD -> TicketButtons.rewardDeleteRow;
            case STAFF_APP -> TicketButtons.appDeleteRow;
        };

        event.replyEmbeds(replayEmbed.build())
                .addComponents(replayActionRow)
                .setEphemeral(false)
                .queue();
    }

    public void handleDeleteTicket(ButtonInteractionEvent event, Member member, TextChannel channel,
            TicketType ticketType) {
        if (member.getRoles().stream().noneMatch(role -> role.getId().equals(Config.STAFF_ROLE_ID))) {
            EmbedBuilder noPermissions = new EmbedBuilder()
                    .setColor(new Color(0x0090FF))
                    .setTitle("**NO PERMISSIONS**")
                    .setDescription("**You must be a staff member to do that.**")
                    .setFooter("・CSky Developments",
                            "https://cdn.discordapp.com/attachments/1112390125276631080/1112442565766168808/CSkyDevelopements.png");

            event.replyEmbeds(noPermissions.build())
                    .setEphemeral(true)
                    .queue(success -> success.deleteOriginal().queueAfter(10, TimeUnit.SECONDS));
            return;
        }
        String channelTag = channel.getName();
        Logger.info("Deleting `" + channelTag + "`...", true);
        event.replyEmbeds(new EmbedBuilder().setColor(0x0090FF).setTitle("Deleting...").build()).setEphemeral(true)
                .queue(success -> success.deleteOriginal().queueAfter(5, TimeUnit.SECONDS));
        saveTicketMessages(ticketType, channel).thenRun(() -> {
            channel.delete().queue(
                    success -> Logger.info("Successfully deleted `" + channelTag + "`!", true),
                    error -> Logger.error("An error occurred while deleting the ticket: " + channel.getName() + ": "
                            + error.getMessage(), false));
        }).exceptionally(error -> {
            Logger.error("An error occurred while processing the ticket deletion: " + channel.getName() + ": "
                    + error.getMessage(), false);
            return null;
        });
    }

    private CompletableFuture<Void> saveTicketMessages(TicketType ticketType, TextChannel channel) {
        String ticketName = switch (ticketType) {
            case NORMAL -> "ticket";
            case ORDER -> "order";
            case PLUGIN_GEN -> "plugin generation";
            case REWARD -> "reward ticket";
            case STAFF_APP -> "staff application";
        };
        StringBuilder ticketData = new StringBuilder();
        ticketData.append("----------------------------------------\n");
        ticketData.append("Channel ID: ").append(channel.getId()).append("\n");
        ticketData.append("Ticket Type: ").append(ticketName).append("\n");
        ticketData.append("Channel Name: ").append(channel.getName()).append("\n");
        ticketData.append("Closed At: ").append(Instant.now().toString()).append("\n");
        ticketData.append("----------------------------------------\n\n");
        ticketData.append("Messages:\n");

        return channel.getIterableHistory().takeAsync(1000).thenCompose(messages -> {
            List<Message> orderedMessages = new ArrayList<>(messages);
            Collections.reverse(orderedMessages);

            orderedMessages.forEach(message -> {
                ticketData.append(message.getTimeCreated().toInstant()).append(" ");
                ticketData.append(message.getAuthor().getName()).append(": ");
                ticketData.append(message.getContentRaw()).append("\n");
            });

            String fileName = "data/tickets/" + ticketName + "_" + channel.getId() + "_" + System.currentTimeMillis()
                    + ".txt";
            File file = new File(fileName);

            file.getParentFile().mkdirs();

            try (FileWriter writer = new FileWriter(file)) {
                writer.write(ticketData.toString());
                Logger.info("Saved " + channel.getAsMention() + " messages to " + fileName, false);

                FileUpload fileUpload = FileUpload.fromData(file, file.getName());
                return guild.getTextChannelById(Config.LOG_CHANNEL_ID)
                        .sendFiles(fileUpload)
                        .submit()
                        .thenRun(() -> Logger.info("Successfully sent ticket log to log channel: " + fileName, false))
                        .exceptionally(error -> {
                            Logger.error("Failed to send ticket log to log channel: " + error.getMessage(), false);
                            return null;
                        });
            } catch (IOException ex) {
                Logger.error("Failed to save " + ticketName + " messages for `" + channel.getName() + "`: "
                        + ex.getMessage(), false);
                return CompletableFuture.completedFuture(null);
            }
        });
    }

    public synchronized String getTicketID(TicketType ticketType) {
        int id = switch (ticketType) {
            case NORMAL -> ticketData.getNormalTicketID();
            case ORDER -> ticketData.getOrderTicketID();
            case PLUGIN_GEN -> ticketData.getPluginGenTicketID();
            case REWARD -> ticketData.getRewardTicketID();
            case STAFF_APP -> ticketData.getStaffAppTicketID();
        };
        if (id == 9999) {
            id = 0;
        }
        switch (ticketType) {
            case NORMAL -> ticketData.setNormalTicketID(id + 1);
            case ORDER -> ticketData.setOrderTicketID(id + 1);
            case PLUGIN_GEN -> ticketData.setPluginGenTicketID(id + 1);
            case REWARD -> ticketData.setRewardTicketID(id + 1);
            case STAFF_APP -> ticketData.setStaffAppTicketID(id + 1);
        }
        ;
        saveTicketData();
        return String.format("%04d", id);
    }

    public static class TicketData {
        private int normalTicketID = 1;
        private int orderTicketID = 1;
        private int pluginGenTicketID = 1;
        private int rewardTicketID = 1;
        private int staffAppTicketID = 1;

        public TicketData() {
        }

        public int getNormalTicketID() {
            return normalTicketID;
        }

        public void setNormalTicketID(int normalTicketID) {
            this.normalTicketID = normalTicketID;
        }

        public int getOrderTicketID() {
            return orderTicketID;
        }

        public void setOrderTicketID(int orderTicketID) {
            this.orderTicketID = orderTicketID;
        }

        public int getPluginGenTicketID() {
            return pluginGenTicketID;
        }

        public void setPluginGenTicketID(int pluginGenTicketID) {
            this.pluginGenTicketID = pluginGenTicketID;
        }

        public int getRewardTicketID() {
            return rewardTicketID;
        }

        public void setRewardTicketID(int rewardTicketID) {
            this.rewardTicketID = rewardTicketID;
        }

        public int getStaffAppTicketID() {
            return staffAppTicketID;
        }

        public void setStaffAppTicketID(int staffAppTicketID) {
            this.staffAppTicketID = staffAppTicketID;
        }
    }

}