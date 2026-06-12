from typing import List

async def retrieve_documents(
    query: str
) -> List[str]:

    # TODO:
    # Replace with Qdrant/Pinecone/etc

    docs = [
        "LangGraph orchestrates agent workflows.",
        "Gemini supports native function calling.",
        "FastAPI enables async AI APIs."
    ]

    return docs