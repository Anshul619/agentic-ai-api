from fastapi import APIRouter

router = APIRouter()


@router.get("/eval/health")

async def eval_health():

    return {
        "evaluation": "ready"
    }