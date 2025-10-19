from typing import Optional, Any

from google.adk.agents import InvocationContext, BaseAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.events import Event
from google.adk.models import LlmRequest, LlmResponse
from google.adk.plugins import BasePlugin
from google.adk.tools import BaseTool, ToolContext
from google.genai import types


class LoggerPlugin(BasePlugin):

    def __init__(self):
        super().__init__(name="logger")

    async def on_user_message_callback(
        self,
        *,
        invocation_context: InvocationContext,
        user_message: types.Content,
    ) -> Optional[types.Content]:
        print(f"[On user message plugin] Agent: {invocation_context.agent.name}")

    async def before_run_callback(
        self, *, invocation_context: InvocationContext
    ) -> Optional[types.Content]:
        print(f"[Before run plugin] Agent: {invocation_context.agent.name}")

    async def on_event_callback(
        self, *, invocation_context: InvocationContext, event: Event
    ) -> Optional[Event]:
        print(f"[On event plugin] Agent: {invocation_context.agent.name}")

    async def after_run_callback(
        self, *, invocation_context: InvocationContext
    ) -> Optional[None]:
        print(f"[After run plugin] Agent: {invocation_context.agent.name}")

    async def before_agent_callback(
        self, *, agent: BaseAgent, callback_context: CallbackContext
    ) -> Optional[types.Content]:
        print(f"[Before Agent plugin] Agent: {agent.name}")

    async def after_agent_callback(
        self, *, agent: BaseAgent, callback_context: CallbackContext
    ) -> Optional[types.Content]:
        print(f"[After Agent plugin] Agent: {agent.name}")

    async def before_model_callback(
        self, *, callback_context: CallbackContext, llm_request: LlmRequest
    ) -> Optional[LlmResponse]:
        agent_name = callback_context.agent_name
        print(f"[Before Model plugin] Agent: {agent_name}")

    async def after_model_callback(
        self, *, callback_context: CallbackContext, llm_response: LlmResponse
    ) -> Optional[LlmResponse]:
        agent_name = callback_context.agent_name
        print(f"[After Model plugin] Agent: {agent_name}")

    async def before_tool_callback(
        self,
        *,
        tool: BaseTool,
        tool_args: dict[str, Any],
        tool_context: ToolContext,
    ) -> Optional[dict]:
        print(f"[Before Tool plugin] Tool: {tool.name}")

    async def after_tool_callback(
        self,
        *,
        tool: BaseTool,
        tool_args: dict[str, Any],
        tool_context: ToolContext,
        result: dict,
    ) -> Optional[dict]:
        print(f"[After Tool plugin] Tool: {tool.name}")
