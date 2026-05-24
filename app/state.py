from typing import TypedDict, List

class AgentState(TypedDict):
    session_id: str
    messages: List[dict]
    memories: List[str]
    user_input: str
    response: str