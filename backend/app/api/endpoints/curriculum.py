from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status
from sqlalchemy.orm import Session
import tempfile, os, math

from app.db import get_db
from app.models import Curriculum, Course, Elective
from app.utils.parse_curriculum import parse_curriculum
from app.utils.auth import require_admin

from pydantic import BaseModel
from typing import List, Dict, Any

router = APIRouter(prefix="/curriculum", tags=["curriculum"])


def _sanitize(obj):
    if isinstance(obj, float) and math.isnan(obj):
        return None
    if isinstance(obj, str) and obj.strip() in ("", "--"):
        return None
    if isinstance(obj, dict):
        return {k: _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize(v) for v in obj]
    return obj


@router.post(
    "/upload",
    dependencies=[Depends(require_admin)],
    status_code=status.HTTP_201_CREATED,
)
async def upload_and_save_curriculum(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    ext = os.path.splitext(file.filename)[1].lower() or ".xlsx"
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
    try:
        tmp.write(await file.read())
        tmp.close()

        data = parse_curriculum(tmp.name)
        data = _sanitize(data)

        prog = data["program"]
        code = prog["program_code"]
        year = prog["intake_year"]
        lang = prog.get("language")

        existing = (
            db.query(Curriculum)
              .filter_by(program_code=code, intake_year=year, language=lang)
              .first()
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Curriculum '{code}' for year {year}"
                    f"{f' ({lang})' if lang else ''} already exists (id={existing.id})"
                )
            )

        cur = Curriculum(
            program_code=code,
            program_name=prog["program_name"],
            intake_year=year,
            total_credits=prog["total_credits"],
            language=lang,
        )
        db.add(cur)
        db.flush()

        for yr, sems in data["courses"].items():
            for sem, lst in sems.items():
                for c in lst:
                    raw_ch = c.get("contact_hours")
                    try:
                        ch = float(raw_ch) if raw_ch is not None else None
                    except:
                        ch = None

                    db.add(Course(
                        curriculum_id=cur.id,
                        year=int(yr),
                        semester=sem,
                        block=c.get("block", ""),
                        discipline_code=c.get("discipline_code", ""),
                        discipline_name=c.get("discipline_name", ""),
                        discipline_type=c.get("discipline_type", ""),
                        credits=c.get("credits", 0) or 0,
                        contact_hours=ch,
                        exam_type=c.get("exam_type"),
                        prerequisite=c.get("prerequisite"),
                        module=c.get("module", ""),
                    ))

        for grp, lst in data["electives"].items():
            for e in lst:
                raw_ch = e.get("contact_hours")
                try:
                    ch = float(raw_ch) if raw_ch is not None else None
                except:
                    ch = None

                db.add(Elective(
                    curriculum_id=cur.id,
                    group_name=grp,
                    block=e.get("block", ""),
                    discipline_code=e.get("discipline_code", ""),
                    discipline_name=e.get("discipline_name", ""),
                    discipline_type=e.get("discipline_type", ""),
                    credits=e.get("credits", 0) or 0,
                    contact_hours=ch,
                    exam_type=e.get("exam_type"),
                    prerequisite=e.get("prerequisite"),
                    module=e.get("module", ""),
                ))

        db.commit()
        return {"msg": "Curriculum saved", "id": cur.id}

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        try:
            os.unlink(tmp.name)
        except:
            pass


class CurriculumSummary(BaseModel):
    id: int
    program_code: str
    program_name: str
    intake_year: int
    language: str


@router.get(
    "/",
    response_model=List[CurriculumSummary],
    dependencies=[Depends(require_admin)],
)
def list_curricula(db: Session = Depends(get_db)):
    items = db.query(Curriculum).all()
    return [
        {
            "id":           c.id,
            "program_code": c.program_code,
            "program_name": c.program_name,
            "intake_year":  c.intake_year,
            "language":     c.language,
        }
        for c in items
    ]


class CurriculumDetailResponse(BaseModel):
    program:   Dict[str, Any]
    courses:   Dict[str, Dict[str, List[Dict[str, Any]]]]
    electives: Dict[str, List[Dict[str, Any]]]


def _group_courses(courses: List[Course]):
    out: Dict[str, Dict[str, List[Dict[str, Any]]]] = {}
    for c in courses:
        y = str(c.year)
        out.setdefault(y, {}).setdefault(c.semester, []).append({
            "block":           c.block,
            "discipline_code": c.discipline_code,
            "discipline_name": c.discipline_name,
            "discipline_type": c.discipline_type,
            "credits":         c.credits,
            "contact_hours":   c.contact_hours,
            "exam_type":       c.exam_type,
            "prerequisite":    c.prerequisite,
            "module":          c.module,
        })
    return out


def _group_electives(electives: List[Elective]):
    out: Dict[str, List[Dict[str, Any]]] = {}
    for e in electives:
        grp = e.group_name
        out.setdefault(grp, []).append({
            "block":           e.block,
            "discipline_code": e.discipline_code,
            "discipline_name": e.discipline_name,
            "discipline_type": e.discipline_type,
            "credits":         e.credits,
            "contact_hours":   e.contact_hours,
            "exam_type":       e.exam_type,
            "prerequisite":    e.prerequisite,
            "module":          e.module,
        })
    return out


@router.get(
    "/{curriculum_id}",
    response_model=CurriculumDetailResponse,
    dependencies=[Depends(require_admin)],
)
def get_curriculum(curriculum_id: str, db: Session = Depends(get_db)):
    cur = db.query(Curriculum).filter_by(id=curriculum_id).first()
    if not cur:
        raise HTTPException(status_code=404, detail="Curriculum not found")

    return {
        "program": {
            "program_code":  cur.program_code,
            "program_name":  cur.program_name,
            "intake_year":   cur.intake_year,
            "total_credits": cur.total_credits,
            "language":      cur.language,
        },
        "courses":   _group_courses(cur.courses),
        "electives": _group_electives(cur.electives),
    }
