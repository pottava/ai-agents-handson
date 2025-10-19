from google.adk.agents import LlmAgent
from google.adk.apps import App
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool
from google.adk.runners import Runner
from google.genai import types

from .tools import calculator_tools
from .callbacks import (
    before_agent,
    after_agent,
    before_model,
    after_model,
    before_tool,
    after_tool,
)
from .plugins.validate import ValidatePlugin
from .plugins.logger import LoggerPlugin
from .plugins.counter import CountInvocationPlugin


llm = LiteLlm(model="vertex_ai/gemini-2.5-flash")

greeter_agent = LlmAgent(
    name="greeter_agent",
    model=llm,
    description="あいさつエージェント",
    instruction="""
        **必ず** 今日誕生日の芸能人を一人、あいさつに織り交ぜてください。
        できるだけ若く著名な方が望ましいです。
    """,
    tools=[google_search],
)

calculator_agent = LlmAgent(
    name="calculator_agent",
    model=llm,
    description="四則演算エージェント",
    instruction="あなたは四則演算を支援するアシスタントです",
    generate_content_config=types.GenerateContentConfig(
        temperature=0.1,
        top_p=0.95,
    ),
    tools=calculator_tools,
    before_agent_callback=before_agent,
    after_agent_callback=after_agent,
    before_model_callback=before_model,
    after_model_callback=after_model,
    before_tool_callback=before_tool,
    after_tool_callback=after_tool,
    output_key="data",
)

root_agent = LlmAgent(
    name="coordinator_agent",
    model=llm,
    description="コーディネーターとしてエージェントを使い分けます",
    instruction="""
        単なる計算の依頼でも、その他どんな質問でも
        セッション開始時には **必ず** greeter_agent を利用して
        **極力楽しいあいさつから** 始めてください！！
        その上で依頼が完了しなければ処理を継続し、
        最終的な回答を試みてください。
        わからないことはわからないと答えても問題ありません。
    """.strip(),
    tools=[AgentTool(agent=greeter_agent), AgentTool(agent=calculator_agent)],
    before_model_callback=before_model,
)

# アプリケーションとしてプラグインを設定することで、すべての AI エージェントに一括反映
app = App(
    name="02",
    root_agent=root_agent,
    plugins=[ValidatePlugin(), LoggerPlugin(), CountInvocationPlugin()],
)


# 以下、python -m 02.agent で実行するための実装
async def main():
    runner = Runner(app=app, session_service=InMemorySessionService())
    try:
        session = await runner.session_service.create_session(
            app_name=runner.app_name,
            user_id="user-001",
        )
        async for event in runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=types.Content(
                role="user",
                parts=[types.Part.from_text(text="45*(987-65*10)/10 の答えは？")],
            ),
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    print(f"[{event.author}] {event.content.parts[0].text}")
                else:
                    print(f"Got event from {event.author}")
    finally:
        await runner.close()


import asyncio

if __name__ == "__main__":
    asyncio.run(main())
