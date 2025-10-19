from typing import Optional, Dict, Any

from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.base_tool import BaseTool
from google.genai import types


# root_agent は invocation_context にユーザ ID を保持しているが、sub_agent にはないため state にもつ
def before_agent(callback_context: CallbackContext) -> Optional[types.Content]:
    if location := callback_context.state.get("location"):
        print(f"[Before agent] Location: {location}")

    # @see https://google.github.io/adk-docs/sessions/state/#organizing-state-with-prefixes-scope-matters
    user_id = callback_context.state.get("temp:session_user_id")
    if user_id:
        return None
    if (
        callback_context
        and callback_context._invocation_context
        and callback_context._invocation_context.session
    ):
        user_id = callback_context._invocation_context.session.user_id
        callback_context.state["temp:session_user_id"] = user_id
        print(f"[Before agent] User ID: {user_id}")
    return None


def before_tool(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext
) -> Optional[Dict]:
    expected_user_id = tool_context.state.get("temp:session_user_id")
    actual_user_id = args.get("user_id")
    print(f"[Before tool] Actual ID: {actual_user_id}, Expected ID: {expected_user_id}")

    # user_id を利用するツールの場合、セッション利用中のユーザーと一致することを確認する
    if actual_user_id and actual_user_id != expected_user_id:
        return {"error": "Tool call blocked: User ID mismatch."}
    return None
