import time

async def measure_latency(
    start_time: float
):

    latency = round(
        time.time() - start_time,
        2
    )

    return {
        "latency_seconds": latency
    }