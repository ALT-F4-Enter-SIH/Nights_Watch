"""ShadowLink AI — FastAPI entry point."""
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from config import settings
from database import init_db
from routers import api_router


app = FastAPI(
    title=settings.app_name,
    description="AI-Powered Threat Intelligence & Identity Correlation Platform",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event() -> None:
    init_db()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": "Validation failed",
            "detail": exc.errors(),
            "status_code": 422,
        },
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "Database error",
            "detail": str(exc),
            "status_code": 500,
        },
    )


@app.get("/", tags=["health"])
async def root() -> dict:
    return {
        "message": "ShadowLink AI",
        "version": settings.app_version,
        "description": "AI-Powered Threat Intelligence & Identity Correlation Platform",
        "docs": "/docs",
    }


@app.get("/health", tags=["health"])
async def health_check() -> dict:
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
    }


app.include_router(api_router)
