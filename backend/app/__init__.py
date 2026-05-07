"""
app/__init__.py
Creates and configures the FastAPI application instance.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router
from .config import settings


def create_app() -> FastAPI:
    """
    Application factory — builds and returns the configured FastAPI instance.
    Keeps startup logic separate from route logic (easier to test).
    """
    app = FastAPI(
        title=settings.APP_NAME,
        description="Upload a video, get back a transcript. Simple as that.",
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # For development only
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register all routes from the routes module
    app.include_router(router)

    return app