from pydantic import Field

from fastapi_kit.type import BaseModel


class ErrorInfo(BaseModel):
    response_id: str = Field(default="response_id", alias="id")
    status_code: int = 500
    msg: str = "Internal Server Error"
    detail: str = ""
    log_level: str = "error"
