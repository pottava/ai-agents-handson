import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from .tools import anthropic_endpoint, calculator_tools


model = os.getenv("MODEL_NAME", "vertex_ai/gemini-2.5-flash")

llm = LiteLlm(model)
if "claude" in model:
    llm = LiteLlm(model, api_base=anthropic_endpoint(model))

root_agent = LlmAgent(
    name="my_agent",
    model=llm,
    description="四則演算エージェント",
    instruction="あなたは四則演算を支援するアシスタントです",
    tools=calculator_tools,
)
