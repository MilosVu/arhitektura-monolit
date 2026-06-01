"""Correlation ID middleware."""

from __future__ import annotations

import logging

from cortex_core.correlation import (
    new_correlation_id,
    reset_correlation_id,
    set_correlation_id,
)
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)
_HEADER = "X-Correlation-ID"


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        incoming = request.headers.get(_HEADER)
        cid = incoming or new_correlation_id()
        token = set_correlation_id(cid)
        try:
            response = await call_next(request)
        finally:
            reset_correlation_id(token)
        response.headers[_HEADER] = cid
        logger.debug("request correlation_id=%s path=%s", cid, request.url.path)
        return response
