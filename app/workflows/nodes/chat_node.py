from app.providers.gemini_provider import (
    GeminiProvider
)

provider = GeminiProvider()

async def chat_node(state):

    messages = state["messages"]

    messages.append({
        "role": "user",
        "parts": [
            {
                "text": state["user_input"]
            }
        ],
    })

    # response = await provider.chat(messages)

    result = await provider.generate_with_tools(
        messages
    )

    messages.append({
        "role": "model",
        "parts": [
            {
                "text": result["response"]
            }
        ],
    })

    state["messages"] = messages
    state["response"] = result["response"]
    state["tool_calls"] = result["tool_calls"]
    state["retrieved_docs"] = result["retrieved_docs"]

    return state