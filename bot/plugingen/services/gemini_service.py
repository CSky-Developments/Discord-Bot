import time
from typing import Optional, List
from bot.logger import BotLogger

MODELS: List[str] = [
    "gemini-3-flash-preview",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
]

class GeminiService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.model_index = 0
        self.client = None
        self._init_client()

    def _init_client(self):
        try:
            from google import genai
            self.client = genai.Client(api_key=self.api_key)
        except Exception as e:
            BotLogger.error(f"Failed to initialize GeminiService: {e}")
            self.client = None

    def is_available(self) -> bool:
        return self.client is not None

    def generate(self, prompt: str) -> Optional[str]:
        if not self.client:
            return None

        retries = 5
        cooldown = 10.0

        for attempt in range(1, retries + 1):
            if self.model_index >= len(MODELS):
                BotLogger.warn("No model left to switch!")
                break

            current_model = MODELS[self.model_index]
            try:
                response = self.client.models.generate_content(
                    model=current_model,
                    contents=prompt
                )
                if response and response.text:
                    return response.text
                return None
            except Exception as ex:
                msg = str(ex)
                if "429" in msg or "Quota" in msg or "Too Many" in msg:
                    self.model_index += 1
                    BotLogger.warn(f"Quota limit reached for {current_model}. Switching model...")
                    if self.model_index < len(MODELS):
                        BotLogger.warn(f"Switched to model: {MODELS[self.model_index]}")
                        continue
                    break

                if "503" in msg or "overloaded" in msg:
                    if attempt < retries:
                        BotLogger.warn(f"Service overloaded. Retrying in {int(cooldown)} seconds... ({attempt}/{retries})")
                        time.sleep(cooldown)
                        cooldown *= 2
                        continue

                BotLogger.error(f"Request failed: {msg}")
                BotLogger.warn(f"Waiting for {int(cooldown)} seconds before retrying... [{attempt}/{retries}]")
                time.sleep(cooldown)
                cooldown *= 2

        BotLogger.error("FAILED TO GENERATE")
        return None
