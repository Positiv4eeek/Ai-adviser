from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.curriculum import router as curriculum_router
from app.api.endpoints.transcript import router as transcript_router
from app.db import Base, engine
from app.utils.auth import get_current_user
from app.models import User

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

@app.get("/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return {
        "first_name": current_user.first_name,
        "last_name":  current_user.last_name,
        "role":       current_user.role.value,
    }
