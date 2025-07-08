import re
import unicodedata
import pandas as pd
from collections import defaultdict

def normalize_text(text):
    return unicodedata.normalize("NFKC", text)

def detect_language(text_lines):
    joined = " ".join(text_lines).lower()
    if "жылы" in joined or "пән" in joined:
        return "kz"
    elif "year" in joined or "course" in joined or "semester" in joined:
        return "en"
    return "ru"

def extract_metadata(lines):
    meta = {
        "program_code": None,
        "program_name": None,
        "intake_year": None,
        "language": detect_language(lines),
    }
    for line in lines:
        norm = normalize_text(line)

        m = re.search(r'(6[ВB][0-9]{5})\s+"(.+?)"', norm)
        if m:
            meta["program_code"] = m.group(1)
            meta["program_name"] = m.group(2).strip()

        y = re.search(r"(20\d{2})\s*(г|жылы|intake)", norm.lower())
        if y:
            meta["intake_year"] = int(y.group(1))

    return meta

def parse_curriculum(excel_path):
    excel = pd.ExcelFile(excel_path)
    df_raw = excel.parse(excel.sheet_names[0], header=None)

    lines = []
    for i in range(40):
        row = df_raw.iloc[i]
        txt = " ".join(str(c) for c in row if pd.notna(c)).strip()
        if txt:
            lines.append(txt)

    meta = extract_metadata(lines)
    language = meta["language"]

    df_full = excel.parse(excel.sheet_names[0], header=None)
    df = df_full.iloc[8:].reset_index(drop=True)

    base_cols = [
        "marker", "block", "discipline_code", "name", "credits",
        "contact_hours", "exam_type", "discipline_type",
        "prerequisite", "module"
    ]
    n_cols = df.shape[1]
    if n_cols < len(base_cols):
        raise ValueError(f"В файле {n_cols} столбцов, а нужно минимум {len(base_cols)}")
    extra = [f"ignore{i}" for i in range(n_cols - len(base_cols))]
    df.columns = base_cols + extra


    year_map = {
        "первый": 1, "второй": 2, "третий": 3, "четвертый": 4,
        "бірінші": 1, "екінші": 2, "үшінші": 3, "төртінші": 4,
        "first": 1, "second": 2, "third": 3, "fourth": 4
    }


    fall_keywords = {"осень", "итого осень", "күз", "күзі:", "autumn", "total autumn"}
    spring_keywords = {"весна", "итого весна", "көктем", "көктемі:", "spring", "total spring"}

    skip_names = {
        "наименование дисциплины", "пәннің атауы", "course title"
    }

    parsed = []
    electives = []
    in_el = False
    grp = None
    curr_year = curr_sem = curr_season = None

    for _, r in df.iterrows():
        mkr = str(r["marker"]).strip()
        blk = str(r["block"]).strip().lower()

        if re.fullmatch(r"G\d+", mkr, re.IGNORECASE):
            in_el = True
            grp = mkr

        if not in_el:
            for k, v in year_map.items():
                if blk.startswith(f"{k} год") or blk.startswith(f"{k} оқу жылы") or blk.startswith(f"{k} year"):
                    curr_year = v
                    break

            if any(k in blk for k in fall_keywords):
                curr_season = "fall"
                curr_sem = (curr_year - 1) * 2 + 1 if curr_year else None
            elif any(k in blk for k in spring_keywords):
                curr_season = "spring"
                curr_sem = (curr_year - 1) * 2 + 2 if curr_year else None

        if pd.notna(r["name"]) and pd.notna(r["credits"]):
            name = str(r["name"]).strip().lower()
            if name in skip_names:
                continue

            entry = {
                "block": r["block"],
                "discipline_code": r["discipline_code"],
                "discipline_name": r["name"],
                "credits": r["credits"],
                "contact_hours": r["contact_hours"],
                "exam_type": r["exam_type"],
                "discipline_type": r["discipline_type"],
                "prerequisite": r["prerequisite"],
                "module": r["module"]
            }

            if in_el:
                entry["group"] = grp
                electives.append(entry.copy())
            else:
                entry.update({
                    "year": curr_year,
                    "semester": curr_sem,
                    "season": curr_season
                })
                parsed.append(entry.copy())

    by_year = defaultdict(lambda: {"fall": [], "spring": []})
    for c in parsed:
        y, s = c["year"], c["season"]
        data = {k: v for k, v in c.items() if k not in ("year", "season")}
        if y and s:
            by_year[y][s].append(data)

    el_by_grp = defaultdict(list)
    for e in electives:
        g = e.pop("group", "Unknown")
        el_by_grp[g].append(e)

    total = sum(float(c["credits"]) for c in parsed if pd.notna(c["credits"]))
    meta["total_credits"] = total

    return {
        "program": meta,
        "courses": dict(by_year),
        "electives": dict(el_by_grp)
    }
