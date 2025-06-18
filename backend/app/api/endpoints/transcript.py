from fastapi import APIRouter, UploadFile, File
from app.utils.parser import parse_transcript

router = APIRouter()

@router.post("/upload_transcript")
async def upload_transcript(file: UploadFile = File(...)):
    contents = await file.read()
    with open("temp.pdf", "wb") as f:
        f.write(contents)
    parsed = parse_transcript("temp.pdf")
    return parsed