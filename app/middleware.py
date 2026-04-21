from __future__ import annotations

import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from structlog.contextvars import bind_contextvars, clear_contextvars


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
<<<<<<< HEAD
        # Clear contextvars to avoid leakage between requests
=======
        # TODO: Clear contextvars to avoid leakage between requests
>>>>>>> dda802208b47e9caba0e1cbb959fe4fedc9861b7
        clear_contextvars()

        # Extract x-request-id from headers or generate a new one
        # Use format: req-<8-char-hex>
<<<<<<< HEAD
        correlation_id = request.headers.get("x-request-id")
        if not correlation_id:
            correlation_id = f"req-{uuid.uuid4().hex[:8]}"
        
        # Bind the correlation_id to structlog contextvars
=======
        request_id = request.headers.get("x-request-id")
        if request_id:
            correlation_id = request_id
        else:
            correlation_id = f"req-{uuid.uuid4().hex[:8]}"
        
        # TODO: Bind the correlation_id to structlog contextvars
>>>>>>> dda802208b47e9caba0e1cbb959fe4fedc9861b7
        bind_contextvars(correlation_id=correlation_id)
        
        request.state.correlation_id = correlation_id
        
        start = time.perf_counter()
        response = await call_next(request)
        
<<<<<<< HEAD
        # Add the correlation_id and processing time to response headers
        response.headers["x-request-id"] = correlation_id
        response.headers["x-response-time-ms"] = str(int((time.perf_counter() - start) * 1000))
        
=======
        # TODO: Add the correlation_id and processing time to response headers
        # response.headers["x-request-id"] = correlation_id
        # response.headers["x-response-time-ms"] = ...
        response.headers["x-request-id"] = correlation_id
        processing_time_ms = int((time.perf_counter() - start) * 1000)
        response.headers["x-response-time-ms"] = str(processing_time_ms)

>>>>>>> dda802208b47e9caba0e1cbb959fe4fedc9861b7
        return response
