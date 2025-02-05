# filepath: /home/fiodar/repositories/sarna/sarna/middleware.py
import time
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class TokenBucket:
    def __init__(self, rate: int, capacity: int):
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.timestamp = time.time()

    def consume(self, tokens: int = 1) -> bool:
        current_time = time.time()
        elapsed = current_time - self.timestamp
        self.timestamp = current_time
        self.tokens += elapsed * self.rate
        if self.tokens > self.capacity:
            self.tokens = self.capacity
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False


# Define a logging and rate limiting middleware using token bucket algorithm
class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, rate: int = 1, capacity: int = 5):
        super().__init__(app)
        self.rate = rate
        self.capacity = capacity
        self.clients = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        if client_ip not in self.clients:
            self.clients[client_ip] = TokenBucket(self.rate, self.capacity)

        token_bucket = self.clients[client_ip]
        if not token_bucket.consume():
            return JSONResponse({"detail": "Rate limit exceeded"}, status_code=429)

        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        formatted_process_time = '{0:.2f}'.format(process_time * 1000)
        print(f"Request: {request.method} {request.url} completed in {formatted_process_time}ms")
        print(f"Client IP: {client_ip}, Remaining tokens: {token_bucket.tokens}")
        return response
