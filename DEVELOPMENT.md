# Development Guide

This document provides guidelines for developing and contributing to FastAPI Kit.

## Setup Development Environment

1. **Clone the repository**
   ```bash
   git clone https://github.com/bestend/fastapi-kit.git
   cd fastapi-kit
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install in development mode**
   ```bash
   pip install -e ".[dev]"
   ```

## Development Workflow

### Code Quality

We use several tools to maintain code quality:

- **Ruff**: For linting and formatting
- **MyPy**: For type checking
- **Pytest**: For testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=fastapi_kit --cov-report=html

# Run specific test file
pytest tests/test_app.py

# Run with verbose output
pytest tests/ -v
```

### Code Formatting

```bash
# Format code with ruff
ruff format src/ tests/

# Check formatting without changing files
ruff format --check src/ tests/
```

### Linting

```bash
# Lint code with ruff
ruff check src/ tests/

# Auto-fix issues
ruff check --fix src/ tests/
```

### Type Checking

```bash
# Type check with mypy
mypy src/
```

## Project Structure

```
fastapi-kit/
├── .github/
│   └── workflows/          # GitHub Actions workflows
│       ├── tests.yml       # CI tests
│       └── publish.yml     # PyPI publishing
├── src/
│   └── fastapi_kit/
│       ├── __init__.py     # Public API exports
│       ├── base.py         # create_app function
│       ├── logging_api_route.py  # Custom APIRoute
│       ├── logging_utils.py      # Logging configuration
│       ├── exception/      # Exception handling
│       ├── log/            # Logging utilities
│       ├── type/           # Type definitions
│       └── util/           # Utility functions
├── tests/                  # Test files
├── pyproject.toml          # Project metadata and dependencies
├── ruff.toml              # Ruff configuration
└── README.md              # Documentation
```

## Making Changes

1. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write code following the existing style
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**
   ```bash
   # Run all checks
   ruff check src/ tests/
   ruff format --check src/ tests/
   mypy src/
   pytest tests/
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

   We follow [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `style:` - Code style changes (formatting, etc.)
   - `refactor:` - Code refactoring
   - `test:` - Test changes
   - `chore:` - Build process or tooling changes

5. **Push and create a Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Release Process

Releases are automated via GitHub Actions:

1. **Update CHANGELOG.md** with the new version changes

2. **Create and push a version tag**
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

3. **GitHub Actions will automatically:**
   - Update version in `pyproject.toml`
   - Build the package
   - Publish to PyPI
   - Create a GitHub Release

## Code Style Guidelines

### Python Style

- Follow PEP 8 with line length of 100 characters
- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes
- Use descriptive variable names

### Example

```python
def create_app(
    api_list: list[APIRouter],
    title: str = "",
    version: str = "",
) -> FastAPI:
    """Create a FastAPI application with pre-configured features.

    Args:
        api_list: List of FastAPI APIRouter instances to include
        title: API title for documentation
        version: API version string

    Returns:
        Configured FastAPI application instance
    """
    # Implementation here
    pass
```

### Import Order

1. Standard library imports
2. Third-party imports
3. Local application imports

Example:
```python
import os
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from fastapi_kit.exception import ErrorInfo
from fastapi_kit.log import get_logger
```

## Testing Guidelines

### Test Structure

- Place tests in the `tests/` directory
- Name test files as `test_*.py`
- Name test functions as `test_*`
- Use fixtures for common setup

### Writing Tests

```python
def test_create_app_basic(simple_router):
    """Test basic app creation."""
    app = create_app(
        [simple_router],
        title="Test API",
        version="1.0.0",
    )

    assert app.title == "Test API"
    assert app.version == "1.0.0"
```

## Documentation

- Update README.md for user-facing changes
- Update CHANGELOG.md for all changes
- Add docstrings to all public APIs
- Include code examples in docstrings

## Questions or Issues?

- Open an issue on GitHub
- Reach out to maintainers

Thank you for contributing to FastAPI Kit! 🚀

