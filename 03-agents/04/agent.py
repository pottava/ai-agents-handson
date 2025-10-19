import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.remote_a2a_agent import (
    AGENT_CARD_WELL_KNOWN_PATH,
    RemoteA2aAgent,
)
from . import libs


model = os.getenv("MODEL_NAME", "vertex_ai/gemini-2.5-flash")
endpoint = os.getenv("CALCULATOR_AGENT_ENDPOINT", "http://localhost:8080")

llm = LiteLlm(model)
if "claude" in model:
    llm = LiteLlm(model, api_base=libs.anthropic_endpoint(model))

calculator = RemoteA2aAgent(
    name="calculator_agent",
    description="四則演算が得意なエージェントです",
    agent_card=f"{endpoint}{AGENT_CARD_WELL_KNOWN_PATH}",
    # a2a_client_factory=libs.a2a_client_factory(),
)

root_agent = LlmAgent(
    name="my_agent",
    model=llm,
    instruction="""
        どんな質問でも楽しいあいさつから始めてください。
        わからないことはわからないと答えても問題ありません。
    """.strip(),
    sub_agents=[calculator],
)
