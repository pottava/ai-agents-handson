from typing import Optional, Any

from google.adk.agents.base_agent import BaseAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.plugins.base_plugin import BasePlugin
from google.adk.tools import BaseTool, ToolContext


class ValidatePlugin(BasePlugin):
    """A custom plugin that counts agent and tool invocations."""

    def __init__(self) -> None:
        super().__init__(name="validator")

    async def before_tool_callback(
        self,
        *,
        tool: BaseTool,
        tool_args: dict[str, Any],
        tool_context: ToolContext,
    ) -> Optional[dict]:
        expected_user_id = tool_context.state.get("temp:session_user_id")
        actual_user_id = tool_args.get("user_id")

        if actual_user_id and actual_user_id != expected_user_id:
            print(f"Actual: {actual_user_id}, Expected: {expected_user_id}")
            return {"error": "Tool call blocked: User ID mismatch."}
        return None
