"""Main FastAPI entrypoint for Civic Issue Discovery & Action Engine."""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db, SessionLocal
from app.core.exceptions import (
    CivicEngineError,
    ConfigurationError,
    ProviderError,
    ValidationError,
    PromptInjectionDetectedError,
)
from app.stakeholders.service import StakeholderService
from app.api.v1 import api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle event handler: initializes tables and seeds directory."""
    logger.info("Initializing Civic Engine database...")
    init_db()

    # Pre-seed verified stakeholder directory
    db = SessionLocal()
    try:
        StakeholderService(db)
        logger.info("Verified civic authorities directory verified/seeded.")
    finally:
        db.close()

    yield
    logger.info("Civic Engine shutdown.")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "Production-oriented GenAI engine that discovers civic issues from publicly available sources, "
        "cross-corroborates related reports, detects recurring defects, discovers statutory authorities, "
        "and generates safe, practical civic action and volunteer opportunities."
    ),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global Exception Handlers
@app.exception_handler(ConfigurationError)
async def configuration_error_handler(request: Request, exc: ConfigurationError):
    logger.error(f"Configuration error: {exc}")
    return JSONResponse(
        status_code=503,
        content={
            "error": "ConfigurationError",
            "message": str(exc),
            "hint": "Check your .env settings or switch to AI_PROVIDER=mock for offline development.",
        },
    )


@app.exception_handler(ProviderError)
async def provider_error_handler(request: Request, exc: ProviderError):
    logger.error(f"AI Provider error ({exc.provider}): {exc}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "ProviderError",
            "provider": exc.provider,
            "message": str(exc),
            "retryable": exc.retryable,
        },
    )


@app.exception_handler(PromptInjectionDetectedError)
async def prompt_injection_handler(request: Request, exc: PromptInjectionDetectedError):
    logger.warning(f"Security event - Prompt injection blocked: {exc}")
    return JSONResponse(
        status_code=400,
        content={"error": "SecurityViolation", "message": "Untrusted input contains prohibited prompt injection patterns."},
    )


@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError):
    logger.error(f"Output schema validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"error": "ValidationError", "message": str(exc)},
    )


@app.exception_handler(CivicEngineError)
async def civic_error_handler(request: Request, exc: CivicEngineError):
    return JSONResponse(
        status_code=400,
        content={"error": "CivicEngineError", "message": str(exc)},
    )


# Mount versioned API routes
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", include_in_schema=False)
def root_redirect():
    """Redirect root path to interactive Swagger documentation."""
    return RedirectResponse(url="/docs")
