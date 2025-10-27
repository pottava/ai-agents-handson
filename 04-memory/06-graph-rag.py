from langchain_litellm import ChatLiteLLM
from langchain_core.documents import Document
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_neo4j import Neo4jGraph


llm = ChatLiteLLM(model="vertex_ai/gemini-2.5-flash-lite")

graph_transformer = LLMGraphTransformer(llm, ignore_tool_usage=True)

text = """
物語の中心は、互いの正体を隠して偽りの家族を演じるフォージャー家です。
父ロイド・フォージャーは、西国（ウェスタリス）の敏腕スパイ「黄昏（たそがれ）」。東国（オスタニア）の平和を脅かす政治家ドノバン・デズモンドに接近する任務「オペレーション〈梟〉（ストリクス）」のため、精神科医に扮して急遽家族を作ります。
母ヨル・フォージャーは、表向きは市役所職員ですが、裏では幼い頃から暗殺稼業を営む凄腕の殺し屋「いばら姫」。独身であることが周囲から怪しまれないよう、利害が一致したロイドと偽装結婚します。
娘アーニャ・フォージャーは、ある組織の実験で生み出された、他人の心を読める超能力者。孤児院にいたところをロイドに引き取られます。父がスパイ、母が殺し屋という刺激的な家庭環境を唯一知り、ワクワクしながら学校生活を送っています。
一家のペットであるボンド・フォージャーは、未来予知能力を持つ犬。その能力でたびたびフォージャー家の危機を救います。
この奇妙な家族を取り巻く人物たちも物語を彩ります。ヨルの弟ユーリ・ブライアは、姉を溺愛するあまりロイドを敵視していますが、彼の正体は姉が知らない国家保安局（SSS）の少尉で、スパイである「黄昏」を追っています。
アーニャが通う名門イーデン校では、任務の標的であるドノバンの次男ダミアン・デズモンドが重要な存在です。アーニャは彼と親しくなるミッションを課されますが、ダミアンはアーニャを意識しつつも素直になれないツンデレな関係です。
アーニャの初めての親友ベッキー・ブラックベルは、彼女の最大の理解者として学校生活を支えます。
"""

documents = [Document(page_content=text)]

graph_documents = graph_transformer.convert_to_graph_documents(documents)

print("\nNodes:\n")
for node in graph_documents[0].nodes:
    print(node)
print("\nRelationships:\n")
for rel in graph_documents[0].relationships:
    print(rel)

# Neo4j に解析したグラフデータを保存
graph = Neo4jGraph()
graph.add_graph_documents(graph_documents)
