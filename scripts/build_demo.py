#!/usr/bin/env python3
"""把 ledger.csv 整理成 docs/demos/ledger-chart/data.json，給 HTML-in-Canvas 的 demo 模組用。"""
import csv, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "demos" / "ledger-chart" / "data.json"

groups = {}
rows = [r for r in csv.DictReader(open(ROOT / "ledger.csv", encoding="utf-8", newline="")) if r["狀態"] == "有效"]
for r in rows:
    groups.setdefault(r["對手組"], []).append(
        dict(id=r["line_id"], feature=r["功能"], result=r["戰報"], kind=r["類型"], level=r["支援狀態"]))

data = dict(total=len(rows), updated=max(r["日期"] for r in rows),
            groups=[dict(name=k, lines=v) for k, v in groups.items()])
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"docs/demos/ledger-chart/data.json: {len(groups)} groups, {len(rows)} lines")
