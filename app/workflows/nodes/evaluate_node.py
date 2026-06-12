from app.tools.evaluation import (
    evaluate_faithfulness,
)


async def evaluate_node(state):

    evaluation = (
        await evaluate_faithfulness(
            answer=state["response"],
            context=state["retrieved_docs"],
        )
    )

    return {
        "evaluation": evaluation,
    }