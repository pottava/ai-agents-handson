import os


# LiteLLM は claude に限って Vertex AI エンドポイントをうまく解決しないためワークアラウンド
def anthropic_endpoint(model: str) -> str:
    location = os.getenv("GOOGLE_CLOUD_LOCATION")
    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    model = model.removeprefix("vertex_ai/")

    if location == "global":
        return f"https://aiplatform.googleapis.com/v1/projects/{project}/locations/global/publishers/anthropic/models/{model}"
    return f"https://{location}-aiplatform.googleapis.com/v1/projects/{project}/locations/{location}/publishers/anthropic/models/{model}"
