import fitz
import re
import uuid
from datetime import datetime

from sqlalchemy.orm import joinedload
from app.db import SessionLocal
from app.models import Curriculum

def extract_transcript_text(pdf_path):
    with fitz.open(pdf_path) as doc:
        return "\n".join(page.get_text() for page in doc)


def detect_language(text):
    if re.search(r'(?i)\b(Жақсы|Өте жақсы|Қанағат-лық|сынақталмаған|сынақ)\b', text):
        return 'kk'
    if re.search(r'(?i)\b(Good|Excellent|Satisfactory|passed attestation)\b', text):
        return 'en'
    return 'ru'


def safe_split_get(text, delimiter='/', index=0):
    parts = text.split(delimiter)
    return parts[index].strip() if index < len(parts) else None


LANG_KEYS = {
    'ru': {
        'faculty': 'Факультет',
        'group': 'Группа образовательных программ',
        'program': 'Образовательная программа',
        'year': 'Год поступления',
        'language': 'Язык обучения',
    },
    'kk': {
        'faculty': 'Факультет',
        'group': 'Білім беру бағдарламаларының тобы',
        'program': 'Білім беру бағдарламасы',
        'year': 'Түскен жылы',
        'language': 'Оқыту тілі',
    },
    'en': {
        'faculty': 'Faculty',
        'group': 'Educational program group',
        'program': 'Educational program/',
        'year': 'Enter year',
        'language': 'Language of education',
    }
}


def extract_student_info(text):
    lang = detect_language(text)
    keys = LANG_KEYS[lang]
    idx_map = {'kk': 0, 'en': 1, 'ru': 2}
    idx = idx_map[lang]

    info = {
        'name': None,
        'faculty': None,
        'program_group': None,
        'program_code': None,
        'program_name': None,
        'entry_year': None,
        'language': None,
        'gpa': None,
        'total_credits': None
    }
    lines = text.splitlines()

    for i, line in enumerate(lines):
        if 'Transcript' in line:
            raw = lines[i + 1].strip()
            info['name'] = raw.split('/', 1)[0].strip()
            break

    for i, line in enumerate(lines):
        if keys['faculty'] in line and i - 1 >= 0:
            info['faculty'] = safe_split_get(lines[i - 1], '/', idx)

        if keys['group'] in line and i - 1 >= 0:
            info['program_group'] = safe_split_get(lines[i - 1], '/', idx)

        if keys['program'] in line and i - 1 >= 0:
            maybe_program = safe_split_get(lines[i - 1], '/', idx)
            if maybe_program:
                tokens = maybe_program.split()
                if len(tokens) >= 2:
                    info['program_code'] = tokens[0]
                    info['program_name'] = ' '.join(tokens[1:])
                else:
                    info['program_code'] = maybe_program


    m = re.search(keys['year'] + r'.*?(\d{4})', text)
    if m:
        info['entry_year'] = int(m.group(1))

    for line in lines:
        if keys['language'] in line:
            parts = [p.strip() for p in line.split('/')]
            if lang == 'kk':
                raw = parts[2]
                info['language'] = ' '.join(raw.split()[-2:])
            elif lang == 'en':
                info['language'] = parts[-2]
            else:
                info['language'] = parts[-1]
            break

    m = re.search(r'GPA.*?(\d+\.\d+)', text)
    if m:
        info['gpa'] = float(m.group(1))

    credits = re.search(r'(?:Кредиттердің жалпы саны|Total credits passed|Общее количество кредитов)[^\d]{0,20}(\d+)', text)
    info["total_credits"] = int(credits.group(1)) if credits else None

    return info


GRADE_MAP = {
    'ru': {'Отлично': 'Отлично', 'Хорошо': 'Хорошо', 'Удов': 'Удовлетворительно', 'Зачет': 'Зачет', 'Неуд': 'Неудовлетворительно', 'не зачет': 'Не зачет'},
    'kk': {'Өте жақсы': 'Өте жақсы', 'Жақсы': 'Жақсы', 'Қанағат-лық': 'Қанағат-лық', 'сынақ': 'Сынақ', 'сынақталмаған': 'Сынақталмаған'},
    'en': {'Excellent': 'Excellent', 'Good': 'Good', 'Sat': 'Satisfactory', 'Satisfactory': 'Satisfactory', 'Pass': 'Pass', 'Unsat': 'Unsatisfactory', 'not passed': 'Not passed'}
}


