from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.presentation.api.routes import include_routers
from app.config.settings import settings

app = FastAPI(title="COLLAB Backend", version="1.0.0")

# Configure CORS based on environment
if settings.cors_origins == "*":
    allow_origins = ["*"]
else:
    allow_origins = [origin.strip() for origin in settings.cors_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
include_routers(app)


@app.get("/")
async def root():
    """Root endpoint for health check"""
    return {"message": "Welcome to COLLAB Backend"}


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
