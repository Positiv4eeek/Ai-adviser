from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.parser import parse_curriculum
import tempfile

router = APIRouter()

@router.post("/upload-curriculum")
async def upload_curriculum(file: UploadFile = File(...)):
    suffix = file.filename.lower().endswith('.csv') and '.csv' or '.xlsx'
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(await file.read()); tmp.close()
    try:
        res = parse_curriculum(tmp.name)
    except Exception as e:
        raise HTTPException(400, str(e))
    return res