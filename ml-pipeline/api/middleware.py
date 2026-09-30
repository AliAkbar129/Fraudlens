from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
from loguru import logger
import collections

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.4f}s")
        return response

class LatencyTrackingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.latencies = collections.deque(maxlen=1000)
        
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        self.latencies.append(time.time() - start_time)
        return response

class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/predict") or request.url.path.startswith("/explain"):
            api_key = request.headers.get("X-API-Key")
            if not api_key or api_key != "fraudlens-secret-key":
                from fastapi.responses import JSONResponse
                return JSONResponse(status_code=401, content={"detail": "Invalid API Key"})
        return await call_next(request)

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute=600):
        super().__init__(app)
        self.limit = requests_per_minute
        self.tokens = self.limit
        self.last_update = time.time()
        
    async def dispatch(self, request: Request, call_next):
        now = time.time()
        time_passed = now - self.last_update
        self.tokens = min(self.limit, self.tokens + time_passed * (self.limit / 60.0))
        self.last_update = now
        
        if self.tokens < 1:
            from fastapi.responses import JSONResponse
            return JSONResponse(status_code=429, content={"detail": "Too Many Requests"})
            
        self.tokens -= 1
        return await call_next(request)
