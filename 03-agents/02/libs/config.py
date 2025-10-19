import os
import logging
from dotenv import load_dotenv


load_dotenv()


class Settings:
    APP_ENV: str = os.getenv("APP_ENV", "local")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "DEBUG")

    GOOGLE_CLOUD_PROJECT: str = os.getenv("GOOGLE_CLOUD_PROJECT", "***")
    GOOGLE_CLOUD_LOCATION: str = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
    GOOGLE_CLOUD_AGENT_ENGINE: str = os.getenv("GOOGLE_CLOUD_AGENT_ENGINE", "***")
    GOOGLE_CLOUD_BUCKET_NAME: str = os.getenv("GOOGLE_CLOUD_BUCKET_NAME", "***")


settings = Settings()

logging.basicConfig(
    level=logging.getLevelNamesMapping()[settings.LOG_LEVEL],
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
