from app.observability.tracing.workflow_tracer import (
    WorkflowTracer
)

tracer = WorkflowTracer()


def traced_node(
    node_name,
    node_fn
):

    async def wrapper(state):

        return await tracer.trace_node(
            node_name=node_name,
            fn=node_fn,
            state=state
        )

    return wrapper