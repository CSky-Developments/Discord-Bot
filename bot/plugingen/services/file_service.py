import re
from pathlib import Path
from bot.plugingen.models import Project
from bot.logger import BotLogger

BLOCK_PATTERN = re.compile(r"```(?:\w+)?\s*\n([\s\S]*?)```")

class FileService:
    def save(self, project: Project, file_path: str, content: str):
        root = project.get_path() / "sourcecode" / project.get_name()
        target = root / file_path

        found_block = False
        if content:
            matches = BLOCK_PATTERN.findall(content)
            for code in matches:
                found_block = True
                try:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    if file_path.lower() == "readme.md":
                        target.write_text(content, encoding="utf-8")
                        return
                    target.write_text(code.strip(), encoding="utf-8")
                except Exception as e:
                    BotLogger.error(f"Failed to write {file_path}: {e}")

        if not found_block and content and content.strip():
            try:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content.strip(), encoding="utf-8")
            except Exception as e:
                BotLogger.error(f"Failed to write raw {file_path}: {e}")

    def save_markdown(self, project: Project, file_path: str, content: str):
        root = project.get_path() / "sourcecode" / project.get_name()
        target = root / file_path
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        except Exception as e:
            BotLogger.error(f"Failed to write {file_path}: {e}")
