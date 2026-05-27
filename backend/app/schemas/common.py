from __future__ import annotations
from typing import Generic, TypeVar, Any

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    data: T | None = None
    error: str | None = None
    status: str  # "success" | "error"


def success_response(data: Any) -> dict:
    return {"data": data, "error": None, "status": "success"}


def error_response(message: str) -> dict:
    return {"data": None, "error": message, "status": "error"}
