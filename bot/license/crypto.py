import base64
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

class AESEncrypter:
    @staticmethod
    def encrypt(aes_key: str, aes_iv: str, data: str) -> str:
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data.encode("utf-8")) + padder.finalize()

        cipher = Cipher(
            algorithms.AES(aes_key.encode("utf-8")),
            modes.CBC(aes_iv.encode("utf-8"))
        )
        encryptor = cipher.encryptor()
        encrypted_bytes = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(encrypted_bytes).decode("utf-8")

class KeyGenerator:
    @staticmethod
    def generate_key(salt: str, ip: str, port: int, uuid: str) -> str:
        input_data = f"{ip}:{port}:{uuid}:{salt}"
        digest = hashlib.sha256(input_data.encode("utf-8")).digest()
        return base64.b64encode(digest).decode("utf-8")
