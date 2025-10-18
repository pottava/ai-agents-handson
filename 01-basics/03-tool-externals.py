import os
import random
from langchain_litellm import ChatLiteLLM
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
import libs
from tools.apis import get_users, get_user_by_id
from tools.database import get_appointments


model = os.getenv("MODEL_NAME", "gemini-2.5-flash")

default_queries = [
    "ペットストアのすべてのお客様のメールアドレスを教えてください",
    "ペットストアに過去来店されたお客様は誰ですか？",
    "堂本という方の来店予定はありますか？",
]

user_input = input("質問したいことを入力してください: ")
query = user_input.strip() or random.choice(default_queries)
print(f"\n--- モデル: {model} ---")
print(f"\n--- 質問: {query} ---\n")


external_tools = {
    "get_users": get_users,
    "get_user_by_id": get_user_by_id,
    "get_appointments": get_appointments,
}


# 1. API コールや DB クエリをツールとして LLM にバインド
llm = ChatLiteLLM(model=model).bind_tools(external_tools.values())
if "claude" in model:
    llm = ChatLiteLLM(model=model, api_base=libs.anthropic_endpoint(model)).bind_tools(
        external_tools.values()
    )


# 2. LLM にツールの呼び出し指示を考えさせる
messages = [
    SystemMessage(
        content="""
        You are an excellent assistant who is calm and values accuracy.
        Don't answer questions based on your intuition; instead, make good use
        of the tools available to you and carefully consider how to respond.
        """.strip(),
    ),
    HumanMessage(query),
]
response = llm.invoke(messages)


# 3. LLM がツールを使うべきと判断した場合、その指示に従ってツールを実行
while response.tool_calls:
    messages.append(response)  # 応答を履歴に追加

    print("--- LLMの判断: ツールを利用します ---")
    print(response.tool_calls)

    for tool_call in response.tool_calls:
        tool = external_tools[tool_call["name"]]
        output = tool.invoke(tool_call["args"])

        # 4. ツールの実行結果をメッセージに追記
        messages.append(ToolMessage(content=str(output), tool_call_id=tool_call["id"]))

    # 5. 更新された履歴で、再度 LLM を呼び出す
    response = llm.invoke(messages)


print("\n--- 最終的な LLM の回答 ---")
print(f"{response.content}\n\n")
