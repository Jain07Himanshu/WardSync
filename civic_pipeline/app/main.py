import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import get_settings
from .routes.ingest import router as ingest_router
from .routes.ngos import router as ngos_router
from .routes.events import router as events_router
from .routes.public import router as public_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("civic_pipeline")


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    logger.info("Starting Civic Ingestion, Verification, and NGO Mobilization Pipeline...")
    logger.info("Environment: %s", settings.ENVIRONMENT)
    logger.info("Supabase configured: %s", settings.is_supabase_configured)
    logger.info("Gemini configured: %s", settings.is_gemini_configured)
    logger.info("Similarity Threshold: %.2f | Verification Threshold: %d", 
                settings.SIMILARITY_THRESHOLD, settings.VERIFICATION_THRESHOLD)
    yield
    logger.info("Shutting down Civic Pipeline engine...")


def create_app() -> FastAPI:
    """FastAPI application factory."""
    app = FastAPI(
        title="Civic Ingestion, Verification, and NGO Mobilization Pipeline",
        description=(
            "Production-ready backend engine automating civic signal ingestion, "
            "Gemini 1.5 Flash structured synthesis & credibility scoring, "
            "pgvector text-embedding-004 semantic clustering, and automated NGO volunteer mobilization."
        ),
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Global Exception Handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled error on %s %s: %s", request.method, request.url.path, exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An internal server error occurred.", "error": str(exc)},
        )

    # Health Check
    @app.get("/health", tags=["System"])
    async def health_check():
        settings = get_settings()
        return {
            "status": "healthy",
            "service": "Civic Ingestion, Verification, and NGO Mobilization Pipeline",
            "supabase_live": settings.is_supabase_configured,
            "gemini_live": settings.is_gemini_configured,
            "similarity_threshold": settings.SIMILARITY_THRESHOLD,
            "verification_threshold": settings.VERIFICATION_THRESHOLD,
        }

    # Register Routers
    app.include_router(ingest_router)
    app.include_router(ngos_router)
    app.include_router(events_router)
    app.include_router(public_router)

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
