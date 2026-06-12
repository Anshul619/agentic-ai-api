from typing import TypedDict, List, Dict, Any


class AgentState(TypedDict):

    session_id: str

    messages: List[dict]

    memories: List[str]

    user_input: str

    retrieved_docs: List[str]

    tool_calls: List[dict]

    evaluation: Dict[str, Any]

    response: str