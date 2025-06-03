import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.api_v1 import api_router
from src.config import settings
from src.core.db.initial_data import seed_data
from src.core.db.session import async_session

root_router = APIRouter()


def get_application() -> FastAPI:
    app = FastAPI(title="Organizations Catalog FastAPI")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router, prefix=settings.API_V1_STR)
    app.include_router(root_router)
    return app


app = get_application()


@app.on_event("startup")
async def startup_event():
    async with async_session() as session:
        await seed_data(session)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, log_level="info")
