import json
import redis.asyncio as redis

class RedisMemoryStore:

    def __init__(self):
        self.client = redis.Redis(
            host="localhost",
            port=6379,
            decode_responses=True
        )

    async def save_messages(
        self,
        session_id: str,
        messages: list
    ):

        await self.client.set(
            f"chat:{session_id}",
            json.dumps(messages)
        )

    async def load_messages(
        self,
        session_id: str
    ):

        data = await self.client.get(
            f"chat:{session_id}"
        )

        if not data:
            return []

        return json.loads(data)