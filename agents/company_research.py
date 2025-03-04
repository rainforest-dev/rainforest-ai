from autogen_agentchat.agents import AssistantAgent
from autogen_core.tools import FunctionTool
from autogen_agentchat.ui import Console
from autogen_agentchat.teams import RoundRobinGroupChat

# from autogen_ext.models.semantic_kernel import SKChatCompletionAdapter
from autogen_ext.models.openai import OpenAIChatCompletionClient

# from semantic_kernel import Kernel
# from semantic_kernel.connectors.ai.ollama import (
#     OllamaChatCompletion,
#     OllamaChatPromptExecutionSettings,
# )
# from semantic_kernel.memory.null_memory import NullMemory

from utils.google_search import google_search

google_search_tool = FunctionTool(
    google_search,
    description="Search Google for information, returns results with a snippet and body content",
)

# sk_client = OllamaChatCompletion(
#     service_id="ollama",
#     ai_model_id="phi4:latest",
# )
# settings = OllamaChatPromptExecutionSettings(temperature=0.2)
# model_client = SKChatCompletionAdapter(
#     sk_client,
#     kernel=Kernel(memory=NullMemory()),
#     prompt_settings=settings,
# )

model_client = OpenAIChatCompletionClient(
    model="llama3.2:latest",
    base_url="http://localhost:11434/v1",
    api_key="your_api_key",
    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": False,
        "family": "unknown",
    },
)

search_agent = AssistantAgent(
    name="Google_Search_Agent",
    model_client=model_client,
    tools=[google_search_tool],
    description="Search Google for information, returns top 2 results with a snippet and body content",
    system_message="You are a helpful AI assistant. Solve tasks using your tools.",
)

report_agent = AssistantAgent(
    name="Report_Agent",
    model_client=model_client,
    description="Generate a report based the search and results of stock analysis",
    system_message="You are a helpful assistant that can generate a comprehensive report on a given topic based on search and stock analysis. When you done with generating the report, reply with TERMINATE.",
)

team = RoundRobinGroupChat([search_agent, report_agent], max_turns=3)
stream = team.run_stream(task="Write a product release plan of Apple in 2025")


# The Console class requires the event loop to be running, so we need to use 'await' inside an async function.
async def main():
    await Console(stream)


import asyncio

asyncio.run(main())
