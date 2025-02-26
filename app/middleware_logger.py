import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from loguru import logger


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Get or generate a request id
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        # Bind the request id to the logger
        logger_ctx = logger.bind(request_id=request_id, method=request.method, path=request.url.path)
        logger_ctx.info("Request started")
        # Pass the logger context through request.state
        request.state.logger = logger_ctx

        response = await call_next(request)

        logger_ctx.info("Request completed")
        response.headers["X-Request-ID"] = request_id
        return response
