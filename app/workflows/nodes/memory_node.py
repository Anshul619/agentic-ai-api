from app.memory.redis import RedisMemoryStore

memory_store = RedisMemoryStore()

async def load_memory_node(state):

    messages = await memory_store.load_messages(
        state["session_id"]
    )

    state["messages"] = messages

    return state