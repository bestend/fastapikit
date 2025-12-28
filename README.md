<p align="center">
  <h1 align="center">🚀 FastAPI Kit</h1>
</p>

<div align="center">

**Production-ready FastAPI boilerplate with batteries included**

**Language:** [한국어](./README.ko.md) | English

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/status-alpha-yellow)](https://github.com/bestend/fastapi-kit)
[![Tests](https://github.com/bestend/fastapi-kit/actions/workflows/tests.yml/badge.svg)](https://github.com/bestend/fastapi-kit/actions/workflows/tests.yml)

</div>

---

## ✨ Overview

**FastAPI Kit** is a production-ready FastAPI boilerplate that includes everything you need to build robust APIs quickly. It provides pre-configured logging, error handling, request/response tracking, and more out of the box.

Stop writing the same boilerplate code for every FastAPI project. Start building features immediately with FastAPI Kit.

---

## 🎯 Key Features

- **📝 Smart Logging** — Structured logging with Loguru, request/response tracking, and trace IDs
- **🛡️ Exception Handling** — Centralized error handling with customizable error responses
- **🔍 Request Tracing** — OpenTelemetry integration with automatic trace ID propagation
- **🎨 Custom API Route** — Enhanced APIRoute with automatic request/response logging
- **⚡️ Type Safety** — Pydantic V2 integration for robust data validation
- **🏥 Health Checks** — Built-in health check endpoint
- **📚 Auto Documentation** — Automatic OpenAPI/Swagger UI generation
- **🔧 Highly Configurable** — Customize logging, CORS, middleware, and more
- **🚀 Production Ready** — Graceful shutdown, environment-based configuration

---

## 📦 Installation

```bash
pip install fastapi-kit
```

---

## 🚀 Quick Start

### Basic Usage

```python
from fastapi import APIRouter
from fastapi_kit import create_app, LoggingAPIRoute

# Create your API router
router = APIRouter(route_class=LoggingAPIRoute)

@router.get("/hello")
async def hello():
    return {"message": "Hello, World!"}

# Create the app with minimal configuration
app = create_app(
    [router],
    title="My API",
    version="1.0.0",
)
```

### Run the app

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### With Full Configuration

```python
from fastapi import APIRouter, Depends
from fastapi_kit import create_app, LoggingAPIRoute, get_logger

logger = get_logger()

router = APIRouter(route_class=LoggingAPIRoute)

@router.get("/api/hello")
async def hello():
    logger.info("Hello endpoint called")
    return {"message": "Hello, World!"}

async def startup_handler(app):
    logger.info("Application starting up...")
    # Initialize database, connections, etc.

async def shutdown_handler(app):
    logger.info("Application shutting down...")
    # Cleanup resources

app = create_app(
    api_list=[router],
    title="My Production API",
    version="1.0.0",
    prefix_url="/api/v1",
    graceful_timeout=10,
    docs_enable=True,
    docs_prefix_url="/api/v1",
    health_check_api="/healthz",
    startup_coroutines=[startup_handler],
    shutdown_coroutines=[shutdown_handler],
    stage="prod",  # dev, staging, prod
)
```

---

## 📖 Core Components

### 1. `create_app()`

The main function to create a FastAPI application with all features enabled.

**Parameters:**
- `api_list`: List of APIRouter instances
- `title`: API title
- `version`: API version
- `prefix_url`: URL prefix for all routes
- `graceful_timeout`: Seconds to wait before shutdown (default: 10)
- `docs_enable`: Enable/disable API documentation (default: True)
- `health_check_api`: Health check endpoint path (default: "/healthz")
- `startup_coroutines`: List of async functions to run on startup
- `shutdown_coroutines`: List of async functions to run on shutdown
- `stage`: Environment stage (dev/staging/prod)

### 2. `LoggingAPIRoute`

Enhanced APIRoute class that automatically logs all requests and responses with trace IDs.

```python
from fastapi import APIRouter
from fastapi_kit import LoggingAPIRoute

router = APIRouter(route_class=LoggingAPIRoute)
```

### 3. `get_logger()`

Get a pre-configured Loguru logger instance.

```python
from fastapi_kit import get_logger

logger = get_logger()
logger.info("Application started")
logger.error("Something went wrong")
```

### 4. `BaseModel`

Enhanced Pydantic BaseModel with sensible defaults.

```python
from fastapi_kit import BaseModel

class UserRequest(BaseModel):
    name: str
    email: str
    age: int = 0
```

### 5. Exception Handling

Automatic exception handling with customizable error responses.

```python
from fastapi_kit.exception import BadRequestHeaderError, InvalidAccessTokenError

# Raise custom exceptions
raise BadRequestHeaderError("Invalid header format")
raise InvalidAccessTokenError("Token expired")
```

---

## 🔧 Environment Variables

Configure the application using environment variables:

```bash
# Logging
export LOG_LEVEL=INFO              # DEBUG, INFO, WARNING, ERROR, CRITICAL
export LOG_JSON=false              # true for JSON logs, false for pretty logs
export LOG_STRING_LENGTH=5000      # Max length of logged strings

# Application
export CONFIG_FILE=config.yaml     # Configuration file path
```

---

## 📝 Logging Features

FastAPI Kit includes advanced logging capabilities:

- **Structured Logging**: JSON or pretty-formatted logs
- **Request/Response Logging**: Automatic logging of all API calls
- **Trace ID Propagation**: Track requests across services with OpenTelemetry
- **Context Binding**: Attach contextual information to log entries
- **Log Truncation**: Automatically truncate long log messages
- **Standard Library Integration**: Captures logs from uvicorn, fastapi, and other libraries

Example log output:
```
2024-12-28 22:30:15.123 | INFO  | app.py:main:42 | request | abc123def | GET | /api/v1/users | {"query": "active"}
2024-12-28 22:30:15.234 | INFO  | app.py:main:42 | response | abc123def | GET | /api/v1/users | 200 | {"users": [...]}
```

---

## 🎨 Example Application

See `example.py` for a complete example with:
- Configuration management
- Service initialization
- Dependency injection
- Custom middleware
- Startup/shutdown handlers

---

## 🧪 Testing

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run with coverage
pytest tests/ --cov=fastapi_kit --cov-report=html
```

---

## 🛠️ Development

```bash
# Clone the repository
git clone https://github.com/bestend/fastapi-kit.git
cd fastapi-kit

# Install in development mode
pip install -e ".[dev]"

# Run linting
ruff check src/ tests/

# Format code
ruff format src/ tests/

# Type checking
mypy src/
```

---

## 📚 Advanced Usage

### Custom Exception Handlers

```python
from fastapi_kit.exception import ErrorInfo, get_exception_definitions

# Add custom exception
class CustomError(Exception):
    pass

# Register custom error info
get_exception_definitions()[CustomError] = ErrorInfo(
    status_code=400,
    msg="Custom error occurred",
    log_level="warning"
)
```

### Custom Middleware

```python
from starlette.middleware.base import BaseHTTPMiddleware

class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Pre-processing
        response = await call_next(request)
        # Post-processing
        return response

app = create_app(
    [router],
    middlewares=[CustomMiddleware]
)
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Inspired by [confee](https://github.com/bestend/confee) - Configuration management done right
- Built with [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework
- Logging powered by [Loguru](https://github.com/Delgan/loguru) - Python logging made simple

---

<div align="center">

**Made with ❤️ by [@bestend](https://github.com/bestend)**

If this project helped you, please give it a ⭐️!

</div>

