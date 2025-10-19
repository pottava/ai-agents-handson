# AI エージェント ハンズオン

AI エージェントの基礎から応用までを学びます。

## Overview

1. 基本: シンプルな LLM への問い合わせから、関数の呼び出しや MCP といったツールの利用
2. AI エージェント: 役割の設定、ツールの利用、ユーザ・セッション管理、評価テスト
3. マルチ AI エージェント: A2A、WebUI でのデバッグ

## セットアップ

`.devcontainer/.env.example` ファイルをコピーして `.env` ファイルを作成します。

```bash
cp .devcontainer/.env.example .devcontainer/.env 
```

### Visual Studio Code の Dev Container が使える場合

このフォルダを VS Code で開き、Dev Container を起動してください。  
（セクションごとに別のコンテナとして起動し直す必要があります）

### それ以外の場合

仮想環境を作り、依存関係を解決してください。

```bash
uv venv
source .venv/bin/activate
uv sync --directory .devcontainer
```

`.env` ファイルを読み込み、環境変数を設定します。  
`DB_HOST` については `localhost` で上書きしてください。

```bash
source .devcontainer/.env
export DB_HOST="localhost"
```

## 認証

Google Cloud にログインし

```bash
gcloud auth login
```

プロジェクト ID を環境変数にセットしたら

```bash
export GOOGLE_CLOUD_PROJECT=
```

CLI のデフォルトに設定しつつ、Vertex AI を有効化しましょう。  
デフォルトのリージョンも global に設定しておきます。

```bash
gcloud config set project "${GOOGLE_CLOUD_PROJECT}"
gcloud services enable aiplatform.googleapis.com
```

自分の権限でローカルのプログラムを実行できるよう、  
アプリケーションのデフォルト認証情報も作成します。

```bash
gcloud auth application-default login
```

## Anthropic などパートナーモデルを使う場合

クラウドのコンソールから **利用規約への同意と有効化が必要** です。

1. Google Cloud コンソールの [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) に移動
2. `Anthropic` などと検索するか、リストから使いたいモデル (例: `Claude Haiku 4.5`) を見つけ、選択
3. "有効にする" をクリックします
4. 必要事項を記入すると利用規約が表示されるので、確認して "同意する" をクリックします

`Anthropic` や `Mistral` は API でそのまま利用できますが  
[GPT OSS](https://console.cloud.google.com/vertex-ai/publishers/openai/model-garden/gpt-oss-120b-maas) などオープンウェイト モデルは **API Service** という種類なら Model as a Service として利用できます。

パートナーモデルについての料金は以下を確認しましょう。  
https://cloud.google.com/vertex-ai/generative-ai/pricing?hl=en#partner-models


## ハンズオンの開始

章ごとに README ファイルを参照してください。

- [01-basics/README.md](https://github.com/pottava/ai-agents-handson/blob/main/01-basics/README.md)
- [02-agent/README.md](https://github.com/pottava/ai-agents-handson/blob/main/02-agent/README.md)
- [03-agents/README.md](https://github.com/pottava/ai-agents-handson/blob/main/03-agents/README.md)
- [04-memory/README.md](https://github.com/pottava/ai-agents-handson/blob/main/04-memory/README.md)
