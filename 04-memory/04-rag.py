import re
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.settings import Settings
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from langchain_litellm import ChatLiteLLM


Settings.embed_model = GoogleGenAIEmbedding(model="vertex_ai/gemini-embedding-001")
Settings.llm = ChatLiteLLM(model="vertex_ai/gemini-2.5-flash-lite")


# PDF の読み込み
documents = SimpleDirectoryReader("04-memory/docs/").load_data()

# インデックスの作成
index = VectorStoreIndex.from_documents(documents)
embedding_dict = index.vector_store.to_dict()["embedding_dict"]

# インデックスの中身を確認
for i, node in enumerate(list(index.docstore.docs.values())):
    print(f"チャンク #{i+1} (Node ID: {node.node_id})")

    print("\n--- テキスト ---")
    text = re.sub(r"\s+", "", node.get_content()).strip()
    print(text[:200] + "...")

    print("\n--- ベクトル ---")
    try:
        embedding = embedding_dict[node.node_id]
        print(embedding[:5])  # 最初の 5 次元だけ
    except Exception as e:
        print("ベクトルなし")

    print("\n" + "=" * 30 + "\n")

# インデックスをベクトル DB + 組み込み LLM として利用
db = index.as_query_engine()

response = db.query("田中さんは競合についてどう言っていますか？")

print("\n✅ 応答:")
print(response)
print("-" * 50)

print("\n✅ ソースとなったチャンク:")
if response.source_nodes:
    for i, source_node in enumerate(response.source_nodes):
        print(f"--- ソース {i+1} (スコア: {source_node.score:.4f}) ---")
        print(f"メタデータ: {source_node.node.metadata}")
        print()
else:
    print("ソースノードが見つかりませんでした。")
