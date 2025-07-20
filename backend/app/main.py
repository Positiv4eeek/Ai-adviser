from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.curriculum import router as curriculum_router
from app.api.endpoints.transcript import router as transcript_router
from app.api.endpoints.user import router as user_router
from app.api.endpoints.ai import router as ai_router
from app.api.endpoints.prompts import router as prompts_router
from app.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    docs_url='/docs',
    redoc_url='/redoc',
    openapi_url='/openapi.json',
)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

app.include_router(curriculum_router)

app.include_router(transcript_router)

app.include_router(user_router)

app.include_router(ai_router)

app.include_router(prompts_router)