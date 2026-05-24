from langgraph.graph import StateGraph

from app.state import AgentState

from app.workflows.nodes.memory_node import (
    load_memory_node
)

from app.workflows.nodes.chat_node import (
    chat_node
)

from app.workflows.nodes.save_memory_node import (
    save_memory_node
)

workflow = StateGraph(AgentState)

workflow.add_node(
    "load_memory",
    load_memory_node
)

workflow.add_node(
    "chat",
    chat_node
)

workflow.add_node(
    "save_memory",
    save_memory_node
)

workflow.set_entry_point("load_memory")

workflow.add_edge(
    "load_memory",
    "chat"
)

workflow.add_edge(
    "chat",
    "save_memory"
)

workflow.set_finish_point("save_memory")

graph = workflow.compile()