package io.arsh;

import io.arsh.ai.AI;
import io.arsh.ai.AIListener;
import io.arsh.commands.CommandManager;
import io.arsh.game.Counting;
import io.arsh.invite.InviteManager;
import io.arsh.invite.InviteTracker;
import io.arsh.message.MessageManager;
import io.arsh.ticket.TicketManager;
import io.arsh.utils.Config;
import io.arsh.utils.Logger;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.JDABuilder;
import net.dv8tion.jda.api.OnlineStatus;
import net.dv8tion.jda.api.entities.Activity;
import net.dv8tion.jda.api.entities.Guild;
import net.dv8tion.jda.api.requests.GatewayIntent;
import net.dv8tion.jda.api.utils.MemberCachePolicy;

public class Main {

    private static JDA bot;
    private static Guild guild;
    private static TicketManager ticketManager;
    private static InviteManager inviteManager;

    private static void buildBot() throws InterruptedException {
        Logger.info("Building the bot...", false);
        try {
            bot = JDABuilder.createDefault(Config.TOKEN)
                    .enableIntents(
                            GatewayIntent.GUILD_MEMBERS,
                            GatewayIntent.GUILD_INVITES,
                            GatewayIntent.GUILD_PRESENCES,
                            GatewayIntent.GUILD_MESSAGES,
                            GatewayIntent.MESSAGE_CONTENT
                    )
                    .setMemberCachePolicy(MemberCachePolicy.ALL)
                    .build();
        } catch (Exception ex){
            Logger.error(ex.getMessage(), false);
            Logger.error("Failed to build the bot. :(", false);
            Logger.warn("Disconnecting...", false);
            Logger.warn("Bot has crashed! Please check bot TOKEN in your configuration.", false);
            System.exit(1);
            return;
        }
        Logger.info("Connecting to bot and getting ready...", false);
        Logger.info("Setting up bot's presence...", false);
        Activity activity = Activity.watching("CSky Developments");
        OnlineStatus onlineStatus = OnlineStatus.DO_NOT_DISTURB;
        bot.getPresence().setPresence(onlineStatus, activity, true);
        Logger.info("Bot's presence has set!", false);
        bot.awaitReady();
        Logger.info("Bot is now ready!", false);
        Logger.info("Successfully build!", false);
    }

    private static void accessGuild() {
        Logger.info("Accessing CSky Developments Server...", false);
        guild = bot.getGuildById(Config.GUILD_ID);
        if (guild == null) {
            Logger.error("Failed to access CSky Developments Servers. :(", false);
            Logger.warn("Disconnecting...", false);
            Logger.warn("Bot has crashed! Please check the GUILD_ID in your configuration.", false);
            System.exit(1);
        }
        Logger.info("Successfully accessed CSky Developments Servers!", false);
    }

    private static void initializeTicketManager() {
        try {
            ticketManager = new TicketManager(guild);
            bot.addEventListener(ticketManager);
        } catch (Exception ex) {
            Logger.error(ex.getMessage(), false);
            Logger.error("Failed to initialize ticket manager. :(", false);
            Logger.warn("Disconnecting...", false);
            Logger.warn("Bot has crashed! Please check the code of ticket manager.", false);
            System.exit(1);
        }
    }

    private static void initializeInviteTracker() {
        try {
            inviteManager = new InviteManager(guild);
            bot.addEventListener(new InviteTracker(guild, inviteManager));
        } catch (Exception ex) {
            Logger.error(ex.getMessage(), false);
            Logger.error("Failed to initialize invite tracker. :(", false);
            Logger.warn("Disconnecting...", false);
            Logger.warn("Bot has crashed! Please check the code of invite tracker.", false);
            System.exit(1);
        }
    }

    private static void initializeMessageManager() {
        Logger.info("Initializing message manager...", false);
        try {
            bot.addEventListener(new MessageManager());
        } catch (Exception ex) {
            Logger.error(ex.getMessage(), false);
            Logger.error("Failed to initialize message manager. :(", false);
            Logger.warn("Disconnecting...", false);
            Logger.warn("Bot has crashed! Please check the code of message manager.", false);
            System.exit(1);
        }
        Logger.info("Successfully initialized message manager!", false);
    }

    private static void registerCommands() {
        Logger.info("Registering commands...", false);
        try {
            bot.addEventListener(new CommandManager(guild, ticketManager, inviteManager));
        } catch (Exception ex) {
            Logger.error(ex.getMessage(), false);
            Logger.error("Failed register command. :(", false);
            Logger.warn("Disconnecting...", false);
            Logger.warn("Bot has crashed! Please check the code for commands.", false);
            System.exit(1);
        }
        Logger.info("Successfully registered all commands!", false);
    }

    private static void loadCountingGame() {
        try {
            bot.addEventListener(new Counting());
        } catch (Exception ex) {
            Logger.error(ex.getMessage(), false);
            Logger.error("Failed to load counting minigames. :(", false);
            Logger.warn("Disconnecting...", false);
            Logger.warn("Bot has crashed! Please check the code of counting minigames game.", false);
            System.exit(1);
        }
    }

    private static void initializeSupportAI() {
        AI ai = null;
        try {
            ai = new AI();
            bot.addEventListener(new AIListener(ai));
        } catch (Exception ex) {
            Logger.error(ex.getMessage(), false);
            Logger.error("Failed to initialize supporter AI. AI support will be unavailable. :(", false);
            bot.removeEventListener(new AIListener(ai));
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Logger.info("Starting...", false);
        Logger.info("Loading configuration...", false);
        Config.load();
        Logger.info("Successfully load the bot's configurations.", false);
        buildBot();
        accessGuild();
        initializeTicketManager();
        initializeInviteTracker();
        initializeMessageManager();
        registerCommands();
        loadCountingGame();
        initializeSupportAI();
        Logger.setLogChannel(guild.getTextChannelById(Config.LOG_CHANNEL_ID));
        Logger.info("CSky Development's bot is now online!", true);
    }

}