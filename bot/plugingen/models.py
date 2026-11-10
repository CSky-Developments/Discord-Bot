import os
import uuid
import tempfile
from pathlib import Path

class Project:
    def __init__(self, name: str, version: str, description: str):
        self.id = uuid.uuid4()
        self.name = name
        self.version = version
        self.description = description
        self.path = Path(tempfile.gettempdir()) / "plugins" / f"{name}-{self.id}"

    def get_id(self) -> uuid.UUID:
        return self.id

    def get_path(self) -> Path:
        return self.path

    def get_name(self) -> str:
        return self.name

    def get_version(self) -> str:
        return self.version

    def get_description(self) -> str:
        return self.description
