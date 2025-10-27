from langchain_litellm import ChatLiteLLM
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory


# セッション ID ごとにチャット履歴を保存するためのストア
store = {}


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "友人として、会話は簡潔に、しかし親しみ深く、日本語で行ってください。",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

runnable = prompt | ChatLiteLLM(
    model="vertex_ai/gemini-2.5-flash-lite",
    temperature=0.5,
)

chain = RunnableWithMessageHistory(
    runnable=runnable,
    get_session_history=get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)


def chat_with_bot(session_id: str):
    count = 0
    while True:
        print("---")
        message = input(f"You [{count}]: ")

        # exit と書いたら終了
        if message.lower() == "exit":
            break

        response = chain.invoke(
            input={"input": message},
            config={"configurable": {"session_id": session_id}},
        )
        print(f"AI: {response.content}")
        count += 1


if __name__ == "__main__":
    chat_with_bot("session-id")
