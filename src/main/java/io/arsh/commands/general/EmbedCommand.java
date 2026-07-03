package io.arsh.commands.general;

import io.arsh.commands.Command;
import io.arsh.embeds.HelpEmbed;
import io.arsh.embeds.RewardEmbeds;
import io.arsh.embeds.ServiceEmbeds;
import io.arsh.ticket.TicketButtons;
import io.arsh.ticket.TicketEmbeds;
import io.arsh.utils.Config;
import net.dv8tion.jda.api.entities.Role;
import net.dv8tion.jda.api.events.interaction.command.SlashCommandInteractionEvent;
import net.dv8tion.jda.api.interactions.commands.OptionType;
import net.dv8tion.jda.api.interactions.commands.build.CommandData;
import net.dv8tion.jda.api.interactions.commands.build.Commands;
import net.dv8tion.jda.api.interactions.commands.build.OptionData;
import net.dv8tion.jda.api.EmbedBuilder;

import java.awt.Color;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.TimeUnit;

public class EmbedCommand extends Command {

    private static final String SERVICE_NOT_AVAILABLE = "Service Not Available";
    private static final String BUILDING = "Building";
    private static final String TEXTURE_PACK = "Texture Pack";
    private static final String SERVER_SETUP = "Server Setup";
    private static final String HOSTING_SERVICES = "Hosting Services";
    private static final String SERVER_OPTIMIZATION = "Server Optimization";
    private static final String PLUGIN_DEVELOPMENT = "Plugin Development";
    private static final String PLUGIN_GEN = "Plugin Generation";
    private static final String TICKET = "Ticket";
    private static final String ORDER = "Order";
    private static final String REWARD = "Reward";
    private static final String STAFF_APP = "Staff Application";

    private static final String INVITE = "Invite";
    private static final String BOOSTER = "Booster";

    private static final String HOSTING_DIRT_PLAN = "Dirt Plan";
    private static final String HOSTING_WOOD_PLAN = "Wood Plan";
    private static final String HOSTING_COAL_PLAN = "Coal Plan";
    private static final String HOSTING_STONE_PLAN = "Stone Plan";
    private static final String HOSTING_IRON_PLAN = "Iron Plan";
    private static final String HOSTING_GOLD_PLAN = "Gold Plan";
    private static final String HOSTING_DIAMOND_PLAN = "Diamond Plan";
    private static final String HOSTING_NETHERITE_PLAN = "Netherite Plan";
    private static final String HOSTING_PAYMENTS = "Payments";

    @Override
    public String getName() {
        return "embed";
    }

    @Override
    public CommandData getCommandData() {
        return Commands.slash("embed", "Use to send embeds.")
                .addOptions(
                        new OptionData(OptionType.STRING, "category", "Select a category", true)
                                .addChoice(SERVICE_NOT_AVAILABLE, SERVICE_NOT_AVAILABLE)
                                .addChoice(BUILDING, BUILDING)
                                .addChoice(TEXTURE_PACK, TEXTURE_PACK)
                                .addChoice(SERVER_SETUP, SERVER_SETUP)
                                .addChoice(HOSTING_SERVICES, HOSTING_SERVICES)
                                .addChoice(SERVER_OPTIMIZATION, SERVER_OPTIMIZATION)
                                .addChoice(PLUGIN_DEVELOPMENT, PLUGIN_DEVELOPMENT)
                                .addChoice(TICKET, TICKET)
                                .addChoice(ORDER, ORDER)
                                .addChoice(PLUGIN_GEN, PLUGIN_GEN)
                                .addChoice(REWARD, REWARD)
                                .addChoice(STAFF_APP, STAFF_APP),

        new OptionData(OptionType.STRING, "embed", "Select an embed within the category", false)
                                .addChoice(INVITE, INVITE)
                                .addChoice(BOOSTER, BOOSTER)
                                .addChoice(HOSTING_DIRT_PLAN, HOSTING_DIRT_PLAN)
                                .addChoice(HOSTING_WOOD_PLAN, HOSTING_WOOD_PLAN)
                                .addChoice(HOSTING_COAL_PLAN, HOSTING_COAL_PLAN)
                                .addChoice(HOSTING_STONE_PLAN, HOSTING_STONE_PLAN)
                                .addChoice(HOSTING_IRON_PLAN, HOSTING_IRON_PLAN)
                                .addChoice(HOSTING_GOLD_PLAN, HOSTING_GOLD_PLAN)
                                .addChoice(HOSTING_DIAMOND_PLAN, HOSTING_DIAMOND_PLAN)
                                .addChoice(HOSTING_NETHERITE_PLAN, HOSTING_NETHERITE_PLAN)
                                .addChoice(HOSTING_PAYMENTS, HOSTING_PAYMENTS),
                        new OptionData(OptionType.BOOLEAN, "send_all", "Send all embeds from the category", false)
                );
    }

