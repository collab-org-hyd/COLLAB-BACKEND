from fastapi import FastAPI
from app.presentation.api.routes import include_routers

app = FastAPI(title="COLLAB Backend", version="1.0.0")

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
