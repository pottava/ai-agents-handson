from typing import Optional, Any

from google.adk.agents.base_agent import BaseAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse, LlmRequest
from google.adk.plugins.base_plugin import BasePlugin
from google.adk.tools import BaseTool, ToolContext


class CountInvocationPlugin(BasePlugin):
    """A custom plugin that counts agent and tool invocations."""

    def __init__(self) -> None:
        """Initialize the plugin with counters."""
        super().__init__(name="count_invocation")
        self.agent_count: int = 0
        self.llm_request_count: int = 0
        self.tool_count: int = 0

    async def before_agent_callback(
        self, *, agent: BaseAgent, callback_context: CallbackContext
    ) -> None:
        """Count agent runs."""
        self.agent_count += 1
        print(f"[Plugin] Agent run count: {self.agent_count}")

    async def before_model_callback(
        self, *, callback_context: CallbackContext, llm_request: LlmRequest
    ) -> None:
        """Count LLM requests."""
        self.llm_request_count += 1
        print(f"[Plugin] LLM request count: {self.llm_request_count}")

    async def after_model_callback(
        self, *, callback_context: CallbackContext, llm_response: LlmResponse
    ) -> Optional[LlmResponse]:
        if (
            llm_response.usage_metadata
            and llm_response.usage_metadata.prompt_token_count
            and llm_response.usage_metadata.candidates_token_count
            and llm_response.usage_metadata.total_token_count
        ):
            input = llm_response.usage_metadata.prompt_token_count
            out = llm_response.usage_metadata.candidates_token_count
            total = llm_response.usage_metadata.total_token_count
            print(f"[After model] Token: {total} (in: {input}, out: {out})")
        return None

    async def before_tool_callback(
        self,
        *,
        tool: BaseTool,
        tool_args: dict[str, Any],
        tool_context: ToolContext,
    ) -> Optional[dict]:
        self.tool_count += 1
        print(f"[Plugin] Tool request count: {self.tool_count}")
