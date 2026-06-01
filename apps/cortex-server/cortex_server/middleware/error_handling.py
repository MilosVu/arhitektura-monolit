"""Mapiranje CortexError na ErrorResponse JSON."""

from __future__ import annotations

from cortex_core.api_types import ErrorResponse
from cortex_core.errors import (
    ConflictError,
    CortexError,
    ForbiddenError,
    NotAuthenticatedError,
    NotFoundError,
    ValidationError,
)
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundError)
    async def not_found_handler(_request: Request, exc: NotFoundError) -> JSONResponse:
        body = ErrorResponse(status=404, code="not_found", detail=str(exc))
        return JSONResponse(status_code=404, content=body.model_dump())

    @app.exception_handler(ValidationError)
    async def validation_handler(
        _request: Request, exc: ValidationError
    ) -> JSONResponse:
        body = ErrorResponse(status=422, code="validation_error", detail=str(exc))
        return JSONResponse(status_code=422, content=body.model_dump())

    @app.exception_handler(RequestValidationError)
    async def request_validation_handler(
        _request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        body = ErrorResponse(status=422, code="validation_error", detail=str(exc))
        return JSONResponse(status_code=422, content=body.model_dump())

    @app.exception_handler(ConflictError)
    async def conflict_handler(_request: Request, exc: ConflictError) -> JSONResponse:
        body = ErrorResponse(status=409, code="conflict", detail=str(exc))
        return JSONResponse(status_code=409, content=body.model_dump())

    @app.exception_handler(NotAuthenticatedError)
    async def not_authenticated_handler(
        _request: Request, exc: NotAuthenticatedError
    ) -> JSONResponse:
        body = ErrorResponse(status=401, code=exc.code, detail=str(exc))
        return JSONResponse(status_code=401, content=body.model_dump())

    @app.exception_handler(ForbiddenError)
    async def forbidden_handler(_request: Request, exc: ForbiddenError) -> JSONResponse:
        body = ErrorResponse(status=403, code=exc.code, detail=str(exc))
        return JSONResponse(status_code=403, content=body.model_dump())

    @app.exception_handler(CortexError)
    async def cortex_error_handler(_request: Request, exc: CortexError) -> JSONResponse:
        body = ErrorResponse(status=500, code="internal_error", detail=str(exc))
        return JSONResponse(status_code=500, content=body.model_dump())
