import os
import re
import unicodedata
import pandas as pd
from collections import defaultdict

def normalize_text(text):
    return unicodedata.normalize("NFKC", text)

def extract_metadata(lines):
    meta = {"program_code": None, "program_name": None, "intake_year": None, "language": "ru"}
    for line in lines:
        norm = normalize_text(line)
        m = re.search(r'6[ВB][0-9]{5}\s+"(.+?)"', line)
        if m:
            cm = re.search(r'(6[ВB][0-9]{5})', line)
            meta["program_code"] = cm.group(1) if cm else None
            meta["program_name"] = m.group(1).strip()
        y = re.search(r"(20\d{2})\s+г", norm)
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

    df = excel.parse(excel.sheet_names[0])
    df.columns = [
        "marker", "block", "ignore1", "name", "credits",
        "contact_hours", "exam_type", "discipline_type",
        "prerequisite", "module", "ignore2", "ignore3", "ignore4"
    ]
    df = df[8:]

    year_map = {"первый": 1, "второй": 2, "третий": 3, "четвертый": 4}
    parsed, electives = [], []
    in_el, grp = False, None
    curr_year = curr_sem = None
    curr_season = None

    for _, r in df.iterrows():
        mkr = str(r["marker"]).strip()
        blk = str(r["block"]).strip().lower()

        if re.fullmatch(r"G\d+", mkr, re.IGNORECASE):
            in_el = True
            grp = mkr

        if not in_el:
            for k, v in year_map.items():
                if blk.startswith(f"{k} год"):
                    curr_year = v
                    break
            if blk == "осень" or "итого осень" in blk:
                curr_season = "fall"
                curr_sem = (curr_year - 1) * 2 + 1 if curr_year else None
            if blk == "весна" or "итого весна" in blk:
                curr_season = "spring"
                curr_sem = (curr_year - 1) * 2 + 2 if curr_year else None

        if pd.notna(r["name"]) and pd.notna(r["credits"]):
            if r["name"].strip().lower() == "наименование дисциплины":
                continue
            base = {
                "block": r["block"],
                "discipline_code": r["ignore1"],
                "discipline_name": r["name"],
                "credits": r["credits"],
                "contact_hours": r["contact_hours"],
                "exam_type": r["exam_type"],
                "discipline_type": r["discipline_type"],
                "prerequisite": r["prerequisite"],
                "module": r["module"]
            }
            if in_el:
                base["group"] = grp
                electives.append(base.copy())
            else:
                base.update({"year": curr_year, "semester": curr_sem, "season": curr_season})
                parsed.append(base.copy())

    by_year = defaultdict(lambda: {"fall": [], "spring": []})
    for c in parsed:
        y, s = c["year"], c["season"]
        entry = {k: v for k, v in c.items() if k not in ("year", "season")}
        if y and s in by_year[y]:
            by_year[y][s].append(entry)

    el_by_grp = defaultdict(list)
    for e in electives:
        g = e.pop("group", "Unknown")
        el_by_grp[g].append(e)

    total = sum(c["credits"] for c in parsed)
    meta["total_credits"] = total

    return {
        "program": meta,
        "courses": dict(by_year),
        "electives": dict(el_by_grp)
    }