import os
import httpx

from google.auth import default
from google.auth.transport.requests import Request
from a2a.client import ClientConfig, ClientFactory
from a2a.types import TransportProtocol


# LiteLLM は claude に限って Vertex AI エンドポイントをうまく解決しないためワークアラウンド
def anthropic_endpoint(model: str) -> str:
    location = os.getenv("GOOGLE_CLOUD_LOCATION")
    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    model = model.removeprefix("vertex_ai/")

    if location == "global":
        return f"https://aiplatform.googleapis.com/v1/projects/{project}/locations/global/publishers/anthropic/models/{model}"
    return f"https://{location}-aiplatform.googleapis.com/v1/projects/{project}/locations/{location}/publishers/anthropic/models/{model}"


# Google Cloud 認証を httpx.Auth として実装
class GoogleAuthRefresh(httpx.Auth):
    def __init__(self, scopes):
        self.credentials, _ = default(scopes=scopes)
        self.transport_request = Request()
        self.credentials.refresh(self.transport_request)

    def auth_flow(self, request):
        if not self.credentials.valid:
            self.credentials.refresh(self.transport_request)
        request.headers["Authorization"] = f"Bearer {self.credentials.token}"
        yield request


def a2a_client_factory():
    return ClientFactory(
        ClientConfig(
            httpx_client=httpx.AsyncClient(
                auth=GoogleAuthRefresh(
                    scopes=["https://www.googleapis.com/auth/cloud-platform"]
                ),
                headers={"Content-Type": "application/json"},
                timeout=60,
            ),
            use_client_preference=True,
            supported_transports=[TransportProtocol.http_json],
        )
    )
