from typing import AsyncGenerator

from google import genai

from app.core.settings import settings

from app.tools.registry import TOOL_REGISTRY

from google.genai import types

TOOLS = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="retrieve_documents",
                description="Retrieve relevant documents",
                parameters={
                    "type": "OBJECT",
                    "properties": {
                        "query": {
                            "type": "STRING"
                        }
                    },
                    "required": ["query"],
                },
            )
        ]
    )
]

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
    
    async def generate_with_tools(
        self,
        messages: list,
    ):

        response = self.client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=messages,
            config={
                "tools": TOOLS,
            },
        )

        candidate = response.candidates[0]

        for part in candidate.content.parts:

            function_call = getattr(
                part,
                "function_call",
                None,
            )

            if not function_call:
                continue

            function_name = function_call.name

            args = dict(function_call.args)

            tool = TOOL_REGISTRY[function_name]

            tool_result = await tool(**args)

            followup_response = (
                self.client.models.generate_content(
                    model=settings.GEMINI_MODEL,
                    contents=[
                        *messages,

                        {
                            "role": "model",
                            "parts": [
                                {
                                    "function_call": {
                                        "name": function_name,
                                        "args": args,
                                    }
                                }
                            ],
                        },

                        {
                            "role": "function",
                            "parts": [
                                {
                                    "function_response": {
                                        "name": function_name,
                                        "response": {
                                            "result": tool_result
                                        },
                                    }
                                }
                            ],
                        },
                    ],
                    config=types.GenerateContentConfig(
                        tools=TOOLS
                    ),
                )
            )

            return {
                "response": followup_response.text,
                "tool_calls": [
                    {
                        "tool": function_name,
                        "args": args,
                        "result": tool_result,
                    }
                ],
                "retrieved_docs": (
                    tool_result
                    if isinstance(tool_result, list)
                    else []
                ),
            }

        return {
            "response": response.text,
            "tool_calls": [],
            "retrieved_docs": [],
        }