import asyncio
from typing import Set
import discord
from bot.config import Config
from bot.ai.assistant import SupportAI

class AIListener:
    def __init__(self, ai: SupportAI):
        self.ai = ai
        self.muted_channel_ids: Set[int] = set()

    async def handle_message(self, message: discord.Message):
        if message.author.bot:
            return

        channel = message.channel
        parent_id = getattr(channel, "category_id", None)

        if parent_id and parent_id == Config.TICKET_NORMAL:
            channel_id = channel.id
            raw_content = message.content

            if "c!" in raw_content:
                if channel_id not in self.muted_channel_ids:
                    self.muted_channel_ids.add(channel_id)
                    await message.reply("> **AI muted!**")
                else:
                    self.muted_channel_ids.remove(channel_id)
                    await message.reply("> **AI unmuted!**")
                return

            if channel_id in self.muted_channel_ids:
                return

            try:
                async with channel.typing():
                    author_name = message.author.name
                    prompt = raw_content

                    response = await asyncio.to_thread(self.ai.get_response, author_name, prompt)
                    if response and response.strip():
                        await message.reply(response)
            except Exception:
                pass
