import os
import sys
from typing import List, Optional, Any, Dict
import yaml

class Config:
    TOKEN: str = ""
    GUILD_ID: int = 0
    LOG_CHANNEL_ID: int = 0
    MEMBER_COUNT_CHANNEL_ID: int = 0
    COUNTING_CHANNEL_ID: int = 0
    STAFF_ROLE_ID: int = 0
    MEMBER_ROLE_ID: int = 0

    TICKET_NORMAL: int = 0
    TICKET_ORDER: int = 0
    TICKET_PLUGIN_GEN: int = 0
    TICKET_REWARD: int = 0
    TICKET_STAFF_APP: int = 0
    AI_KEY: str = ""
    TICKET_CHANNEL_ID: int = 0
    SUPPORT_CATEGORY_ID: int = 0

    PLUGIN_GEN_ACCESS_ROLE_ID: int = 0

    @classmethod
    def load(cls, config_path: Optional[str] = None):
        data: Optional[Dict[str, Any]] = None

        search_paths = [
            config_path,
            "config.yml",
            "src/main/resources/config.yml",
            "/app/config.yml",
        ]

        for path in search_paths:
            if path and os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = yaml.safe_load(f) or {}
                    break
                except Exception:
                    pass

        cls.TOKEN = cls._get_str(data, "Token", "DISCORD_TOKEN")
        cls.GUILD_ID = cls._get_int(data, "Guild-ID", "GUILD_ID")
        cls.LOG_CHANNEL_ID = cls._get_int(data, "Log-Channel-ID", "LOG_CHANNEL_ID")
        cls.MEMBER_COUNT_CHANNEL_ID = cls._get_int(data, "Member-Count-Channel-ID", "MEMBER_COUNT_CHANNEL_ID")
        cls.COUNTING_CHANNEL_ID = cls._get_int(data, "Counting-Channel-ID", "COUNTING_CHANNEL_ID")
        cls.STAFF_ROLE_ID = cls._get_int(data, "Staff-Role-ID", "STAFF_ROLE_ID")
        cls.MEMBER_ROLE_ID = cls._get_int(data, "Member-Role-ID", "MEMBER_ROLE_ID")
        cls.AI_KEY = cls._get_str(data, "AI-Key", "AI_KEY", required=False) or ""
        cls.SUPPORT_CATEGORY_ID = cls._get_int(data, "Support-Category-ID", "SUPPORT_CATEGORY_ID", required=False)
        cls.TICKET_CHANNEL_ID = cls._get_int(data, "Ticket-Channel-ID", "TICKET_CHANNEL_ID", required=False)
        cls.TICKET_NORMAL = cls._get_int(data, "Ticket-Normal-Category", "TICKET_NORMAL_CATEGORY")
        cls.TICKET_ORDER = cls._get_int(data, "Ticket-Order-Category", "TICKET_ORDER_CATEGORY")
        cls.TICKET_PLUGIN_GEN = cls._get_int(data, "Ticket-Plugin-Generation-Category", "TICKET_PLUGIN_GEN_CATEGORY")
        cls.TICKET_REWARD = cls._get_int(data, "Ticket-Reward-Category", "TICKET_REWARD_CATEGORY")
        cls.TICKET_STAFF_APP = cls._get_int(data, "Ticket-Staff-App-Category", "TICKET_STAFF_APP_CATEGORY")
        cls.PLUGIN_GEN_ACCESS_ROLE_ID = cls._get_int(data, "Plugin-Gen-Access-Role-ID", "PLUGIN_GEN_ACCESS_ROLE_ID", required=False)

    @classmethod
    def _get_str(cls, data: Optional[Dict[str, Any]], yaml_key: str, env_key: str, required: bool = True) -> str:
        env_val = os.getenv(env_key)
        if env_val and env_val.strip():
            return env_val.strip()

        if data and yaml_key in data and data[yaml_key] is not None:
            return str(data[yaml_key]).strip()

        if required:
            print(f"[ERROR] Missing required config value. Please set ENV: '{env_key}' (or '{yaml_key}' in config.yml)", file=sys.stderr)
            sys.exit(1)
        return ""

    @classmethod
    def _get_int(cls, data: Optional[Dict[str, Any]], yaml_key: str, env_key: str, required: bool = True) -> int:
        val_str = cls._get_str(data, yaml_key, env_key, required=required)
        if not val_str:
            return 0
        try:
            return int(val_str)
        except ValueError:
            print(f"[ERROR] Config value for '{env_key}'/'{yaml_key}' must be an integer, got '{val_str}'", file=sys.stderr)
            if required:
                sys.exit(1)
            return 0

    @classmethod
    def _get_list(cls, data: Optional[Dict[str, Any]], yaml_key: str, env_key: str, required: bool = False) -> List[str]:
        env_val = os.getenv(env_key)
        if env_val and env_val.strip():
            return [x.strip() for x in env_val.split(",") if x.strip()]

        if data and yaml_key in data and data[yaml_key] is not None:
            val = data[yaml_key]
            if isinstance(val, list):
                return [str(x).strip() for x in val if x]
            elif isinstance(val, str):
                return [x.strip() for x in val.split(",") if x.strip()]

        if required:
            print(f"[ERROR] Missing required list value. Please set ENV: '{env_key}' (or '{yaml_key}' in config.yml)", file=sys.stderr)
            sys.exit(1)
        return []
