import time


async def measure_latency(
    workflow,
    payload
):

    start = time.time()

    result = await workflow.ainvoke(payload)

    duration = time.time() - start

    return {

        "duration_seconds": duration,

        "result": result
    }