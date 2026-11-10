import sys
import signal
import asyncio
import discord
from discord import app_commands

from bot.config import Config
from bot.logger import BotLogger
from bot.game.counting import CountingGame
from bot.invite.manager import InviteManager
from bot.invite.tracker import InviteTracker
from bot.message.manager import MessageManager
from bot.ticket.manager import TicketManager
from bot.commands import (
    setup_ping_command,
    setup_invite_command,
    setup_ticket_command,
    setup_order_command,
    setup_plugin_command,
    setup_reward_command,
    setup_staffapp_command,
    setup_embed_command,
)

class CSkyBot(discord.Client):
    def __init__(self, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.guild_obj: discord.Guild | None = None
        self.ticket_manager: TicketManager | None = None
        self.invite_manager: InviteManager | None = None
        self.invite_tracker: InviteTracker | None = None
        self.message_manager: MessageManager | None = None
        self.counting_game: CountingGame | None = None

    async def setup_hook(self):
        # Configure global tree error handler
        @self.tree.error
        async def on_tree_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
            cmd_name = interaction.command.name if interaction.command else "unknown"
            BotLogger.error(f"Command execution error for /{cmd_name}: {error}", True)
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message("❌ An internal error occurred while executing this command.", ephemeral=True)
                else:
                    await interaction.followup.send("❌ An internal error occurred while executing this command.", ephemeral=True)
            except Exception:
                pass

    async def on_ready(self):
        BotLogger.info("Connecting to bot and getting ready...", False)
        BotLogger.info("Setting up bot's presence...", False)

        activity = discord.Activity(type=discord.ActivityType.watching, name="CSky Developments")
        await self.change_presence(status=discord.Status.dnd, activity=activity)
        BotLogger.info("Bot's presence has set!", False)
        BotLogger.info("Bot is now ready!", False)
        BotLogger.info("Successfully build!", False)

        BotLogger.info("Accessing CSky Developments Server...", False)
        self.guild_obj = self.get_guild(Config.GUILD_ID)
        if not self.guild_obj:
            BotLogger.error("Failed to access CSky Developments Servers. :(", False)
            BotLogger.warn("Disconnecting...", False)
            BotLogger.warn("Bot has crashed! Please check the GUILD_ID in your configuration.", False)
            await self.close()
            sys.exit(1)

        BotLogger.info("Successfully accessed CSky Developments Servers!", False)

        # Initialize Ticket Manager
        try:
            self.ticket_manager = TicketManager(self.guild_obj)
        except Exception as ex:
            BotLogger.error(f"Failed to initialize ticket manager. :( Error: {ex}", False)
            BotLogger.warn("Bot has crashed! Please check the code of ticket manager.", False)
            await self.close()
            sys.exit(1)

        # Initialize Invite Tracker
        try:
            self.invite_manager = InviteManager()
            self.invite_tracker = InviteTracker(self.guild_obj, self.invite_manager)
            await self.invite_tracker.initialize()
        except Exception as ex:
            BotLogger.error(f"Failed to initialize invite tracker. :( Error: {ex}", False)
            BotLogger.warn("Bot has crashed! Please check the code of invite tracker.", False)
            await self.close()
            sys.exit(1)

        # Initialize Message Manager
        BotLogger.info("Initializing message manager...", False)
        try:
            self.message_manager = MessageManager()
        except Exception as ex:
            BotLogger.error(f"Failed to initialize message manager. :( Error: {ex}", False)
            BotLogger.warn("Bot has crashed! Please check the code of message manager.", False)
            await self.close()
            sys.exit(1)
        BotLogger.info("Successfully initialized message manager!", False)

        # Load Counting Minigame
        try:
            self.counting_game = CountingGame()
        except Exception as ex:
            BotLogger.error(f"Failed to load counting minigames. :( Error: {ex}", False)
            BotLogger.warn("Bot has crashed! Please check the code of counting minigames game.", False)
            await self.close()
            sys.exit(1)

        # Register Commands
        BotLogger.info("Registering commands...", False)
        guild_target = discord.Object(id=Config.GUILD_ID)
        try:
            setup_ping_command(self.tree, guild_target)
            setup_embed_command(self.tree, guild_target)
            setup_invite_command(self.tree, guild_target, self.invite_manager)
            setup_ticket_command(self.tree, guild_target, self.ticket_manager)
            setup_order_command(self.tree, guild_target, self.ticket_manager)
            setup_plugin_command(self.tree, guild_target, self.ticket_manager)
            setup_reward_command(self.tree, guild_target, self.ticket_manager)
            setup_staffapp_command(self.tree, guild_target)

            synced = await self.tree.sync(guild=guild_target)
            BotLogger.info(f"Successfully registered {len(synced)} commands for guild {self.guild_obj.name}", False)
        except Exception as ex:
            BotLogger.error(f"Failed register command. :( Error: {ex}", False)
            BotLogger.warn("Bot has crashed! Please check the code for commands.", False)
            await self.close()
            sys.exit(1)
        BotLogger.info("Successfully registered all commands!", False)

        # Set up log channel
        log_channel = self.guild_obj.get_channel(Config.LOG_CHANNEL_ID)
        if isinstance(log_channel, discord.TextChannel):
            BotLogger.set_log_channel(log_channel, asyncio.get_running_loop())
        BotLogger.info("CSky Development's bot is now online!", True)

    async def on_message(self, message: discord.Message):
        if self.message_manager:
            self.message_manager.handle_message(message)
        if self.counting_game:
            await self.counting_game.handle_message(message)

    async def on_message_delete(self, message: discord.Message):
        if self.message_manager:
            self.message_manager.handle_message_delete(message, self.guild_obj)

    async def on_raw_message_delete(self, payload: discord.RawMessageDeleteEvent):
        # Fallback for un-cached raw message deletes
        if self.message_manager:
            self.message_manager.handle_message_delete(payload, self.guild_obj)

    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if self.message_manager:
            self.message_manager.handle_message_edit(before, after)

    async def on_member_join(self, member: discord.Member):
        if self.invite_tracker:
            await self.invite_tracker.on_member_join(member)

    async def on_member_remove(self, member: discord.Member):
        if self.invite_tracker:
            await self.invite_tracker.on_member_remove(member)

    async def on_interaction(self, interaction: discord.Interaction):
        # Component interactions (buttons)
        if interaction.type == discord.InteractionType.component and self.ticket_manager:
            await self.ticket_manager.handle_button_interaction(interaction)

def main():
    BotLogger.rotate_active_logs()
    BotLogger.info("Starting...", False)
    BotLogger.info("Loading configuration...", False)
    Config.load()
    BotLogger.info("Successfully load the bot's configurations.", False)

    intents = discord.Intents.default()
    intents.members = True
    intents.invites = True
    intents.presences = True
    intents.message_content = True
    intents.guild_messages = True

    bot = CSkyBot(intents=intents)

    # Signal handling
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    def handle_exit(*_):
        BotLogger.info("Shutting down bot...", False)
        asyncio.create_task(bot.close())

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            signal.signal(sig, handle_exit)
        except Exception:
            pass

    try:
        loop.run_until_complete(bot.start(Config.TOKEN))
    except KeyboardInterrupt:
        pass
    except Exception as ex:
        BotLogger.error(f"Failed to build the bot. :( Error: {ex}", False)
        BotLogger.warn("Disconnecting...", False)
        BotLogger.warn("Bot has crashed! Please check bot TOKEN in your configuration.", False)
        sys.exit(1)
    finally:
        loop.close()

if __name__ == "__main__":
    main()
