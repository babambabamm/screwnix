from fastapi import FastAPI


app = FastAPI(
    title="screwnix",
    description="Autonomous Runtime Application Security Platform",
    version="0.1"
)

@app.get("/")
async def root():
    return {"message": "Screwnix is running"}