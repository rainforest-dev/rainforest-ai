from autogen_core.models import UserMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.models.semantic_kernel import SKChatCompletionAdapter
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.ollama import (
    OllamaChatCompletion,
    OllamaChatPromptExecutionSettings,
)
from semantic_kernel.memory.null_memory import NullMemory

sk_client = OllamaChatCompletion(
    service_id="ollama",
    ai_model_id="phi4:latest",
)
settings = OllamaChatPromptExecutionSettings(temperature=0.2)

model_client = SKChatCompletionAdapter(
    sk_client,
    kernel=Kernel(memory=NullMemory()),
    prompt_settings=settings,
)

messages = [
    UserMessage(content="Write a very short story about a dragon.", source="user"),
]

stream = model_client.create_stream(messages=messages)


async def process_stream():
    async for response in stream:
        if isinstance(response, str):
            print(response, flush=True, end="")
        else:
            print("\n\n------------\n")
            print("The complete response:", flush=True)
            print(response.content, flush=True)
            print("\n\n------------\n")
            print("The token usage was:", flush=True)
            print(response.usage, flush=True)


import asyncio

asyncio.run(process_stream())
