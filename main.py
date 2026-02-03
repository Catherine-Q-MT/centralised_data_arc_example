from fastapi import FastAPI
from routes import router

app = FastAPI(
    title="Centralized Data Architecture Example",
    description="A mock FastAPI application demonstrating a centralized data architecture.",
    version="1.0.0",
)

app.include_router(router, prefix="/api")

@app.get("/", summary="Root endpoint")
async def root():
    return {"message": "Welcome to the Centralized Data Architecture API!"}
