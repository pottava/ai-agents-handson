from langchain_litellm import ChatLiteLLM


response = ChatLiteLLM(model="gemini-2.5-flash-lite").invoke("あなたは誰？")
print(response.content)
