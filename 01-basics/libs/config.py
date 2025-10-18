import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DB_HOST: str = os.getenv("DB_HOST", "db")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_NAME: str = os.getenv("DB_NAME", "ai_agents")
    DB_USER: str = os.getenv("DB_USER", "remote")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "remote")


settings = Settings()
