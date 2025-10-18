# 生成 AI の基本

## 01. LLM の基本

シンプルに「あなたは誰？」と聞いてみます。以下の通り Python を実行してください。

```bash
python 01-basics/01-llm.py
```


## 02. 関数ツールの利用

Python による関数実装を活用し、より正確な四則演算が行ってみます。  
コードを実行し、四則演算を問題として出してみてください。

```bash
python 01-basics/02-tool-functions.py
```

突然ですがクイズです。いま LLM は何度呼び出されましたか？


## 03. 外部 API やデータベースの利用

外部の API やデータベースへのクエリを使った回答をさせてみます。  
ペットストアの利用者や来店予約を確認できます。質問をしてみましょう！

```bash
python 01-basics/03-tool-externals.py
```

もしサードパーティ モデルについても有効化しているようであれば  
環境変数にモデル名を設定して実行し直してみてください。  
例）

- Anthropic: export MODEL_NAME='vertex_ai/claude-haiku-4-5@20251001'
- Mistral: export MODEL_NAME='vertex_ai/mistral-medium-3@001'
- GPT OSS: export MODEL_NAME='vertex_ai/openai/gpt-oss-120b-maas'

（Llama 4、Qwen3 はうまく動かない・・）

```bash
export MODEL_NAME='vertex_ai/claude-haiku-4-5@20251001'
python 01-basics/03-tool-externals.py
```

どうですか？実行結果に差はありましたか？
