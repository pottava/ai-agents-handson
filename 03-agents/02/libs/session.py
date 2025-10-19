from google.adk.sessions import InMemorySessionService
from google.adk.sessions import VertexAiSessionService

from .config import settings


def get_session_service():
    if settings.APP_ENV == "cloud":
        return VertexAiSessionService(
            project=settings.GOOGLE_CLOUD_PROJECT,
            location=settings.GOOGLE_CLOUD_LOCATION,
        )
    else:
        return InMemorySessionService()
