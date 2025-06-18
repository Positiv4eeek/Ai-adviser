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

GRADE_TRANSLATIONS = {
    "ru": {
        "Отлично": "Отлично",
        "Хорошо": "Хорошо",
        "Удов": "Удовлетворительно",
        "Зачет": "Зачет"
    },
    "kk": {
        "Өте жақсы": "Өте жақсы",
        "Жақсы": "Жақсы",
        "Қанағат-лық": "Қанағат-лық",
        "сынақ": "сынақ"
    },
    "en": {
        "Excellent": "Excellent",
        "Good": "Good",
        "Sat": "Satisfactory",
        "Satisfactory": "Satisfactory",
        "passed attestation": "Pass"
    }
}


def extract_courses(text, lang_code):
    lines = text.splitlines()
    courses = []
    buffer = []
    course_number = 1

    stop_keywords = [
        "қорытынды аттестаттау", "кәсіптік практика", "итоговая аттестация",
        "final certification", "has passed professional", "мaк хаттамасының",
        "diploma work", "gpa", "выполнил", "дипломдық жұмыс"
    ]

    header_keywords = [
        "наименование дисциплины", "кредиттер саны", "пайызбен",
        "traditional", "дәстүрлі жүйемен", "course title", "cources"
    ]

    def flush(buf):
        if not buf:
            return None

        joined = " ".join(buf).strip()

        # Ключевые слова, по которым мы фильтруем "мусор"
        stop_keywords = [
            "наименование дисциплины", "кредиттер саны", "пайызбен",
            "traditional", "дәстүрлі жүйемен", "course title", "cources",
            "қорытынды аттестаттау", "кәсіптік практика", "итоговая аттестация",
            "final certification", "has passed professional", "мaк хаттамасының",
            "diploma work", "gpa", "выполнил", "дипломдық жұмыс"
        ]
        if any(kw in joined.lower() for kw in stop_keywords):
            return None

        # Удаление номера в начале строки
        if re.match(r'^\d+\s+', joined):
            joined = re.sub(r'^\d+\s+', '', joined)

        # Обработка зачётов
        if any(word in joined.lower() for word in ["passed attestation", "сынақ", "зачет", "өтті"]):
            course_name = re.split(r'(passed attestation|сынақ|зачет|өтті)', joined, flags=re.IGNORECASE)[0].strip().title()
            keyword = next((w for w in ["passed attestation", "сынақ", "өтті", "зачет"] if w in joined.lower()), None)
            return {
                "code": None,
                "course_name": course_name,
                "credits": None,
                "percent": None,
                "grade_letter": None,
                "grade_point": None,
                "grade_traditional": GRADE_TRANSLATIONS[lang_code].get(keyword, keyword),
                "is_retake": "*" in course_name
            }

        # Гибкая регулярка
        pattern = re.compile(
            r'(?P<name>.+?)\s+'
            r'(?P<credits>\d+)\s+'
            r'(?P<percent>\d+\.\d)?\s*'
            r'(?P<letter>[A-D][+-]?|F|зачет)?\s*'
            r'(?P<gpa>[\d.]+)?\s*'
            r'(?P<trad>[^«»"]+)?$'
        )

        m = pattern.search(joined)
        if m:
            trad_raw = (m.group("trad") or "").strip()

            # Обрезаем мусор после традиционной оценки
            trad_raw = re.split(r'\d{2}\.\d{2}\.\d{4}|platonus|https?://', trad_raw, flags=re.IGNORECASE)[0].strip()
            trad_raw = " ".join(trad_raw.split()[:2])  # максимум два слова

            translated = GRADE_TRANSLATIONS.get(lang_code, {}).get(trad_raw, trad_raw)

            def safe_float(val):
                try:
                    return float(val)
                except:
                    return None

            return {
                "code": None,
                "course_name": m.group("name").strip().title(),
                "credits": int(m.group("credits")),
                "percent": safe_float(m.group("percent")),
                "grade_letter": m.group("letter"),
                "grade_point": safe_float(m.group("gpa")),
                "grade_traditional": translated,
                "is_retake": "*" in m.group("name")
            }

        print("⚠️ Не удалось распарсить:", joined)
        return None


    start = False
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Запустить парсинг после заголовка
        if not start and any(kw in line.lower() for kw in header_keywords):
            start = True
            continue
        if not start:
            continue

        # Пропустить строки-заголовки и повторяющиеся подписи
        if any(kw in line.lower() for kw in header_keywords):
            continue

        # Если новая строка начинается с номера, значит, курс
        if re.match(r'^\d+\s+[^\s]', line):
            if buffer:
                course = flush(buffer)
                if course:
                    course["code"] = course_number
                    courses.append(course)
                    course_number += 1
                buffer = []
        buffer.append(line)

    # Последний буфер
    if buffer:
        course = flush(buffer)
        if course:
            course["code"] = course_number
            courses.append(course)

    return courses



def detect_language(text):
    if "Жақсы" in text or "Қанағат-лық" in text:
        return "kk"
    elif "Good" in text or "passed attestation" in text:
        return "en"
    else:
        return "ru"

def parse_transcript(pdf_path):
    text = extract_transcript_text(pdf_path)
    lang = detect_language(text)
    return {
        "student_id": str(uuid.uuid4()),
        "parsed_at": datetime.now().isoformat(),
        "student_info": extract_student_info(text),
        "courses": extract_courses(text, lang)
    }
