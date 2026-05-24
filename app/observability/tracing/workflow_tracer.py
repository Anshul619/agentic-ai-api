import time
import uuid
import traceback


class WorkflowTracer:

    async def trace_node(
        self,
        node_name,
        fn,
        state
    ):

        trace_id = str(uuid.uuid4())

        start = time.time()

        print(f"\n[TRACE START]")
        print({
            "trace_id": trace_id,
            "node": node_name
        })
        

        try:

            result = await fn(state)

            token_count = len(
                str(result).split()
            )
                        
            duration = (
                time.time() - start
            )

            print(f"[TRACE SUCCESS]")

            print({
                "trace_id": trace_id,
                "node": node_name,
                "duration_seconds":
                    round(duration, 3),
                "status": "success",
                "token_count": token_count
            })

            return result

        except Exception as e:

            duration = (
                time.time() - start
            )

            print(f"[TRACE ERROR]")

            print({
                "trace_id": trace_id,
                "node": node_name,
                "duration_seconds":
                    round(duration, 3),
                "status": "error",
                "error": str(e),
                "stacktrace":
                    traceback.format_exc()
            })

            raise