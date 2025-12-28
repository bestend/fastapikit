import functools
import json
import traceback

from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from fastapi_kit.exception import ErrorInfo
from fastapi_kit.exception.definition import get_exception_definitions
from fastapi_kit.log import get_logger
from fastapi_kit.util import get_trace_id

logger = get_logger()


def exception_message(e: Exception) -> str:
    return f"{type(e).__name__}: {e!s}"


def error_to_json(obj):
    if isinstance(obj, ValueError):
        return str(obj)
    return obj


async def _generate_error_response_core(
    error_info: ErrorInfo, exc: Exception, do_error_log_detail: bool = True
):
    getattr(logger.opt(exception=exc), error_info.log_level)(str(exc))

    if isinstance(exc, HTTPException):
        content = {"msg": exc.detail}
        status_code = exc.status_code
    else:
        content = {
            "msg": error_info.msg,
        }
        status_code = error_info.status_code
        if do_error_log_detail:
            if isinstance(exc, RequestValidationError):
                error_json = json.dumps(exc.errors(), default=error_to_json)
                error_dict = json.loads(error_json)
                content["detail"] = error_dict
                logger.error(error_dict)
            else:
                content["detail"] = exception_message(exc)
                logger.error(traceback.format_exc())

    return JSONResponse(
        headers={"x-trace-id": get_trace_id()}, status_code=status_code, content=content
    )


@functools.lru_cache
def get_responses_for_exception():
    responses = {}
    for _exception, error_info in get_exception_definitions().items():
        responses[error_info.status_code] = {
            "description": error_info.msg,
            "content": {"application/json": {"example": error_info}},
        }
    return responses


def add_exception_handler(app: FastAPI, stage: str):
    do_error_log_detail = stage != "prod"

    exception_definitions = get_exception_definitions()

    for exception, error_info in exception_definitions.items():

        @app.exception_handler(exception)
        async def unicorn_exception_handler(
            request: Request, exc: Exception, error_info=error_info
        ):
            return await _generate_error_response_core(error_info, exc, do_error_log_detail)


async def generate_error_response(exc: Exception, stage: str = "dev"):
    do_error_log_detail = stage != "prod"

    exception_definitions = get_exception_definitions()
    error_info = exception_definitions[Exception]
    for exception, cur_error_info in exception_definitions.items():
        if type(exc) is Exception:
            continue
        if type(exc) is exception:
            error_info = cur_error_info
            break

    return await _generate_error_response_core(error_info, exc, do_error_log_detail)
