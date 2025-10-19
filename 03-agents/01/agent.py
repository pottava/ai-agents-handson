from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import (
    StdioConnectionParams,
    StdioServerParameters,
)
from toolbox_core import ToolboxSyncClient


llm = LiteLlm("vertex_ai/gemini-2.5-flash")

timezone_agent = LlmAgent(
    name="timezone_agent",
    model=llm,
    description="時間管理エージェント",
    instruction="""
        あなたは日時やタイムゾーンに関する質問に対応するアシスタントです。
        日時やタイムゾーン以外の質問だった場合は日本の現在時刻を応答してください。
        """.strip(),
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="uvx", args=["mcp-server-time"]
                )
            )
        )
    ],
    output_key="datetime",
)

dbquery_agent = LlmAgent(
    name="dbquery_agent",
    model=llm,
    description="ペットストア情報検索エージェント",
    instruction="""
        あなたはペットストアに関する質問に対応するアシスタントです。
        timezone_agent の {datetime} を活用しつつ
        来店予約や顧客についての情報を検索して回答してほしいのですが
        ツールから複数の情報が返ってきたら、極力過不足なくユーザーに応答してください。
        来店日時や予約のステータスには十分注意してほしいものの
        できるだけ search-appointments か search-appointments-by-status を
        使って、フィルタリングはクエリに頼らずあなたが考えてください！
        改めてですが、来店日時や予約のステータスには十分注意してください。
        """.strip(),
    tools=ToolboxSyncClient("http://db-toolbox:5000").load_toolset(),
    output_key="petstore-information",
)

merger_agent = LlmAgent(
    name="merger_agent",
    model=llm,
    description="ペットストア エージェント",
    instruction="""
        あなたはペットストアに関する質問に対応するアシスタントです。
        各エージェントの出力を参考に、冷静に答えてください。
        自信をもって回答できることのみに対応してください。

        まずは一言、質問への回答を述べてください。
        相手のトーンを鑑み、気遣いが必要なら寄り添う一言から始めてもいいです。

        来店予約に関する出力は最初に予約件数、その上で以下の項目のみを含めてください。
        複数回答がある場合は予約日時の照準にソートして、
        完了した予定やキャンセルされた予定を回答にいれるかは真剣に考えてください。
        - お客様名
        - 来店日時
        - 目的
        - 状況

        お客様に関する情報は以下のみの応答でよいです。
        - お客様名
        - 連絡先
        """.strip(),
    output_key="merger_agent",
)

root_agent = SequentialAgent(
    name="my_agent",
    description="現在時刻を確認しつつ、必要な情報を検索して回答してください",
    sub_agents=[timezone_agent, dbquery_agent, merger_agent],
)
