from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from gateway.middleware.jwt import JWTMiddleware
from gateway.middleware.rate_limit import RateLimitMiddleware
from gateway.routers import auth, social, transaction, notification

app = FastAPI(title="Soccho Gateway", version="1.0.0")

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://soccho.vercel.app", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