def extract_courses(text):
    lang = detect_language(text)
    lines = text.splitlines()
    courses, buf = [], []
    num = 1
    headers = ['п/п', 'courses', 'cources', 'наименование', 'кредит', 'percent', 'traditional']
    start = False

    for line in lines:
        l = line.strip()
        if not start and any(h in l.lower() for h in headers):
            start = True
            continue
        if not start:
            continue

        if re.match(r'^\d+\s+', l):
            if buf:
                course = _parse_course(' '.join(buf), lang, num)
                if course:
                    courses.append(course)
                    num += 1
                buf = []
        buf.append(l)

    if buf:
        course = _parse_course(' '.join(buf), lang, num)
        if course:
            courses.append(course)

    return [c for c in courses if '/' not in c['course_name'].lower() and 'transcript' not in c['course_name'].lower()]


def _parse_course(text, lang, code):
    text = re.sub(r'^\d+\s+', '', text)
    m = re.match(
        r'(.+?)\s+(\d+)\s*'
        r'(\d+\.\d+)?\s*'
        r'([A-DF][+-]?|F)?\s*'
        r'(\d+\.\d+)?\s*'
        r'(.+)?$',
        text
    )
    if not m:
        return None

    name, cr, perc, letter, gp, trad_raw = m.groups()

    trad_trans = None
    if trad_raw:
        cleaned = re.sub(r'\d{2}\.\d{2}\.\d{4}|https?://\S+', '', trad_raw, flags=re.IGNORECASE).strip()
        for key in sorted(GRADE_MAP[lang].keys(), key=len, reverse=True):
            if key.lower() in cleaned.lower():
                trad_trans = GRADE_MAP[lang][key]
                break
        if trad_trans is None:
            trad_trans = cleaned or None

    is_retake = False

    if '*' in name:
        is_retake = True
    if letter and letter.upper() == 'F':
        is_retake = True
    if gp and float(gp) == 0.0:
        is_retake = True
    if trad_trans and any(fk in trad_trans.lower() for fk in ['незачет', 'не зачет', 'сынақталмаған', 'not passed', 'unsat', 'unsatisfactory']):
        is_retake = True

    return {
        'code': code,
        'course_name': name.strip().title(),
        'credits': int(cr),
        'percent': float(perc) if perc else None,
        'grade_letter': letter or None,
        'grade_point': float(gp) if gp else None,
        'grade_traditional': trad_trans,
        'is_retake': is_retake
    }

def find_curriculum_id(program_code, intake_year):
    db = SessionLocal()
    try:
        curriculum = db.query(Curriculum.id).filter_by(
            program_code=program_code,
            intake_year=intake_year
        ).first()
        return curriculum.id if curriculum else None
    finally:
        db.close()


def compare_courses_with_curriculum(transcript_courses, curriculum_courses, electives):
    transcript_names = set(c['course_name'].strip().lower() for c in transcript_courses)

    missing_mandatory = []
    for course in curriculum_courses:
        if course.discipline_name.strip().lower() not in transcript_names:
            missing_mandatory.append({
                "discipline_code": course.discipline_code,
                "discipline_name": course.discipline_name,
                "credits": course.credits,
                "type": course.discipline_type,
                "block": course.block
            })

    missing_electives = []
    for elective in electives:
        if elective.discipline_name.strip().lower() not in transcript_names:
            missing_electives.append({
                "group_name": elective.group_name,
                "discipline_code": elective.discipline_code,
                "discipline_name": elective.discipline_name,
                "credits": elective.credits
            })

    return {
        "missing_mandatory_courses": missing_mandatory,
        "missing_electives": missing_electives
    }

def parse_transcript(pdf_path):
    text = extract_transcript_text(pdf_path)
    student_info = extract_student_info(text)
    courses = extract_courses(text)

    curriculum_id = None
    if student_info['program_code'] and student_info['entry_year']:
        curriculum_id = find_curriculum_id(
            student_info['program_code'],
            student_info['entry_year']
        )

    return {
        'student_id': str(uuid.uuid4()),
        'parsed_at': datetime.now().isoformat(),
        'student_info': student_info,
        'courses': courses,
        'curriculum_id': curriculum_id
    }