from app.providers.gemini_provider import (
    GeminiProvider
)

provider = GeminiProvider()

async def chat_node(state):

    messages = state["messages"]

    messages.append({
        "role": "user",
        "content": state["user_input"]
    })

    response = await provider.chat(messages)

    messages.append({
        "role": "assistant",
        "content": response
    })

    state["messages"] = messages
    state["response"] = response

    return state