import copy
from typing import Optional, Dict, Any

from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse, LlmRequest
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.base_tool import BaseTool
from google.genai import types


def before_agent(callback_context: CallbackContext) -> Optional[types.Content]:
    agent_name = callback_context.agent_name
    print(f"\n[Before Agent callback] {agent_name}")

    state = callback_context.state.to_dict()
    if state.get("skip_agent", False):
        print(f"[Before Agent callback] Skipping agent {agent_name}.")
        return types.Content(
            role="model",
            parts=[
                types.Part(
                    text=f"Agent {agent_name} skipped by before_agent_callback due to state."
                )
            ],
        )
    return None


def after_agent(callback_context: CallbackContext) -> Optional[types.Content]:
    agent_name = callback_context.agent_name
    print(f"\n[After Agent callback] {agent_name}")

    state = callback_context.state.to_dict()
    if state.get("replace_output", False):
        print(f"[After Agent callback] Replacing agent {agent_name}'s output.")
        return types.Content(
            role="model",
            parts=[types.Part(text=f"CReplacing original output.")],
        )
    return None


def before_model(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    agent_name = callback_context.agent_name
    print(f"[Before Model callback] {agent_name}")

    message = ""
    if llm_request.contents and llm_request.contents[-1].role == "user":
        if llm_request.contents[-1].parts:
            message = llm_request.contents[-1].parts[0].text

    # Block the LLM call
    if message and "BLOCK" in message.upper():
        print("[Before Model callback] 'BLOCK' keyword found. Skipping LLM call.")
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[types.Part(text="LLM call was blocked.")],
            )
        )
    return None


def after_model(
    callback_context: CallbackContext, llm_response: LlmResponse
) -> Optional[LlmResponse]:
    agent_name = callback_context.agent_name
    print(f"[After Model callback] {agent_name}")

    original_text = ""
    if llm_response.content and llm_response.content.parts:
        if llm_response.content.parts[0].text:
            original_text = llm_response.content.parts[0].text
        else:
            return None
    else:
        return None

    # Replace "joke" with "funny story" (case-insensitive)
    search_term = "joke"
    replace_term = "funny story"
    if search_term in original_text.lower():
        print(f"[After Model callback] Found '{search_term}'. Modifying response.")
        modified_text = original_text.replace(search_term, replace_term)
        modified_text = modified_text.replace(
            search_term.capitalize(), replace_term.capitalize()
        )
        modified_parts = [copy.deepcopy(part) for part in llm_response.content.parts]
        modified_parts[0].text = modified_text

        return LlmResponse(
            content=types.Content(role="model", parts=modified_parts),
            grounding_metadata=llm_response.grounding_metadata,
        )
    return None


def before_tool(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext
) -> Optional[Dict]:
    agent_name = tool_context.agent_name
    tool_name = tool.name
    print(f"[Before Tool callback] Tool '{tool_name}' in '{agent_name}'")
    print(f"[Before Tool callback]   args '{args}'")

    # Skip the tool execution
    if args.get("key", "").upper() == "BLOCK":
        print("[Before Tool callback] Detected 'BLOCK'. Skipping tool execution.")
        return {"result": "Tool execution was blocked."}
    return None


def after_tool(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict
) -> Optional[Dict]:
    agent_name = tool_context.agent_name
    tool_name = tool.name
    print(f"[After Tool callback] Tool '{tool_name}' in '{agent_name}'")

    original = ""
    if hasattr(tool_response, "result"):
        original = tool_response.result

    if tool_name == "get_capital_city" and original == "Washington, D.C.":

        # Create a new dictionary or modify a copy
        modified_response = copy.deepcopy(tool_response)
        modified_response["result"] = (
            f"{original} (Note: This is the capital of the USA)."
        )
        modified_response["note_added_by_callback"] = True

        print(f"[After Tool callback] Modified response: {modified_response}")
        return modified_response
    return None
