# AI エージェント

LLM の基本編でも利用していた [LiteLLM](https://docs.litellm.ai/docs/) をベースにしつつ  
Google の [Agent Development Kit (ADK)](https://google.github.io/adk-docs/) と
Gemini の API を使って、エージェントと会話してみましょう。

02 のフォルダに移動してください。

```bash
cd 02-agent/
```

ADK で LiteLLM を使う場合は [モデル名に `vertex_ai/` というプリフィックスが必要](https://docs.litellm.ai/docs/providers/vertex) です。

```bash
export MODEL_NAME='vertex_ai/gemini-2.5-flash'
```


## 01. エージェントの基本実装

ADK は `run` コマンドを使うと対話形式で起動します。  
`[user]` と表示されたら実際に会話を始めてみて下さい。

```bash
adk run 01
```


## 02. 関数ツールの利用

LLM の基本編で設定したツール群をエージェントで実装した例。

ADK には関数シグネチャなどに[お作法](https://google.github.io/adk-docs/tools/function-tools/)はあれど、while 文などの必要もなくシンプルに。  
https://github.com/pottava/ai-agents-handson/blob/main/02-agent/02/agent.py#L26

もし外部 API が OpenAPI による定義がされていれば [spec ファイルを活用](https://google.github.io/adk-docs/tools/openapi-tools/)したり、  
LangChain や CrewAI といったフレームワークの[ツールを活用](https://google.github.io/adk-docs/tools/third-party-tools/) することもできます。

必須ではないですが、API や DB へのクエリについては並列実行できるように非同期処理へ実装を変えています。

- https://github.com/pottava/ai-agents-handson/blob/main/02-agent/02/tools/apis.py
- https://github.com/pottava/ai-agents-handson/blob/main/02-agent/02/tools/database.py

ADK を対話形式で起動し、ペットストアに関する質問をしてみてください。

```bash
adk run 02
```

Anthropic のモデルでも試してみましょう。

```bash
export MODEL_NAME='vertex_ai/claude-haiku-4-5@20251001'
adk run 02
```


## 03. MCP の活用

関数ツールはコードを書かなければいけない分、厳密な制御はしやすいですが  
MCP を使うことでサードパーティのツール群も活用しやすくなります。

データベースへのアクセスに Google の [MCP Toolbox for Databases](https://googleapis.github.io/genai-toolbox/getting-started/introduction/) を使ってみます。  
組み込みの `execute_sql` を使ったり、`postgres-sql` で独自ツールを定義することもできます。  
https://github.com/pottava/ai-agents-handson/blob/main/.devcontainer/.toolbox/tools.yaml

[MCP サーバーを一緒に起動](https://github.com/pottava/ai-agents-handson/blob/main/.devcontainer/compose.yaml#L36-L46)すれば、ローカルのツールとして利用できます。

02. 同様に ADK を対話形式で起動し、ペットストアに関する質問をしてみてください。

```bash
export MODEL_NAME='vertex_ai/gemini-2.5-flash'
adk run 03
```


## 04. セッション

AI エージェントとの対話は "セッション" という単位で行われます。

ADK ではまず、ユーザーごとにセッションを生成した上で会話を開始する仕様のため  
API コールの引数となるユーザ ID が一致しているか確かめるといったこともできます。  
ID をツールやエージェント間で持ち回すために [state](https://google.github.io/adk-docs/sessions/state/) というものを使いつつ  
その確認には[コールバック](https://google.github.io/adk-docs/callbacks/)を利用します。  
https://github.com/pottava/ai-agents-handson/blob/main/02-agent/04/callbacks.py#L32-L38

実際の動作を確認してみましょう。ADK を API サーバとして起動し

```bash
adk api_server
```

`04` アプリケーションに `ID: 3` というユーザで `sess01` というセッションを開始してみます。

```bash
curl -isX POST -H "Content-Type: application/json" http://localhost:8000/apps/04/users/3/sessions/sess01
```

開始したセッションに、注文状況を問い合わせてみます。  
HTTP リクエストの応答にも注目しつ。

```bash
curl -sX POST -H "Content-Type: application/json" http://localhost:8000/run -d '{
        "app_name": "04",
        "user_id": "3",
        "session_id": "sess01",
        "new_message": {
            "role": "user",
            "parts": [{
                "text": "ユーザ ID: 3 の注文を教えて"
            }]
        }
    }' | jq -r 'if type == "array" then .[-1] else . end'
```

`ID: 3` 以外の問い合わせを試してみてください。要求が弾かれます。


## 05. テスト

ADK における AI エージェントの評価は Trajectory（軌跡）と最終的な出力で行います。  
それぞれの閾値をテストの設定として以下のように定義し  
https://github.com/pottava/ai-agents-handson/tree/main/02-agent/05/eval/data/test_config.json

`eval` を実行してみましょう。

```bash
adk eval 05 05/test_001.evalset.json --config_file_path 05/test_config.json
```

うまくいけば `Tests passed: 1` になったかと思います。
fail するようであれば `--print_detailed_results` オプションを有効にして再実行すると

```json
{
    "eval_metric_results": [
        {
            "metric_name": "tool_trajectory_avg_score",
            "threshold": 1.0,
            "score": 0.0
        },
        {
            "metric_name": "response_match_score",
            "threshold": 0.9,
            "score": 0.25
        }
    ]
}
```

といった詳細な状況を確認できます。
