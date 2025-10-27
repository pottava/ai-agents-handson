from langchain_litellm import ChatLiteLLM
from langchain.memory import ConversationSummaryMemory


llm = ChatLiteLLM(model="vertex_ai/gemini-2.5-flash-lite")
memory = ConversationSummaryMemory(llm=llm)

memory.save_context(
    {"input": "こんにちは！今日は晴れていい天気だね"},
    {"output": "それはよかったです。本日はどんなことをお手伝いしましょうか？"},
)
memory.save_context(
    {"input": "銀行口座が凍結されていそうなんだけど"},
    {"output": "ではまず、口座番号の確認をさせてください。"},
)

variables = memory.load_memory_variables({})
print(f"\n{variables['history']}\n\n")
