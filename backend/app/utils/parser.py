import fitz
import re
import uuid
import json
from datetime import datetime


def extract_transcript_text(pdf_path):
    with fitz.open(pdf_path) as doc:
        return "\n".join(page.get_text() for page in doc)


def extract_student_name(text):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if "Transcript" in line and i + 1 < len(lines):
            return lines[i + 1].strip()
    match = re.search(r'([А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+)', text)
    return match.group(1) if match else "Unknown"


def extract_student_info(text):
    info = {
        "name": extract_student_name(text),
        "faculty": None,
        "program_group": None,
        "program_code": None,
        "program_name": None,
        "entry_year": None,
        "language": None,
        "gpa": None,
        "total_credits": None
    }

    match_faculty = re.search(r'(.*?)\nФакультет', text, flags=re.DOTALL)
    if match_faculty:
        info["faculty"] = match_faculty.group(1).strip().splitlines()[-1]

    match_group = re.search(r'^(.*) / (.*) / (.*)\n.*Группа образовательных программ', text, flags=re.MULTILINE)
    if match_group:
        info["program_group"] = match_group.group(1).strip()

    lines = text.splitlines()
    for i, line in enumerate(lines):
        if "Білім беру бағдарламасы" in line and i > 0:
            tokens = lines[i - 1].split('/')[0].strip().split(maxsplit=1)
            if len(tokens) == 2:
                info["program_code"], info["program_name"] = tokens
            break

    year = re.search(r'Түскен жылы.*?(\d{4})', text)
    info["entry_year"] = int(year.group(1)) if year else None

    lang = re.search(r'Оқыту тілі.*?\n', text)
    info["language"] = lang.group().split('/')[-1].strip() if lang else None

    gpa = re.search(r'GPA.*?([\d.]+)', text)
    info["gpa"] = float(gpa.group(1)) if gpa else None

    credits = re.search(r'(?:Кредиттердің жалпы саны|Total credits passed|Общее количество кредитов)[^\d]{0,20}(\d+)', text)
    info["total_credits"] = int(credits.group(1)) if credits else None

    return info


def extract_courses(text):
    lines = text.splitlines()
    courses = []
    buffer = []
    course_number = 1

    def flush(buf):
        joined = " ".join(buf).strip()
        joined = re.sub(r'^\d+\s+', '', joined)
        pattern = re.compile(
            r'(?P<name>.+?)\s+'
            r'(?P<credits>\d+)\s+(?P<percent>\d+\.\d)?\s*'
            r'(?P<letter>[A-D][+-]?|F|зачет)\s*'
            r'(?P<gpa>[\d.]+)?\s*'
            r'(?P<trad>Хорошо|Удов|Отлично)?'
        )
        m = pattern.search(joined)
        if m:
            return {
                "code": None,
                "course_name": m.group("name").title(),
                "credits": int(m.group("credits")),
                "percent": float(m.group("percent")) if m.group("percent") else None,
                "grade_letter": m.group("letter"),
                "grade_point": float(m.group("gpa")) if m.group("gpa") else None,
                "grade_traditional": m.group("trad") or "Зачет",
                "is_retake": "*" in m.group("name")
            }
        return None

    start = False
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if "Пәннің атауы" in line or "Cources" in line:
            start = True
            continue
        if not start:
            continue
        if re.match(r'^\d+\s+[А-Яа-яA-Za-z]', line):
            if buffer:
                course = flush(buffer)
                if course:
                    course["code"] = course_number
                    courses.append(course)
                    course_number += 1
                buffer = []
        buffer.append(line)

    if buffer:
        course = flush(buffer)
        if course:
            course["code"] = course_number
            courses.append(course)

    return courses


def parse_transcript(pdf_path):
    text = extract_transcript_text(pdf_path)
    return {
        "student_id": str(uuid.uuid4()),
        "parsed_at": datetime.now().isoformat(),
        "student_info": extract_student_info(text),
        "courses": extract_courses(text)
    }
