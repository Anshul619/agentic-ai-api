from typing import AsyncGenerator

from google import genai

from app.core.settings import settings


class GeminiProvider:

    def __init__(self):

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    async def chat(
        self,
        messages: list[dict]
    ) -> str:

        prompt = self._format_messages(messages)

        response = self.client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt
        )

        return response.text

    async def stream_chat(
        self,
        messages: list[dict]
    ) -> AsyncGenerator[str, None]:

        prompt = self._format_messages(messages)

        response = self.client.models.generate_content_stream(
            model=settings.GEMINI_MODEL,
            contents=prompt
        )

        for chunk in response:

            if chunk.text:
                yield chunk.text

    def _format_messages(
        self,
        messages: list[dict]
    ) -> str:

        formatted = []

        for msg in messages:

            role = msg["role"]
            content = msg["content"]

            formatted.append(
                f"{role.upper()}: {content}"
            )

        return "\n".join(formatted)