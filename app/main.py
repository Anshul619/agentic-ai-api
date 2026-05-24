from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
#from app.api.rag import router as rag_router
from app.core.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup logic
    print("Starting agentic-ai-api...")

    yield

    # Shutdown logic
    print("Shutting down agentic-ai-api...")


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan=lifespan
)

# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# Routers
# ==========================================

app.include_router(
    chat_router,
    prefix="/api/v1"
)

# app.include_router(
#     rag_router,
#     prefix="/api/v1"
# )

# ==========================================
# Health Check
# ==========================================

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "service": settings.APP_NAME
    }


@app.get("/")
async def root():

    return {
        "message": "agentic-ai-api running"
    }