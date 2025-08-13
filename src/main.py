from fastapi import FastAPI
from src.config import settings, app_configs
from contextlib import asynccontextmanager
from src.logging_config import setup_logging
from fastapi.middleware.cors import CORSMiddleware
from src.router import app_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    yield

app = FastAPI(**app_configs, lifespan=lifespan,)
app.include_router(app_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)

# --- Base Routes
@app.get("/", include_in_schema=False)
async def root() -> dict[str, str]:
    return {
        "message": "Welcome to the Mit Smart Chatbot API! Check out our docs at `/docs`"
    }


@app.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}