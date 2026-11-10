import os
import json
import discord
from typing import Optional, List
from bot.config import Config
from bot.logger import BotLogger

COUNTING_GOALS = [10, 50, 100, 200, 300, 400, 500, 1000, 1500, 2000, 2500, 5000, 7500, 10000]
DATA_FILE = os.path.join("data", "counting_data.json")

# Custom emoji IDs
OMARK_ID = 1120422566725701692
XMARK_ID = 1120422570773184685

class CountingGame:
    def __init__(self, data_file: str = DATA_FILE):
        self.data_file = data_file
        self.current_count: int = 1
        self.last_counter_id: Optional[str] = None
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.data_file):
            self.current_count = 1
            self.last_counter_id = None
            self.save_data()
            return

        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.current_count = data.get("currentCount", 1)
            self.last_counter_id = data.get("lastCounterID")
        except Exception as ex:
            BotLogger.error(f"An error occurred while loading counting data. Error: {ex}", False)
            self.current_count = 1
            self.last_counter_id = None

    def save_data(self):
        try:
            parent = os.path.dirname(self.data_file)
            if parent:
                os.makedirs(parent, exist_ok=True)
            temp_file = f"{self.data_file}.tmp"
            data = {
                "currentCount": self.current_count,
                "lastCounterID": self.last_counter_id
            }
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            os.replace(temp_file, self.data_file)
        except Exception as ex:
            BotLogger.info(f"An error occurred while saving counting data. Error: {ex}", False)

    def reset_count(self):
        self.current_count = 1
        self.last_counter_id = None
        self.save_data()

    def get_goal_message(self, number: int, user: discord.User | discord.Member) -> str:
        mention = user.mention
        if number == 10:
            return f"🎉 **Hooray!** {mention} helped us reach the goal of {number}! Keep up the good work!"
        elif number == 50:
            return f"🎊 **Amazing!** {mention} contributed to the goal of {number}! Let's keep counting!"
        elif number == 100:
            return f"🎈 **Congratulations,** {mention}! We've hit the big {number}! Keep the count going!"
        elif number == 200:
            return f"🥳 **Woohoo!** {mention} has helped us achieve the milestone of {number}! Great work!"
        elif number == 300:
            return f"🌟 **Incredible!** {mention} pushed us to the goal of {number}! Let's keep counting higher!"
        elif number == 400:
            return f"🔥 **Astonishing progress,** {mention}! We've reached {number}! Keep up the great work!"
        elif number == 500:
            return f"🚀 **Spectacular!** {mention} has helped us reach the grand {number} milestone! Keep counting!"
        elif number == 1000:
            return f"💀 **Unbelievable!** {mention} propelled us to the epic goal of {number}! Thank you!"
        elif number == 10000:
            return f"❓ **How did we get here?** {mention}? Don’t tell me you’re hacking... Nah... Man, a score of **{number}** is hard to believe."
        else:
            return f"💀 **Goal reached!** {mention} helped us reach {number}! Keep it up!"

    def get_goal_reactions(self, number: int) -> List[str]:
        if number == 10:
            return ["🎉"]
        elif number == 50:
            return ["🎊"]
        elif number == 100:
            return ["🎈"]
        elif number == 200:
            return ["🥳"]
        elif number == 300:
            return ["🌟"]
        elif number == 400:
            return ["🔥"]
        elif number == 500:
            return ["🚀"]
        elif number == 10000:
            return ["❓"]
        else:
            return ["💀"]

    async def _add_custom_or_fallback_emoji(self, message: discord.Message, name: str, emoji_id: int, fallback: str):
        try:
            custom_emoji = discord.utils.get(message.guild.emojis, id=emoji_id) if message.guild else None
            if custom_emoji:
                await message.add_reaction(custom_emoji)
            else:
                # Use partial emoji
                await message.add_reaction(discord.PartialEmoji(name=name, id=emoji_id))
        except Exception:
            try:
                await message.add_reaction(fallback)
            except Exception:
                pass

    async def handle_message(self, message: discord.Message):
        if message.channel.id != Config.COUNTING_CHANNEL_ID:
            return

        author = message.author
        if author.bot:
            return

        content = message.content.strip()
        try:
            number = int(content)
        except ValueError:
            return

        channel_name = getattr(message.channel, "name", str(message.channel.id))

        if number <= 0 or number != self.current_count:
            await message.reply(f"**Sike!** That's the wrong number. Number should be {self.current_count}.")
            BotLogger.info(f"Oops! Looks like `{author.name}` made a slip in the counting. The count was at `{self.current_count}` in `{channel_name}`.", True)
            await self._add_custom_or_fallback_emoji(message, "XMark", XMARK_ID, "❌")
            self.reset_count()
            return

        if str(author.id) == self.last_counter_id:
            await message.reply(f"**Uh-oh!** {author.mention}, you can't count twice in a row. The count has been reset.")
            BotLogger.info(f"`{author.name}` counted twice in a row. The current count was at `{self.current_count}` in `{channel_name}`.", True)
            await self._add_custom_or_fallback_emoji(message, "XMark", XMARK_ID, "❌")
            self.reset_count()
            return

        if self.current_count in COUNTING_GOALS:
            goal_msg = self.get_goal_message(self.current_count, author)
            for r in self.get_goal_reactions(self.current_count):
                try:
                    await message.add_reaction(r)
                except Exception:
                    pass
            BotLogger.info(f"`{author.name}` helped us reach the goal of `{self.current_count}` in `{channel_name}`.", True)
            await message.reply(goal_msg)
        else:
            await self._add_custom_or_fallback_emoji(message, "OMark", OMARK_ID, "✅")

        self.current_count += 1
        self.last_counter_id = str(author.id)
        self.save_data()
