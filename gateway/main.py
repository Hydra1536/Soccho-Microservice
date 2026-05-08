from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from gateway.middleware.jwt import JWTMiddleware
from gateway.middleware.rate_limit import RateLimitMiddleware
from gateway.middleware.security_headers import SecurityHeadersMiddleware
from gateway.routers import auth, social, transaction, notification

app = FastAPI(
    title="Soccho Gateway",
    version="1.0.0",
    docs_url="/api/docs",  # Hide from root
    openapi_url="/api/openapi.json",
)

# Middleware stack (order matters - outer to inner)
app.add_middleware(SecurityHeadersMiddleware)  # Apply security headers to all responses
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://soccho.vercel.app", "https://www.soccho.vercel.app", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count", "X-Page-Number"],
    max_age=3600,
)
app.add_middleware(JWTMiddleware)
app.add_middleware(RateLimitMiddleware)

# Routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(social.router, prefix="/social", tags=["social"])
app.include_router(transaction.router, prefix="/transactions", tags=["transactions"])
app.include_router(notification.router, prefix="/notifications", tags=["notifications"])

# Health check
@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

