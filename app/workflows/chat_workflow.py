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

from app.workflows.nodes.retrieve_node import (
    retrieve_node
)

from app.workflows.nodes.evaluate_node import (
    evaluate_node
)

from app.observability.tracing.node_wrapper import (
    traced_node
)

workflow = StateGraph(AgentState)

workflow.add_node(
    "retrieve",
    traced_node(
        "retrieve",
        retrieve_node,
    ),
)

workflow.add_node(
    "load_memory",
    load_memory_node
)

workflow.add_node(
    "chat",
    traced_node(
        "chat",
        chat_node
    )
)

workflow.add_node(
    "evaluate",
    traced_node(
        "evaluate",
        evaluate_node,
    ),
)

workflow.add_node(
    "save_memory",
    save_memory_node
)

workflow.set_entry_point("load_memory")

workflow.add_edge(
    "load_memory",
    "retrieve"
)

workflow.add_edge(
    "retrieve",
    "chat",
)

workflow.add_edge(
    "chat",
    "evaluate"
)

workflow.add_edge(
    "evaluate",
    "save_memory",
)

workflow.set_finish_point("save_memory")

graph = workflow.compile()