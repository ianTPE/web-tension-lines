#!/usr/bin/env python3
"""替每個對手組產生一頁 Obsidian 索引：groups/<對手組>.md。

每頁列出該組的線（連到線檔裡的標題），以及「常一起出現的組」（同一份指南裡也出現的其他組）。
在 Obsidian 的關係圖裡，對手組頁與指南線檔互相連起來，同一份指南裡出現的組會聚在一起。
另產生 groups/對手組總覽.md。由 scripts/weekly.sh 每週重建；不要手改。
"""
import csv, collections, itertools, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "groups"
LINE_RE = re.compile(r'%% line-start id="([^"]+)" %%\n(.*?)%% line-end %%', re.S)
INDEX = "對手組總覽"

ledger = [r for r in csv.DictReader(open(ROOT / "ledger.csv", encoding="utf-8", newline="")) if r["狀態"] == "有效"]
en = json.load(open(ROOT / "i18n/en.json", encoding="utf-8"))

# 線檔位置與標題（連結用）
where = {}
for p in sorted((ROOT / "lines").glob("*/*.md")):
    for lid, body in LINE_RE.findall(p.read_text(encoding="utf-8")):
        title = re.search(r"^## (.+)$", body, re.M).group(1).strip()
        where[lid] = (p.relative_to(ROOT).with_suffix("").as_posix(), title)

by_group = collections.defaultdict(list)
for r in ledger:
    if r["line_id"] in where:
        by_group[r["對手組"]].append(r)

# 共現：兩個組出現在同一份指南
guide_groups = collections.defaultdict(set)
for r in ledger:
    guide_groups[r["guide_id"]].add(r["對手組"])
co = collections.Counter()
for gs in guide_groups.values():
    for a, b in itertools.combinations(sorted(gs), 2):
        co[(a, b)] += 1
neighbors = collections.defaultdict(list)
for (a, b), n in co.items():
    neighbors[a].append((b, n)); neighbors[b].append((a, n))

def link(lid, table=False):
    path, title = where[lid]
    # Obsidian 標題連結裡不能有 # | ^ [ ]，換掉
    safe = re.sub(r"[#|^\[\]]", " ", title).strip()
    return f"[[{path}#{safe}{chr(92) if table else ''}|{title}]]"

def dist(rows, key, order):
    c = collections.Counter(r[key] for r in rows)
    return "、".join(f"{k} {c[k]}" for k in order if c[k])

OUT.mkdir(exist_ok=True)
for old in OUT.glob("*.md"):
    old.unlink()

for g, rows in sorted(by_group.items(), key=lambda kv: (-len(kv[1]), kv[0])):
    rows = sorted(rows, key=lambda r: (r["類型"] != "新能力", r["guide_id"], r["line_id"]))
    guides = sorted({r["guide_id"] for r in rows})
    nb = sorted(neighbors[g], key=lambda x: (-x[1], x[0]))
    lines = [
        "---",
        f"group: {g}",
        f"group_en: {en.get('groups', {}).get(g, '')}",
        f"lines: {len(rows)}",
        f"guides: {len(guides)}",
        "tags: [對手組]",
        "---",
        "",
        f"# {g}",
        "",
        f"{len(rows)} 條線，出自 {len(guides)} 份指南。",
        "",
        f"- 類型：{dist(rows, '類型', ['新能力', '糾錯'])}",
        f"- 戰報：{dist(rows, '戰報', ['勝', '部分改善', '僵持'])}",
        f"- 退路：{dist(rows, '退路', ['不需要', '保住主要行為', '失去主要好處', '沒說'])}",
        "",
        "## 線",
        "",
        "| 線 | 指南 | 類型 | 戰報 | 對手 |",
        "|---|---|---|---|---|",
    ]
    for r in rows:
        opp = r["對手"].replace("|", "／").replace("\n", " ")
        opp = opp if len(opp) <= 60 else opp[:60] + "…"
        lines.append(f"| {link(r['line_id'], table=True)} | {r['guide_id']} | {r['類型']} | {r['戰報']} | {opp} |")
    if nb:
        lines += ["", "## 常一起出現的組", "", "同一份指南裡也出現的其他對手組（括號內是共同的指南數）。", ""]
        lines += [f"- [[groups/{b}|{b}]]（{n}）" for b, n in nb[:12]]
    lines += ["", f"← [[groups/{INDEX}|{INDEX}]]", ""]
    (OUT / f"{g}.md").write_text("\n".join(lines), encoding="utf-8")

# 總覽
idx = [
    "---", "tags: [對手組]", "---", "", f"# {INDEX}", "",
    f"共 {len(by_group)} 個對手組、{sum(len(v) for v in by_group.values())} 條線。依條數排序；「跨指南」是出現在幾份不同的指南。",
    "", "在 Obsidian 開關係圖（Graph view）可以看到對手組頁和指南線檔怎麼連在一起：常在同一份指南出現的組會聚成一群。",
    "", "| 對手組 | 條數 | 跨指南 | 新能力 | 常一起出現 |", "|---|---|---|---|---|",
]
for g, rows in sorted(by_group.items(), key=lambda kv: (-len(kv[1]), kv[0])):
    nb = sorted(neighbors[g], key=lambda x: (-x[1], x[0]))[:3]
    idx.append(f"| [[groups/{g}\\|{g}]] | {len(rows)} | {len({r['guide_id'] for r in rows})} | "
               f"{sum(r['類型'] == '新能力' for r in rows)} | {'、'.join(b for b, _ in nb)} |")
(OUT / f"{INDEX}.md").write_text("\n".join(idx) + "\n", encoding="utf-8")
print(f"groups/: {len(by_group)} 個對手組頁 + {INDEX}")
