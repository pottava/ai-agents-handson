from google.adk.memory import InMemoryMemoryService
from google.adk.memory import VertexAiMemoryBankService

from .config import settings


def get_memory_service():
    if settings.APP_ENV == "cloud":
        return VertexAiMemoryBankService(
            project=settings.GOOGLE_CLOUD_PROJECT,
            location=settings.GOOGLE_CLOUD_LOCATION,
            agent_engine_id=settings.GOOGLE_CLOUD_AGENT_ENGINE,
        )
    else:
        return InMemoryMemoryService()
