from google.adk.artifacts import InMemoryArtifactService
from google.adk.artifacts import GcsArtifactService

from .config import settings


def get_artifact_service():
    if settings.APP_ENV == "cloud":
        return GcsArtifactService(
            project=settings.GOOGLE_CLOUD_PROJECT,
            location=settings.GOOGLE_CLOUD_LOCATION,
            bucket_name=settings.GOOGLE_CLOUD_BUCKET_NAME,
        )
    else:
        return InMemoryArtifactService()
