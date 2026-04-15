from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

from app.routes import health, questions, execution
from app.db.init_db import init_db
from app.core.logging import logger
from app.core.config import get_settings

settings = get_settings()


def create_application() -> FastAPI:
    app = FastAPI(
        title="AI Service - RAG DSA Engine",
        description="FastAPI microservice for RAG-based DSA question generation and code execution",
        version="1.0.0",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time

        logger.info(
            f"{request.method} {request.url.path} - {response.status_code} - {duration:.3f}s"
        )
        return response

    # Exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

    # Include routers
    app.include_router(health.router)
    app.include_router(questions.router)
    app.include_router(execution.router)

    @app.on_event("startup")
    async def startup_event():
        logger.info("Initializing database...")
        init_db()
        logger.info("Database initialized")

    @app.get("/")
    async def root():
        return {
            "service": "AI RAG DSA Engine",
            "version": "1.0.0",
            "status": "running"
        }

    return app


app = create_application()
