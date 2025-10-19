import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from .tools import anthropic_endpoint, available_tools
from .callbacks import before_agent, before_tool


model = os.getenv("MODEL_NAME", "vertex_ai/gemini-2.5-flash")

llm = LiteLlm(model)
if "claude" in model:
    llm = LiteLlm(model, api_base=anthropic_endpoint(model))


root_agent = LlmAgent(
    name="my_agent",
    model=llm,
    description="注文確認エージェント",
    instruction="あなたは注文情報を管理するするアシスタントです",
    tools=available_tools,
    before_agent_callback=before_agent,
    before_tool_callback=before_tool,
)
