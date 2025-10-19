from google.adk.tools import ToolContext


def get_orders(user_id: str, tool_context: ToolContext) -> dict:
    """
    指定されたユーザーの注文情報を返します
    """
    # api_key = tool_context.state.get("api_key")
    # if not api_key:
    #     return {"status": "エラー: 該当の API キーがありません"}

    return {"status": "success", "orders": 10}
