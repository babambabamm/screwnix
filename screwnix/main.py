from fastapi import FastAPI

from screwnix.proxy.proxy_router import router as proxy_router


app = FastAPI(
    title="screwnix",
    description="Autonomous Runtime Application Security Platform",
    version="0.1"
)

@app.get("/")
async def root():
    return {"message": "Screwnix is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Include proxy router AFTER direct routes so they take precedence
app.include_router(proxy_router)

