from app.tools.retrieval import (
    retrieve_documents,
)


async def retrieve_node(state):

    docs = await retrieve_documents(
        state["user_input"]
    )

    return {
        "retrieved_docs": docs,
    }