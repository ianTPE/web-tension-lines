"""抽樣 60 條線，輸出判讀用的輸入檔（上游全文＋目標），不含我們寫的線。"""
import csv, json, random, sys, pathlib
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "2026-11-line-retrieval"))
from lines import load, guide_text

L = [l for l in load() if l["quote"]]
R = {r["line_id"]: r for r in csv.DictReader(open(HERE.parents[1] / "ledger.csv", encoding="utf-8", newline=""))}
import os
rng = random.Random(int(os.environ.get("SEED", 42)))
EXCLUDE = set(json.loads(pathlib.Path(os.environ["EXCLUDE"]).read_text())) if os.environ.get("EXCLUDE") else set()
L = [l for l in L if l["id"] not in EXCLUDE]
new = [l for l in L if l["kind"] == "新能力"]; fix = [l for l in L if l["kind"] == "糾錯"]
rng.shuffle(new); rng.shuffle(fix)
# 新能力與糾錯各半；同一份指南最多 2 條，避免全文太多
pick, per = [], {}
for l in [x for pair in zip(new, fix) for x in pair]:
    if per.get(l["guide"], 0) >= 2: continue
    per[l["guide"]] = per.get(l["guide"], 0) + 1; pick.append(l)
    if len(pick) == 60: break
items = [dict(key=l["id"], guide=l["guide"], target_feature=R[l["id"]]["功能"], target_quote=l["quote"]) for l in pick]
guides = {it["guide"]: guide_text(it["guide"]) for it in items}
(HERE / os.environ.get("OUT", "input.json")).write_text(json.dumps({"items": items, "guides": guides}, ensure_ascii=False, indent=1))
print(len(items), "items,", len(guides), "guides,", sum(len(g) for g in guides.values()), "chars")
