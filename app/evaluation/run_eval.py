import asyncio
import json

from app.workflows.chat_workflow import graph

from app.evaluation.metrics.latency import (
    measure_latency
)

from app.evaluation.metrics.token_usage import (
    estimate_tokens
)


async def evaluate():

    with open(
        "app/evaluation/datasets/chat_eval.json"
    ) as f:

        dataset = json.load(f)

    results = []

    for item in dataset:

        payload = {

            "session_id": "eval-user",

            "user_input": item["question"],

            "messages": [],

            "memories": []
        }

        latency_result = await measure_latency(
            graph,
            payload
        )

        response = latency_result[
            "result"
        ]["response"]

        token_count = estimate_tokens(
            response
        )

        passed = all(

            keyword.lower() in response.lower()

            for keyword in item[
                "expected_keywords"
            ]
        )

        results.append({

            "question": item["question"],

            "response": response,

            "passed": passed,

            "latency_seconds":
                latency_result[
                    "duration_seconds"
                ],

            "token_count": token_count
        })

    return results


if __name__ == "__main__":

    results = asyncio.run(
        evaluate()
    )

    for r in results:

        print("\n================")
        print(r)