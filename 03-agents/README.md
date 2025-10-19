# マルチ AI エージェント

複数の AI エージェントを連携させる様子を体験しましょう。  
03 のフォルダに移動してください。

```bash
cd 03-agents
```


## 01. マルチ AI エージェント（ローカル）

とある業務に特化したエージェントがすでに社内にあるといった場合  
そのエージェントと協調することで、より複雑なタスクの完遂を目指すこともできます。

ここではペットストア業務を例に、時刻エージェントとの共同作業により  
以下のような、現在時刻を鑑みた応答を実装してみます。

- "今週" 来客予定ある？
- 堂本さんの予約は "いつ" だっけ？
- "今日" 以降でキャンセルされた予約はある？

ADK を Web UI で起動してみます。

```bash
adk web
```

ブラウザで以下の URL にアクセスしてみてください。  
http://127.0.0.1:8000/dev-ui/?app=01

1. もし画面左上が `Select an agent` になっていたら `01` を選択し
2. 右下の `Type a message` に質問を入力し Enter を押してください。
3. 画面上表示される `get_current_time` などをクリックし、実際の入出力を確認してみてください。


## 02. プラグインの活用

Web UI はローカル開発には便利ですが、商用環境におけるトラブルシュートはどうすればいいでしょうか？

`02` は ADK の[プラグイン](https://google.github.io/adk-docs/plugins/)やコールバック、state をフル活用したサンプルです。  
また単体のエージェント評価ではなく、全体の動作を動かして試すための main 関数も用意しました。  
実行してみましょう。

```bash
python -m 02.agent
```

モデルを呼んだりツールを呼んだり、さまざまなポイントでログが出力されているのがわかります。  
`counter.py` というプラグインでは[処理トークン数やコール数といった出力](https://github.com/pottava/ai-agents-handson/blob/main/03-agents/02/plugins/counter.py#L43-L46)もしています。

対話形式で起動し `block` とだけ入力してみてください。  
処理を停止させるといったことも可能です！

```bash
adk run 02
```


## 03. クラウドへのデプロイ

### クラウドの API 有効化

まずは関連製品を使うためにサービスを有効化します。

```bash
gcloud services enable run.googleapis.com \
    cloudbuild.googleapis.com artifactregistry.googleapis.com
```

### Cloud Run へのデプロイ

四則演算エージェントをアイオワ リージョンにデプロイしてみます。

環境変数を `.env` ファイルとして設定し

```bash
cat << EOF > 03/calculator/.env
MODEL_NAME=vertex_ai/gemini-2.5-flash
GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT}
GOOGLE_CLOUD_LOCATION=global
EOF
```

ADK の `deploy` コマンドを実行します。  
認証が必要か聞かれたら、安全のため必要 (Y) だと回答してください。

```bash
export CLOUD_RUN_SERVICE_NAME="calculator-agent-service"
adk deploy cloud_run --region "us-central1" \
    --app_name "calculator-agent" --service_name "${CLOUD_RUN_SERVICE_NAME}" \
    ./03/calculator
```

### リモート エージェントへの接続

エンドポイントを確認して

```bash
endpoint=$( gcloud run services describe "${CLOUD_RUN_SERVICE_NAME}" --region "us-central1" --format='value(status.address.url)' )
```

セッションを作って

```bash
curl -sX POST -H "Authorization: Bearer $( gcloud auth print-identity-token )" -H "Content-Type: application/json" \
    ${endpoint}/apps/calculator-agent/users/user-01/sessions/session-001 | jq .
```

メッセージを送信してみます。  
（応答結果はすべてのやりとりが返ってくるため `sed` と `jq` で結果だけを抽出していますが、気になる方は `jq -s .` と書き換えてみてください）

```bash
curl -sX POST -H "Authorization: Bearer $( gcloud auth print-identity-token )" -H "Content-Type: application/json" ${endpoint}/run_sse \
    -d '{
        "app_name": "calculator-agent",
        "user_id": "user-01",
        "session_id": "session-001",
        "streaming": false,
        "new_message": {
            "role": "user",
            "parts": [{"text": "75*(430*91-7130)/(60*2000)の答えは？"}]
        }
    }' | sed 's/^data: *//' | jq -s ".[-1].content.parts"
```

Claude などを利用したい場合は 　
`.env` ファイルの `MODEL_NAME` を vertex_ai/claude-haiku-4-5@20251001 などに変え  
ADK の `deploy` コマンドで再度デプロイしてから試してみてください！

### A2A サーバーのデプロイ

AI エージェントが必要になる権限をもったサービスアカウントを作成し

```bash
gcloud iam service-accounts create calculator-agent-sa \
    --display-name "A service account for the calculator agent"
gcloud projects add-iam-policy-binding "${GOOGLE_CLOUD_PROJECT}" \
    --member "serviceAccount:calculator-agent-sa@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com" \
    --role "roles/aiplatform.user"
```

Cloud Run にデプロイします。  
（一時 RemoteA2aAgent の不具合により `--allow-unauthenticated` を指示している点には気をつけてください）

```bash
gcloud run deploy "${CLOUD_RUN_SERVICE_NAME}" --region "us-central1" --cpu 1 --memory "1Gi" --max-instances 1 \
    --set-env-vars "GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT},GOOGLE_CLOUD_LOCATION=global,APP_URL=${endpoint}" \
    --port "8080" --service-account "calculator-agent-sa" --allow-unauthenticated \
    --source 03/calculator_a2a
```

A2A エージェント カードを取得してみます。

```bash
curl -sX GET -H "Authorization: Bearer $( gcloud auth print-identity-token )" \
    ${endpoint}/.well-known/agent-card.json | jq .
```

CLI を使った動作確認は [こちら](https://cloud.google.com/run/docs/verify-deployment-a2a-agents) が有用です。


## 04. マルチ AI エージェント（リモート）

A2A プロトコルを使い、Cloud Run にデプロイされた AI エージェントと通信します。

```bash
CALCULATOR_AGENT_ENDPOINT=${endpoint} adk web
```
