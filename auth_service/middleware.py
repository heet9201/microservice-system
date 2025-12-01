import time
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
from datetime import datetime, timedelta
from config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        execution_time = time.time() - start_time
        logger.info(
            f"Path: {request.url.path} | Method: {request.method} | "
            f"Execution Time: {execution_time:.4f}s"
        )
        
        return response


class SecurityMiddleware(BaseHTTPMiddleware):
    
    def __init__(self, app):
        super().__init__(app)
        self.rate_limit_data = defaultdict(list)
    
    async def dispatch(self, request: Request, call_next):
        # Rate limiting
        if settings.ENABLE_RATE_LIMIT:
            client_ip = request.client.host
            now = datetime.now()
            
            # Clean old entries
            self.rate_limit_data[client_ip] = [
                timestamp for timestamp in self.rate_limit_data[client_ip]
                if now - timestamp < timedelta(seconds=settings.RATE_LIMIT_WINDOW)
            ]
            
            # Check rate limit
            if len(self.rate_limit_data[client_ip]) >= settings.RATE_LIMIT_REQUESTS:
                raise HTTPException(
                    status_code=429,
                    detail=f"Rate limit exceeded. Max {settings.RATE_LIMIT_REQUESTS} requests per {settings.RATE_LIMIT_WINDOW} seconds"
                )
            
            # Add current request
            self.rate_limit_data[client_ip].append(now)
        
        response = await call_next(request)
        return response