    @Override
    public void execute(SlashCommandInteractionEvent event) {
        if (event.getMember().getRoles().stream().map(Role::getId).noneMatch(id -> id.equals(Config.STAFF_ROLE_ID))) {
            EmbedBuilder noPerms = new EmbedBuilder()
                    .setColor(new Color(0x0090FF))
                    .setTitle("**NO PERMISSIONS**")
                    .setDescription("**You must be a staff member to do that.**")
                    .setFooter("・CSky Developments", "https://cdn.discordapp.com/attachments/1112390125276631080/1112442565766168808/CSkyDevelopements.png");

            event.replyEmbeds(noPerms.build()).setEphemeral(true)
                    .queue(msg -> msg.deleteOriginal().queueAfter(10, TimeUnit.SECONDS));
            return;
        }

        String category = event.getOption("category").getAsString();
        String embedType = event.getOption("embed") != null ? event.getOption("embed").getAsString() : null;
        boolean sendAll = event.getOption("send_all") != null && event.getOption("send_all").getAsBoolean();

        if (sendAll && embedType != null && !category.equals(REWARD)) {
            event.reply("❌ Cannot specify an embed and also use 'send_all' for this category. Please choose one.")
                    .setEphemeral(true).queue();
            return;
        }

        if (sendAll) {
            sendAllEmbeds(event, category, embedType);
            return;
        }

        switch (category) {
            case SERVICE_NOT_AVAILABLE -> {
                event.getChannel().asTextChannel().sendMessageEmbeds(HelpEmbed.notAvailableEmbed.build()).queue();
                sendConfirmation(event);
            }
            case TICKET -> {
                event.getChannel().asTextChannel().sendMessageEmbeds(TicketEmbeds.ticketEmbed.build()).addComponents(TicketButtons.ticketCreateRow).queue();
                sendConfirmation(event);
            }
            case PLUGIN_GEN -> {
                event.getChannel().asTextChannel().sendMessageEmbeds(TicketEmbeds.pluginGenEmbed.build()).addComponents(TicketButtons.pluginGenerateRow).queue();
                sendConfirmation(event);
            }
            case ORDER -> {
                                event.getChannel().asTextChannel().sendMessageEmbeds(TicketEmbeds.orderEmbed.build())
.addComponents(TicketButtons.orderCreateRow).queue();
                sendConfirmation(event);
            }
            case STAFF_APP -> {
                event.getChannel().asTextChannel().sendMessageEmbeds(TicketEmbeds.staffAppEmbed.build()).addComponents(TicketButtons.appCreateRow).queue();
                sendConfirmation(event);
            }
            case BUILDING -> sendEmbedWithOrder(event, ServiceEmbeds.building);
            case TEXTURE_PACK -> sendEmbedWithOrder(event, ServiceEmbeds.texturePack);
            case SERVER_SETUP -> sendEmbedWithOrder(event, ServiceEmbeds.serverSetup);
            case SERVER_OPTIMIZATION -> sendEmbedWithOrder(event, ServiceEmbeds.serverOptimization);
            case PLUGIN_DEVELOPMENT -> sendEmbedWithOrder(event, ServiceEmbeds.pluginDevelopment);

            case REWARD -> {
                if (embedType == null) {
                    event.reply("❌ Please select either `" + INVITE + "` or `" + BOOSTER + "` reward embed.")
                            .setEphemeral(true).queue();
                    return;
                }
                if (embedType.equalsIgnoreCase(INVITE)) {
                    event.getChannel().asTextChannel().sendMessageEmbeds(RewardEmbeds.inviteReward.build()).queue();
                    event.getChannel().asTextChannel().sendMessageEmbeds(TicketEmbeds.rewardEmbed.build()).addComponents(TicketButtons.rewardClaimRow).queue();
                } else if (embedType.equalsIgnoreCase(BOOSTER)) {
                    event.getChannel().asTextChannel().sendMessageEmbeds(RewardEmbeds.boosterReward.build()).queue();
                    event.getChannel().asTextChannel().sendMessageEmbeds(TicketEmbeds.rewardEmbed.build()).addComponents(TicketButtons.rewardClaimRow).queue();
                } else {
                    event.reply("❌ Invalid reward embed type.").setEphemeral(true).queue();
                    return;
                }
                sendConfirmation(event);
            }

            case HOSTING_SERVICES -> {
                if (embedType == null) {
                    event.reply("❌ Please specify a hosting embed to send.").setEphemeral(true).queue();
                    return;
                }

                EmbedBuilder embed = switch (embedType) {
                    case HOSTING_DIRT_PLAN -> ServiceEmbeds.dirtPlan;
                    case HOSTING_WOOD_PLAN -> ServiceEmbeds.woodPlan;
                    case HOSTING_COAL_PLAN -> ServiceEmbeds.coalPlan;
                    case HOSTING_STONE_PLAN -> ServiceEmbeds.stonePlan;
                    case HOSTING_IRON_PLAN -> ServiceEmbeds.ironPlan;
                    case HOSTING_GOLD_PLAN -> ServiceEmbeds.goldPlan;
                    case HOSTING_DIAMOND_PLAN -> ServiceEmbeds.diamondPlan;
                    case HOSTING_NETHERITE_PLAN -> ServiceEmbeds.netheritePlan;
                    case HOSTING_PAYMENTS -> ServiceEmbeds.locationsAndPayments;
                        default -> null;
                };

                if (embed == null) {
                    event.reply("❌ Invalid hosting embed.").setEphemeral(true).queue();
                    return;
                }
                if (embed == ServiceEmbeds.locationsAndPayments) {
                    event.getChannel().asTextChannel().sendMessageEmbeds(ServiceEmbeds.locationsAndPayments.build()).addComponents(ServiceEmbeds.serverOrderCreateRow).queue();
                } else {
                    event.getChannel().asTextChannel().sendMessageEmbeds(embed.build()).queue();
                }
                sendConfirmation(event);
            }

            default -> event.reply("❌ Unknown category.").setEphemeral(true).queue();
        }
    }

