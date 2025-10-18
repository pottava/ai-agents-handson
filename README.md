# AI エージェント ハンズオン

AI エージェントの基礎から応用までを学びます。

## Overview

1. 基本: シンプルな LLM への問い合わせから、関数の呼び出しや MCP といったツールの利用

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
