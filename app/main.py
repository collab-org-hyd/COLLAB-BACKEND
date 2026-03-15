from fastapi import FastAPI

app = FastAPI(title="COLLAB Backend", version="1.0.0")


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
