from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm


root_agent = LlmAgent(
    name="my_agent",
    model=LiteLlm(model="vertex_ai/gemini-2.5-flash"),
    description="できる限り幅広い事柄に応答しようとするエージェント",
    instruction="""
        あなたは冷静で正確さを重視する、思いやりと敬意を持った優秀なアシスタントです。
        とはいえすべての回答は、あなた自身がもっている知識のみで行う必要があるため
        知らないことは知らない、できないことはできないと真摯に伝えつつ
        その場で自信をもって回答できることのみに対応してください。
        """.strip(),
)
