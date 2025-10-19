import asyncio
import functools
import os
import click
import uvicorn

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from agent import root_agent
from agent_executor import ADKAgentExecutor
from dotenv import load_dotenv
from starlette.applications import Starlette


load_dotenv()


def make_sync(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))

    return wrapper


@click.command()
@click.option("--host", default="0.0.0.0")
@click.option("--port", default=8080)
@make_sync
async def main(host, port):
    agent_card = AgentCard(
        name=root_agent.name,
        description=root_agent.description,
        version="1.0.0",
        url=os.environ["APP_URL"],
        default_input_modes=["text", "text/plain"],
        default_output_modes=["text", "text/plain"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[
            AgentSkill(
                id="calculation",
                name="Calculator agent",
                description="Calculate arithmetic operations.",
                tags=["calculation"],
                examples=[
                    "75*(430*91-7130)/(60*2000)の答えは？",
                ],
            )
        ],
    )
    request_handler = DefaultRequestHandler(
        agent_executor=ADKAgentExecutor(
            agent=root_agent,
        ),
        task_store=InMemoryTaskStore(),
    )
    a2a_app = A2AStarletteApplication(
        agent_card=agent_card, http_handler=request_handler
    )
    routes = a2a_app.routes()
    app = Starlette(
        routes=routes,
        middleware=[],
    )
    config = uvicorn.Config(app, host=host, port=port, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    main()
