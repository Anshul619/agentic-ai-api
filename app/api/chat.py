from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.providers.gemini_provider import (
    GeminiProvider
)

from app.workflows.chat_workflow import graph

router = APIRouter()

@router.post("/chat")

async def chat(payload: dict):

    result = await graph.ainvoke({
        "session_id": payload["session_id"],
        "user_input": payload["message"],
        "messages": [],
        "memories": []
    })

    return {
        "response": result["response"],
        "tool_calls": result.get(
            "tool_calls",
            [],
        ),
        "evaluation": result.get(
            "evaluation",
            {},
        ),
    }

provider = GeminiProvider()

@router.post("/chat/stream")

async def stream_chat(payload: dict):

    async def event_stream():

        messages = [
            {
                "role": "user",
                "content": payload["message"]
            }
        ]

        async for token in provider.stream_chat(
            messages
        ):
            yield f"data: {token}\\n\\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream"
    )