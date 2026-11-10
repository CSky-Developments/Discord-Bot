import os
import logging
import asyncio
from datetime import datetime
from typing import Optional
import discord

logger = logging.getLogger("discord-bot")
logger.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_format = logging.Formatter("[%(asctime)s] [%(levelname)-5s] [discord-bot] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
console_handler.setFormatter(console_format)
logger.addHandler(console_handler)

# File handler
log_dir = "/app/logs" if os.path.exists("/app") else "./logs"
try:
    os.makedirs(log_dir, exist_ok=True)
    file_handler = logging.FileHandler(os.path.join(log_dir, "service.log"), encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(console_format)
    logger.addHandler(file_handler)
except Exception:
    pass

class BotLogger:
    _log_channel: Optional[discord.TextChannel] = None
    _loop: Optional[asyncio.AbstractEventLoop] = None

    @classmethod
    def set_log_channel(cls, channel: Optional[discord.TextChannel], loop: Optional[asyncio.AbstractEventLoop] = None):
        cls._log_channel = channel
        cls._loop = loop or asyncio.get_event_loop()

    @classmethod
    def rotate_active_logs(cls):
        active_log = os.path.join(log_dir, "service.log")
        if os.path.exists(active_log) and os.path.getsize(active_log) > 0:
            try:
                mtime = os.path.getmtime(active_log)
                ts = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d_%H-%M-%S")
                new_path = os.path.join(log_dir, f"service-{ts}.log")
                os.rename(active_log, new_path)
            except Exception as e:
                logger.error(f"Failed to rotate log file: {e}")

    @classmethod
    def _clean_for_console(cls, msg: str) -> str:
        return msg.replace("`", "").replace("*", "")

    @classmethod
    def info(cls, message: str, send_to_discord: bool = False):
        logger.info(cls._clean_for_console(message))
        if send_to_discord:
            cls.send_to_discord(f"**INFO** {message}")

    @classmethod
    def warn(cls, message: str, send_to_discord: bool = False):
        logger.warning(message)
        if send_to_discord:
            cls.send_to_discord(f"**WARN** {message}")

    @classmethod
    def error(cls, message: str, send_to_discord: bool = False):
        logger.error(message)
        if send_to_discord:
            cls.send_to_discord(f"**ERROR** {message}")

    @classmethod
    def debug(cls, message: str):
        logger.debug(message)

    @classmethod
    def send_to_discord(cls, message: str):
        if cls._log_channel is not None:
            try:
                if cls._loop and cls._loop.is_running():
                    asyncio.run_coroutine_threadsafe(cls._log_channel.send(message), cls._loop)
                else:
                    asyncio.create_task(cls._log_channel.send(message))
            except Exception as e:
                logger.error(f"Failed to dispatch discord log: {e}")
