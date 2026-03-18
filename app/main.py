from fastapi import FastAPI
import app.models  # noqa: F401 — ensure all models are registered with Base.metadata
from app.api.v1.router import api_router

app = FastAPI(
    title="Справочник организаций",
    description=(
        "REST API для справочника Организаций, Зданий и Деятельностей.\n\n"
        "Все запросы требуют заголовок **X-API-Key**."
    ),
    version="1.0.0",
)

app.include_router(api_router)


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
