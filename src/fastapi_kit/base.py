import asyncio
import logging
import os
from collections.abc import Callable
from contextlib import asynccontextmanager

from fastapi import APIRouter, Depends, FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse, Response

from fastapi_kit.exception.handler import add_exception_handler
from fastapi_kit.log import get_logger
from fastapi_kit.logging_utils import setup_logging

logger = get_logger()


def create_app(
    api_list: list[APIRouter],
    title: str = "",
    version: str = "",
    prefix_url: str = "",
    graceful_timeout: int = 10,
    dependencies: list[Depends] | None = None,
    middlewares: list | None = None,
    startup_coroutines: list[Callable] | None = None,
    shutdown_coroutines: list[Callable] | None = None,
    health_check_api: str = "/healthz",
    metrics_api: str = "/metrics",
    docs_enable: bool = True,
    docs_prefix_url: str = "",
    add_external_basic_auth: bool = False,
    stage: str = "dev",
) -> FastAPI:
    """Create a FastAPI application with pre-configured features.

    This function creates a production-ready FastAPI app with:
    - Automatic request/response logging with trace IDs
    - Centralized exception handling
    - Health check endpoint
    - CORS middleware
    - Auto-generated API documentation
    - Graceful shutdown support

    Args:
        api_list: List of FastAPI APIRouter instances to include
        title: API title for documentation
        version: API version string
        prefix_url: URL prefix for all API routes (e.g., "/api/v1")
        graceful_timeout: Seconds to wait during graceful shutdown (default: 10)
        dependencies: List of FastAPI dependencies to apply globally
        middlewares: List of Starlette middleware classes to add
        startup_coroutines: List of async functions to run on app startup
        shutdown_coroutines: List of async functions to run on app shutdown
        health_check_api: Path for health check endpoint (default: "/healthz")
        metrics_api: Path for metrics endpoint (default: "/metrics")
        docs_enable: Enable automatic API documentation (default: True)
        docs_prefix_url: URL prefix for docs (defaults to prefix_url)
        add_external_basic_auth: Add bearer auth to OpenAPI schema (default: False)
        stage: Environment stage - "dev", "staging", or "prod" (default: "dev")

    Returns:
        Configured FastAPI application instance

    Example:
        ```python
        from fastapi import APIRouter
        from fastapi_kit import create_app, LoggingAPIRoute

        router = APIRouter(route_class=LoggingAPIRoute)

        @router.get("/hello")
        async def hello():
            return {"message": "Hello, World!"}

        app = create_app(
            [router],
            title="My API",
            version="1.0.0",
            prefix_url="/api/v1",
            stage="prod"
        )
        ```
    """
    if dependencies is None:
        dependencies = []
    if middlewares is None:
        middlewares = []
    if startup_coroutines is None:
        startup_coroutines = []
    if shutdown_coroutines is None:
        shutdown_coroutines = []

    if docs_prefix_url == "":
        docs_prefix_url = prefix_url

    # constants
    docs_api = f"{docs_prefix_url}/docs"
    redoc_api = f"{docs_prefix_url}/redoc"
    openapi_api = f"{docs_prefix_url}/openapi.json"

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        loggers = (
            logging.getLogger(name)
            for name in logging.root.manager.loggerDict
            if name.startswith("uvicorn.") or name.startswith("fastapi.")
        )
        for logger in loggers:
            logger.handlers = []

        # logging
        setup_logging()

        for coroutine in startup_coroutines:
            await coroutine(app)

        yield

        # graceful shutdown
        await asyncio.sleep(graceful_timeout)
        for coroutine in shutdown_coroutines:
            await coroutine(app)

    app = FastAPI(
        title=title,
        version=version,
        openapi_url="",
        docs_url="",
        redoc_url="",
        lifespan=lifespan,
    )

    for api in api_list:
        app.include_router(api, dependencies=dependencies, prefix=prefix_url)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    add_exception_handler(app, stage)
    for middleware in middlewares:
        app.add_middleware(middleware)

    @app.get(health_check_api, include_in_schema=False)
    async def healthcheck():
        return Response(content="OK", media_type="text/plain")

    if docs_enable:
        if docs_prefix_url:

            @app.get(docs_prefix_url, include_in_schema=False)
            async def docs():
                return RedirectResponse(docs_api)
        else:

            @app.get("/", include_in_schema=False)
            async def docs():
                return RedirectResponse(docs_api)

        @app.get(docs_api, include_in_schema=False)
        async def custom_swagger_ui_html():
            return get_swagger_ui_html(
                openapi_url="openapi.json",
                title=app.title + " - Swagger UI",
                oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            )

        @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
        async def swagger_ui_redirect():
            return get_swagger_ui_oauth2_redirect_html()

        @app.get(redoc_api, include_in_schema=False)
        async def redoc_html():
            return get_redoc_html(
                openapi_url="openapi.json",
                title=app.title + " - ReDoc",
            )

        raw_openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            routes=app.routes,
            tags=app.openapi_tags,
            servers=app.servers,
        )
        if add_external_basic_auth:
            if "components" in raw_openapi_schema:
                raw_openapi_schema["components"]["securitySchemes"] = {
                    "bearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT",
                    }
                }
            raw_openapi_schema["security"] = [{"bearerAuth": []}]

        @app.get(openapi_api, include_in_schema=False)
        async def openapi_json(request: Request):
            if "X-Origin-Path" in request.headers:
                openapi_schema = dict(raw_openapi_schema)
                old_pattern = os.path.dirname(request.url.path)
                new_pattern = request.headers["X-Origin-Path"]
                new_paths = {}
                for k, v in openapi_schema["paths"].items():
                    new_paths[k.replace(old_pattern, new_pattern)] = v
                openapi_schema["paths"] = new_paths
            else:
                openapi_schema = raw_openapi_schema
            return JSONResponse(openapi_schema)

    return app
