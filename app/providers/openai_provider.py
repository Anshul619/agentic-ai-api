
import asyncio
from app.providers.base import LLMProvider

class OpenAIProvider(LLMProvider):

    async def chat(self, messages):
        return "sample response"

    async def stream_chat(self, messages):

        text = "Streaming response from provider"

        for token in text.split():
            await asyncio.sleep(0.1)
            yield token + " "
