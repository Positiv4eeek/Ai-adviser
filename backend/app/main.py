import os
import tempfile
import math

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from app.utils.parser import parse_transcript
from app.utils.parse_curriculum import parse_curriculum
from app.api.endpoints.auth import router as auth_router
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

app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-transcript")
async def upload_transcript(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        parsed = parse_transcript(tmp_path)
        return parsed
    finally:
        os.unlink(tmp_path)

@app.post("/upload-curriculum")
async def upload_curriculum(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    ext = os.path.splitext(file.filename)[1].lower() or ".xlsx"
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
    try:
        content = await file.read()
        tmp.write(content)
        tmp.close()
        curriculum = parse_curriculum(tmp.name)
        return _sanitize(curriculum)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        try:
            os.unlink(tmp.name)
        except:
            pass

@app.get("/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return {
        "first_name": current_user.first_name,
        "last_name":  current_user.last_name,
        "role":       current_user.role.value,
    }

def _sanitize(obj):
    if isinstance(obj, float) and math.isnan(obj):
        return None
    if isinstance(obj, dict):
        return {k: _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize(v) for v in obj]
    return obj
