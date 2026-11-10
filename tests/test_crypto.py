import os
import hashlib
import base64
import pytest
from bot.license.models import LicenseType
from bot.license.crypto import AESEncrypter, KeyGenerator
from bot.license.generator import LicenseGenerator

def test_key_generator():
    salt = "iXkMYovoMcRZTUIO3YrDcmfjyzsNfFP7"
    ip = "127.0.0.1"
    port = 25565
    uuid = "12345678-1234-1234-1234-123456789abc"

    key = KeyGenerator.generate_key(salt, ip, port, uuid)
    expected_sha = hashlib.sha256(f"{ip}:{port}:{uuid}:{salt}".encode("utf-8")).digest()
    expected_key = base64.b64encode(expected_sha).decode("utf-8")

    assert key == expected_key
    assert key == "eNLc6dLrLUIhxIiZI7dVR5wVQN/6faWAq5g9qTqFcAI="

def test_aes_encryption():
    key = "OWCYiekqWNX4zLGh"
    iv = "a2mezIEWVRhdpXh5"
    data = "eNLc6dLrLUIhxIiZI7dVR5wVQN/6faWAq5g9qTqFcAI="

    encrypted = AESEncrypter.encrypt(key, iv, data)
    assert encrypted == "dWpuRJd25c1N9udCI+EWjJbKDH/zPU+b5+VEwCB4dC0ow64XWdk5j7GniGiGH8y0"

def test_all_license_types():
    expected_licenses = ["LoreSMP", "DeckCardSMP", "RisingSMP", "ScoreSMP", "DarkSideSMP"]
    for name in expected_licenses:
        assert hasattr(LicenseType, name)
        lt = LicenseType[name]
        data = lt.license_data
        assert len(data.salt) == 32
        assert len(data.aes_key) == 16
        assert len(data.aes_iv) == 16

def test_license_file_generation():
    file_path = LicenseGenerator.get_license_file(
        LicenseType.LoreSMP,
        "1.2.3.4",
        25565,
        "test-uuid-1234"
    )
    assert file_path is not None
    assert os.path.exists(file_path)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        assert "-----BEGIN LICENSE KEY-----" in content
        assert "-----END LICENSE KEY-----" in content
        assert "© 2025 CSky Developments" in content
        assert "All rights reserved." in content
        assert "CSky Developments retains full rights and intellectual property ownership." in content
    finally:
        os.remove(file_path)
