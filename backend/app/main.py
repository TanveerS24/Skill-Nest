from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import init_db
from app.redis_client import init_redis, close_redis
from app.middleware import RateLimitMiddleware
from app.routes import auth, problems, submissions, leaderboard, admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    await init_redis()
    yield
    # Shutdown
    await close_redis()


app = FastAPI(
    title="SkillNest - Coding Platform API",
    description="Multi-language coding platform with Docker sandbox execution",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # SvelteKit dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting
app.add_middleware(RateLimitMiddleware)

# Include routers
app.include_router(auth.router)
app.include_router(problems.router)
app.include_router(submissions.router)
app.include_router(leaderboard.router)
app.include_router(admin.router)


@app.get("/")
async def root():
    return {
        "message": "SkillNest API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
