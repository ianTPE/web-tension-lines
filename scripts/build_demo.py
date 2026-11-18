#!/usr/bin/env python3
"""把 ledger.csv 整理成戰報圖 demo 的資料：docs/demos/ledger-chart/data.json（中文）與 docs/en/demos/ledger-chart/data.json（英文）。"""
import csv, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
EN = json.load(open(ROOT / "i18n/en.json", encoding="utf-8"))
rows = [r for r in csv.DictReader(open(ROOT / "ledger.csv", encoding="utf-8", newline="")) if r["狀態"] == "有效"]

def build(lang):
    t = (lambda m, v: v) if lang == "zh" else (lambda m, v: EN[m].get(v, v))
    groups = {}
    for r in rows:
        groups.setdefault(t("groups", r["對手組"]), []).append(
            dict(id=r["line_id"], feature=r["功能"], result=t("result", r["戰報"]), kind=t("kind", r["類型"]), level=t("level", r["支援狀態"])))
    return dict(total=len(rows), updated=max(r["日期"] for r in rows), groups=[dict(name=k, lines=v) for k, v in groups.items()])

for lang, out in (("zh", ROOT / "docs/demos/ledger-chart/data.json"), ("en", ROOT / "docs/en/demos/ledger-chart/data.json")):
    out.parent.mkdir(parents=True, exist_ok=True)
    data = build(lang)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{out.relative_to(ROOT)}: {len(data['groups'])} groups, {len(rows)} lines")
