"""Simple example of using FastAPI Kit.

This example shows the basic usage of FastAPI Kit with minimal configuration.
"""

import uvicorn
from fastapi import APIRouter

from fastapi_kit import LoggingAPIRoute, create_app, get_logger

# Create logger
logger = get_logger()

# Create API router with automatic logging
router = APIRouter(route_class=LoggingAPIRoute, prefix="/api", tags=["demo"])


@router.get("/hello")
async def hello(name: str = "World"):
    """Say hello."""
    logger.info(f"Hello endpoint called with name: {name}")
    return {"message": f"Hello, {name}!"}


@router.get("/users/{user_id}")
async def get_user(user_id: int):
    """Get user by ID."""
    logger.info(f"Fetching user {user_id}")
    return {"user_id": user_id, "name": "John Doe", "email": "john@example.com"}


@router.post("/users")
async def create_user(name: str, email: str):
    """Create a new user."""
    logger.info(f"Creating user: {name}")
    return {"id": 1, "name": name, "email": email, "created": True}


# Create FastAPI app with all features
app = create_app(
    api_list=[router],
    title="FastAPI Kit Demo",
    version="1.0.0",
    prefix_url="/v1",
    docs_enable=True,
    health_check_api="/healthz",
    stage="dev",  # dev, staging, or prod
)

if __name__ == "__main__":
    # Run with uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )

