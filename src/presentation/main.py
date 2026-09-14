from fastapi import FastAPI

from src.presentation.api.v1.router import api_v1_router

app = FastAPI(
    title="FastAPI Clean Architecture",
    description="Modular Clean Architecture template built with FastAPI, SQLAlchemy 2.0, and Pydantic.",  # noqa: E501
    version="1.0.0",
)

app.include_router(api_v1_router)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}