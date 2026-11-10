import os
import tempfile
from typing import Optional
from bot.license.models import LicenseType
from bot.license.crypto import AESEncrypter, KeyGenerator
from bot.logger import BotLogger

class LicenseGenerator:
    @staticmethod
    def get_license_file(license_type: LicenseType, ip: str, port: int, uuid: str) -> Optional[str]:
        try:
            data = license_type.license_data
            plain_license = KeyGenerator.generate_key(data.salt, ip, port, uuid)
            encrypted = AESEncrypter.encrypt(data.aes_key, data.aes_iv, plain_license)
            return LicenseGenerator.write_license_file(encrypted, uuid)
        except Exception as ex:
            BotLogger.error(f"Failed to generate license file: {ex}", True)
            return None

    @staticmethod
    def write_license_file(encrypted: str, uuid: Optional[str]) -> str:
        uuid_prefix = uuid[:8] if uuid else "key"
        prefix = f"license-{uuid_prefix}-"

        fd, temp_path = tempfile.mkstemp(prefix=prefix, suffix=".key", text=True)
        with os.fdopen(fd, "w", encoding="utf-8") as writer:
            writer.write("-----BEGIN LICENSE KEY-----\n")
            writer.write(encrypted + "\n")
            writer.write("-----END LICENSE KEY-----\n\n")

            writer.write("© 2025 CSky Developments\n\n")
            writer.write("All rights reserved.\n\n")
            writer.write("This Plugin License Agreement (\"Agreement\") is made between CSky Developments\n")
            writer.write("and the Licensee who purchases and uses the software. Unauthorized use,\n")
            writer.write("reproduction, or distribution is strictly prohibited and may result in legal action.\n\n")
            writer.write("CSky Developments retains full rights and intellectual property ownership.\n")

        return temp_path
