import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from .libs import anthropic_endpoint
from .tools import available_tools


model = os.getenv("MODEL_NAME", "vertex_ai/gemini-2.5-flash")

llm = LiteLlm(model)
if "claude" in model:
    llm = LiteLlm(model, api_base=anthropic_endpoint(model))

root_agent = LlmAgent(
    name="my_agent",
    model=llm,
    description="ペットストア エージェント",
    instruction="""
        あなたは冷静で正確さを重視する、思いやりと敬意を持った優秀なアシスタントです。
        直感で質問に答えず、できる限り利用可能なツールを鑑み
        事前にどのように応答するかを慎重に計画、冷静に答えてください。
        ツールから複数の情報が返ってきたら、極力過不足なくユーザーに応答してください。
        また知らないことは知らない、できないことはできないと真摯に伝えつつ
        その場で自信をもって回答できることのみに対応してください。
        """.strip(),
    tools=available_tools,  # ここにツールを登録するだけ！！
)
