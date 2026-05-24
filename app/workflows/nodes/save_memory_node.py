from app.memory.redis import RedisMemoryStore

memory_store = RedisMemoryStore()

async def save_memory_node(state):

    await memory_store.save_messages(
        state["session_id"],
        state["messages"]
    )

    return state