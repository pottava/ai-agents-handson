import pprint

from sentence_transformers import SentenceTransformer
import torch.nn.functional as F


# https://huggingface.co/cl-nagoya/ruri-v3-30m
MODEL_NAME = "cl-nagoya/ruri-v3-30m"


print("\n***** 1. 埋め込みベクトルの生成とコサイン類似度の例 *****\n")

model = SentenceTransformer(MODEL_NAME, device="cpu")

sentences = [
    "川べりでサーフボードを持った人たちがいます",
    "サーファーたちが川べりに立っています",
    "トピック: 瑠璃色のサーファー",
    "検索クエリ: 瑠璃色はどんな色？",
    "検索文書: 瑠璃色は、紫みを帯びた濃い青。名は、半貴石の瑠璃による。JIS慣用色名では「こい紫みの青」と定義している。",
]

tensor = model.encode(sentences, convert_to_tensor=True)
print("\n===== 次元数 =====\n")
print(tensor.size())

print(f"\n===== {sentences[0]} =====\n")
print(tensor[0])

similarities = F.cosine_similarity(tensor.unsqueeze(0), tensor.unsqueeze(1), dim=2)
print("\n===== コサイン類似度 =====\n")
print(similarities)


print("\n***** 2. ベクトル DB を使った近似最近傍探索例 *****\n")

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy

embeddings = HuggingFaceEmbeddings(
    model_name=MODEL_NAME,
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)

db = FAISS.from_texts(
    ["明日の天気は晴れです", "明日の天気は雨です", "晴れが好きです"],
    embeddings,
    distance_strategy=DistanceStrategy.MAX_INNER_PRODUCT,
)
print("\n===== 近似最近傍探索結果とスコア =====\n")
pprint.pprint(db.similarity_search_with_score("次の日はいい天気です"))
