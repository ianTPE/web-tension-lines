"""從上游英文原文生成測試查詢（不給模型看我們寫的線），輸出 queries.jsonl。

每條抽樣的線給模型：指南標題＋引文附近的上游原文段落。模型寫兩種查詢：
  symptom：開發者描述自己遇到的現象（找答案）
  goal：開發者想做出的東西（找靈感）
都不得出現 API／屬性／元素名稱，也不得直譯引文。
"""
import json, random, re, subprocess, sys, pathlib
from lines import load, guide_text

HERE = pathlib.Path(__file__).parent
N = int(sys.argv[1]) if len(sys.argv) > 1 else 150
norm = lambda s: re.sub(r"\s+", " ", re.sub(r"[`*]", "", s)).strip()


def context(l, width=900):
    g = norm(guide_text(l["guide"]))
    title = g.split(" ## ")[0][:200]
    q = norm(l["quote"])[:60]
    i = g.find(q) if q else -1
    if i < 0:
        return title, g[:width * 2]
    return title, g[max(0, i - width):i + width]


L = [l for l in load() if l["quote"]]
rng = random.Random(20261117)
by_group = {}
for l in L:
    by_group.setdefault(l["group"], []).append(l)
# 分層抽樣：每個對手組先抽一條，不夠再隨機補
sample = [rng.choice(v) for v in by_group.values()]
rest = [l for l in L if l not in sample]
rng.shuffle(rest)
sample = (sample + rest)[:N]
rng.shuffle(sample)

PROMPT = """You write test queries for a retrieval experiment. For each item below you get a web-development guide's title and an excerpt of its original text. The excerpt describes a problem developers run into and how a platform feature addresses it.

For each item write TWO queries in Traditional Chinese (台灣用語), as a real developer would type them into a search box or ask a colleague:
- "symptom": 1–2 sentences, first person, describing the concrete thing that goes wrong for them (what they see, what users complain about). Describe the situation, not the solution.
- "goal": 1 sentence, first person, describing something they want to build or achieve where this problem would block them.

Rules:
- Do NOT name any API, CSS property, HTML element or attribute, JS method, or spec name (no `moveBefore`, `popover`, `:has`, `aria-live`, etc.). Generic words like 表格、按鈕、表單、圖片、動畫、螢幕閱讀器 are fine.
- Do NOT translate the excerpt's sentences; paraphrase from a user's point of view.
- Keep each query under 80 Chinese characters.

Output ONLY JSON lines, one per item, in order: {"id": "...", "symptom": "...", "goal": "..."}

"""

out = HERE / "queries.jsonl"
done = {json.loads(x)["id"] for x in out.read_text().splitlines()} if out.exists() else set()
todo = [l for l in sample if l["id"] not in done]
for b in range(0, len(todo), 25):
    batch = todo[b:b + 25]
    items = []
    for l in batch:
        t, c = context(l)
        items.append(f'### id: {l["id"]}\nGuide: {t}\nExcerpt: {c}\n')
    r = subprocess.run(["claude", "-p", "--model", "haiku", PROMPT + "\n".join(items)],
                       capture_output=True, text=True, timeout=600)
    got = 0
    with out.open("a", encoding="utf-8") as f:
        for line in r.stdout.splitlines():
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            if d.get("id") in {l["id"] for l in batch} and d.get("symptom") and d.get("goal"):
                f.write(json.dumps(d, ensure_ascii=False) + "\n"); got += 1
    print(f"batch {b // 25}: {got}/{len(batch)}", r.stderr[-200:] if r.returncode else "", flush=True)
