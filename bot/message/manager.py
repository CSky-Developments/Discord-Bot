import time
from collections import OrderedDict
from typing import Optional
import discord
from bot.config import Config
from bot.logger import BotLogger

CACHE_LIMIT = 10000

class MessageEntry:
    def __init__(self, content: str, author_id: str, timestamp: float):
        self.content = content
        self.author_id = author_id
        self.timestamp = timestamp

class MessageManager:
    def __init__(self, cache_limit: int = CACHE_LIMIT):
        self.cache_limit = cache_limit
        self.message_cache: OrderedDict[str, MessageEntry] = OrderedDict()

    def handle_message(self, message: discord.Message):
        if message.author.bot or message.channel.id == Config.LOG_CHANNEL_ID:
            return

        content = message.content
        if not content:
            return

        msg_id = str(message.id)
        author_id = str(message.author.id)

        self.message_cache[msg_id] = MessageEntry(content, author_id, time.time())
        if len(self.message_cache) > self.cache_limit:
            self.message_cache.popitem(last=False)

    def handle_message_delete(self, message: discord.Message | discord.RawMessageDeleteEvent, guild: Optional[discord.Guild] = None):
        msg_id = str(message.id if hasattr(message, "id") else message.message_id)
        cached_entry = self.message_cache.pop(msg_id, None)

        if not cached_entry:
            return

        content = cached_entry.content
        author_name = "Unknown Member"

        if guild:
            member = guild.get_member(int(cached_entry.author_id))
            if member:
                author_name = member.name

        channel_name = "unknown-channel"
        if hasattr(message, "channel") and message.channel:
            channel_name = getattr(message.channel, "name", str(message.channel.id))
        elif guild and hasattr(message, "channel_id"):
            ch = guild.get_channel(message.channel_id)
            if ch:
                channel_name = getattr(ch, "name", str(ch.id))

        log_message = f"Messages of `{author_name}` was deleted in `{channel_name}`: ```Content: {content}```"
        BotLogger.info(log_message, True)

    def handle_message_edit(self, before: Optional[discord.Message], after: discord.Message):
        if after.author.bot or after.channel.id == Config.LOG_CHANNEL_ID:
            return

        new_content = after.content
        if not new_content:
            return

        msg_id = str(after.id)
        cached_entry = self.message_cache.get(msg_id)

        if cached_entry and cached_entry.content and cached_entry.content != new_content:
            old_content = cached_entry.content
            author_mention = after.author.name
            channel_name = getattr(after.channel, "name", str(after.channel.id))

            log_message = (
                f"`{author_mention}` edited their message in `{channel_name}`: "
                f"```Original: {old_content}``` ```Edited: {new_content}```"
            )

            self.message_cache[msg_id] = MessageEntry(new_content, cached_entry.author_id, time.time())
            BotLogger.info(log_message, True)
