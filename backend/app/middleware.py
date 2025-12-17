import time
import logging
from fastapi import Request, Response, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.types import ASGIApp
from app.core.config import settings

logger = logging.getLogger(__name__)

class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPException as http_exc:
            return JSONResponse(
                status_code=http_exc.status_code,
                content={"detail": http_exc.detail},
                headers=http_exc.headers,
            )
        except Exception as e:
            logger.exception("Internal Server Error: %s", e)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "An internal server error occurred."},
            )

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        
        log_message = f"Request: {request.method} {request.url} - Status: {response.status_code} - Completed in {process_time:.4f}s"
        
        # Try to get user ID if authenticated
        try:
            from app.dependencies import get_current_user_from_request_if_exists
            user = await get_current_user_from_request_if_exists(request)
            if user:
                log_message += f" - User ID: {user.id}"
        except Exception:
            pass # Ignore if user can't be retrieved (e.g., public endpoint)

        client_ip = request.client.host if request.client else "unknown"
        log_message += f" - Client IP: {client_ip}"
        
        logger.info(log_message)
        return response

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        # Only add HSTS if served over HTTPS. FastAPI's default is HTTP for local dev.
        # For production, ensure this is set only if behind a HTTPS-terminating proxy.
        # response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response