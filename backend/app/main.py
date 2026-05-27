from contextlib import asynccontextmanager
import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.core.config import settings
from app.core.logging import get_logger
from app.schemas.common import error_response

logger = get_logger(__name__)

# Rate limiter — global 100/min; auth/login has its own stricter limit in auth.py
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.core.scheduler import start_scheduler, stop_scheduler
    logger.info("Smart Recruit Platform starting up")
    start_scheduler()
    yield
    stop_scheduler()
    logger.info("Smart Recruit Platform shutting down")


app = FastAPI(
    title="Smart Recruit Platform API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Correlation ID middleware
@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


# Security headers middleware
@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=error_response("An internal server error occurred"),
    )


# Router registration
from app.api.v1 import auth, employees, slots, candidates, bookings, feedback, workflow, joining_bonus, admin, exports, reports, l2, weekend_drive, referral, supply  # noqa: E402

app.include_router(auth.router)
app.include_router(employees.router)
app.include_router(slots.router)
app.include_router(candidates.router)
app.include_router(bookings.router)
app.include_router(feedback.router)
app.include_router(workflow.router)
app.include_router(joining_bonus.router)
app.include_router(admin.router)
app.include_router(exports.router)
app.include_router(reports.router)
app.include_router(l2.router)
app.include_router(weekend_drive.router)
app.include_router(referral.router)
app.include_router(supply.router)


@app.get("/health")
def health():
    return {"status": "ok"}