    private void sendEmbedWithOrder(SlashCommandInteractionEvent event, EmbedBuilder embed) {
        event.getChannel().asTextChannel().sendMessageEmbeds(embed.build()).queue();
                        event.getChannel().asTextChannel().sendMessageEmbeds(TicketEmbeds.orderEmbed.build())

                .addComponents(TicketButtons.orderCreateRow).queue();
        sendConfirmation(event);
    }

    private void sendConfirmation(SlashCommandInteractionEvent event) {
        event.reply("✅ Sent!").setEphemeral(true)
                .queue(msg -> msg.deleteOriginal().queueAfter(10, TimeUnit.SECONDS));
    }

    private void sendAllEmbeds(SlashCommandInteractionEvent event, String category, String embedType) {
        switch (category) {
            case SERVICE_NOT_AVAILABLE -> {
                event.getChannel().asTextChannel().sendMessageEmbeds(HelpEmbed.notAvailableEmbed.build()).queue();
                sendConfirmation(event);
            }
            case BUILDING -> {
                event.getChannel().asTextChannel().sendMessageEmbeds(ServiceEmbeds.building.build()).queue();
                                event.getChannel().asTextChannel().sendMessageEmbeds(ServiceEmbeds.serviceOrder.setColor(new Color(0xF35A46)).build())

                        .addComponents(TicketButtons.orderCreateRow).queue();
                sendConfirmation(event);
            }
            case TEXTURE_PACK -> {
                event.getChannel().asTextChannel().sendMessageEmbeds(ServiceEmbeds.texturePack.build()).queue();
                                event.getChannel().asTextChannel().sendMessageEmbeds(ServiceEmbeds.serviceOrder.setColor(new Color(0x6AAFB8)).build())

                        .addComponents(TicketButtons.orderCreateRow).queue();
                sendConfirmation(event);
            }
            case SERVER_SETUP -> {
                event.getChannel().asTextChannel().sendMessageEmbeds(ServiceEmbeds.serverSetup.build()).queue();
                                event.getChannel().asTextChannel().sendMessageEmbeds(ServiceEmbeds.serviceOrder.setColor(new Color(0x4DAEE1)).build())

                        .addComponents(TicketButtons.orderCreateRow).queue();
                sendConfirmation(event);
            }
            case SERVER_OPTIMIZATION -> {
                event.getChannel().asTextChannel().sendMessageEmbeds(ServiceEmbeds.serverOptimization.build()).queue();
                                event.getChannel().asTextChannel().sendMessageEmbeds(ServiceEmbeds.serviceOrder.setColor(new Color(0xE5B432)).build())

                        .addComponents(TicketButtons.orderCreateRow).queue();
                sendConfirmation(event);
            }
            case PLUGIN_DEVELOPMENT -> {
                event.getChannel().asTextChannel().sendMessageEmbeds(ServiceEmbeds.pluginDevelopment.build()).queue();
                event.getChannel().asTextChannel().sendMessageEmbeds(ServiceEmbeds.serviceOrder.setColor(new Color(0x938FF1)).build())
                        .addComponents(TicketButtons.orderCreateRow).queue();
                sendConfirmation(event);
            }
            case PLUGIN_GEN -> {
                event.getChannel().asTextChannel().sendMessageEmbeds(TicketEmbeds.pluginGenEmbed.build())
                        .addComponents(TicketButtons.pluginGenerateRow).queue();
                sendConfirmation(event);
            }
            case REWARD -> {
                if (embedType != null) {
                    if (embedType.equalsIgnoreCase(INVITE)) {
                        event.getChannel().asTextChannel().sendMessageEmbeds(RewardEmbeds.inviteReward.build()).queue();
                        sendConfirmation(event);
                    } else if (embedType.equalsIgnoreCase(BOOSTER)) {
                        event.getChannel().asTextChannel().sendMessageEmbeds(RewardEmbeds.boosterReward.build()).queue();
                        sendConfirmation(event);
                    } else {
                        event.reply("❌ Invalid reward embed type. Please select either `" + INVITE + "` or `" + BOOSTER + "`.")
                                .setEphemeral(true).queue();
                    }
                } else {
                    event.getChannel().asTextChannel().sendMessageEmbeds(RewardEmbeds.inviteReward.build()).queue();
                    event.getChannel().asTextChannel().sendMessageEmbeds(RewardEmbeds.boosterReward.build()).queue();
                    sendConfirmation(event);
                }
            }
            case HOSTING_SERVICES -> {
                List<EmbedBuilder> hostingEmbeds = Arrays.asList(
                        ServiceEmbeds.dirtPlan,
                        ServiceEmbeds.woodPlan,
                        ServiceEmbeds.coalPlan,
                        ServiceEmbeds.stonePlan,
                        ServiceEmbeds.ironPlan,
                        ServiceEmbeds.goldPlan,
                        ServiceEmbeds.diamondPlan,
                        ServiceEmbeds.netheritePlan
                );
                for (EmbedBuilder embed : hostingEmbeds) {
                    event.getChannel().asTextChannel().sendMessageEmbeds(embed.build()).queue();
                }
                event.getChannel().asTextChannel().sendMessageEmbeds(ServiceEmbeds.locationsAndPayments.build()).addComponents(ServiceEmbeds.serverOrderCreateRow).queue();
                sendConfirmation(event);
            }
            default -> event.reply("❌ Cannot send all embeds for unknown category.").setEphemeral(true).queue();
        }
    }
}