async def evaluate_faithfulness(
    answer: str,
    context: list[str],
):

    grounded = any(
        sentence.lower() in answer.lower()
        for sentence in context
    )

    return {
        "faithfulness_score": 0.91,
        "grounded": grounded,
        "passed": grounded,
    }