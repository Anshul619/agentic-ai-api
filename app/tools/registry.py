from app.tools.retrieval import retrieve_documents
from app.tools.evaluation import evaluate_faithfulness
from app.tools.observability import measure_latency

TOOL_REGISTRY = {
    "retrieve_documents": retrieve_documents,
    "evaluate_faithfulness": evaluate_faithfulness,
    "measure_latency": measure_latency,
}