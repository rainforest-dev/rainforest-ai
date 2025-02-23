import tempfile
from typing import Literal
from autogen_core.models import UserMessage
from autogen_ext.models.semantic_kernel import SKChatCompletionAdapter
from pydantic import BaseModel
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.ollama import (
    OllamaChatCompletion,
    OllamaChatPromptExecutionSettings,
)
from semantic_kernel.memory.null_memory import NullMemory
from autogen_ext.cache_store.diskcache import DiskCacheStore
from autogen_ext.models.cache import CHAT_CACHE_VALUE_TYPE, ChatCompletionCache
from diskcache import Cache


class AgentResponse(BaseModel):
    thoughts: str
    response: Literal["happy", "sad", "neutral"]


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
    UserMessage(content="Hello, how are you?", source="user"),
]


async def main():
    with tempfile.TemporaryDirectory() as temp_dir:
        cache_store = DiskCacheStore[CHAT_CACHE_VALUE_TYPE](Cache(temp_dir))
        cache_client = ChatCompletionCache(model_client, cache_store)
        stream = cache_client.create_stream(messages=messages)
        # async for response in stream:
        #     if isinstance(response, str):
        #         print(response, flush=True, end="")
        #     else:
        #         print("\n\n------------\n")
        #         print("The complete response:", flush=True)
        #         print(response.content, flush=True)
        #         print("\n\n------------\n")
        #         print("The token usage was:", flush=True)
        #         print(response.usage, flush=True)
        response = await cache_client.create(messages=messages)
        print(response)
        response = await cache_client.create(messages=messages)
        print(response)


import asyncio

asyncio.run(main())
