import functools

from fastapi.exceptions import HTTPException, RequestValidationError
from starlette import status

from fastapi_kit.exception.error_info import ErrorInfo
from fastapi_kit.exception.type import BadRequestHeaderError, InvalidAccessTokenError


@functools.lru_cache
def get_exception_definitions():
    return {
        RequestValidationError: ErrorInfo(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            msg="bad request",
            log_level="warning",
        ),
        BadRequestHeaderError: ErrorInfo(
            status_code=status.HTTP_400_BAD_REQUEST,
            msg="invalid request header",
            log_level="warning",
        ),
        TimeoutError: ErrorInfo(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT, msg="request timeout", log_level="error"
        ),
        RuntimeError: ErrorInfo(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            msg="internal server error",
            log_level="error",
        ),
        Exception: ErrorInfo(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            msg="internal server error",
            log_level="error",
        ),
        InvalidAccessTokenError: ErrorInfo(
            status_code=status.HTTP_401_UNAUTHORIZED,
            msg="invalid access token",
            log_level="warning",
        ),
        HTTPException: ErrorInfo(
            status_code=status.HTTP_400_BAD_REQUEST, msg="bad request", log_level="warning"
        ),
    }
