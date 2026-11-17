"""反問測試：模糊查詢先問一題，模擬使用者依真實情境回答，再搜一次。

條件（每題都用同一個搜尋流程：voyage-3.5 取前 30，再 rerank-2.5）：
  direct       原查詢
  generic      原查詢＋對固定開放問題的回答
  raw_targeted 原查詢＋對「提問者看前 8 名的上游原文」所出問題的回答
  slot_targeted原查詢＋對「提問者看前 8 名的四槽」所出問題的回答
  full         模擬使用者完整描述自己的情境（上限）
提問者：Sonnet；回答者：Haiku，看得到該題的上游原文段落（=真實情境），看不到我們寫的線。
"""
import json, random, re, subprocess, sys, pathlib
import numpy as np
from lines import load, guide_text
from voyage import embed, rerank
from make_queries import context

HERE = pathlib.Path(__file__).parent
OUT = HERE / "ask"; OUT.mkdir(exist_ok=True)
L = load(); ID = {l["id"]: i for i, l in enumerate(L)}
Q = [json.loads(x) for x in open(HERE / "queries.jsonl", encoding="utf-8")]
Q = [q for q in Q if q["id"] in ID]
unit = lambda m: (lambda a: a / np.linalg.norm(a, axis=1, keepdims=True))(np.asarray(m, dtype=np.float32))
DOCS = [l["block"] for l in L]
DV = unit(embed(DOCS, "document"))


def search(text):
    qv = unit(embed([text], "query"))[0]
    order = list(np.argsort(-(DV @ qv)))
    top = order[:30]
    rr = rerank(text, [DOCS[j] for j in top])
    return [top[k] for k, _ in rr] + order[30:]


# 選題：70 題原本沒命中第一名、30 題命中
items = []
for q in Q:
    for kind in ("symptom", "goal"):
        items.append(dict(key=f'{q["id"]}|{kind}', id=q["id"], kind=kind, query=q[kind]))
for it in items:
    it["order"] = search(it["query"])
    it["rank"] = it["order"].index(ID[it["id"]]) + 1
rng = random.Random(7)
miss = [it for it in items if it["rank"] > 1]; hit = [it for it in items if it["rank"] == 1]
rng.shuffle(miss); rng.shuffle(hit)
S = sorted(miss[:70] + hit[:30], key=lambda it: it["key"])
print(f"{len(S)} 題：原本未中第一 {sum(it['rank'] > 1 for it in S)}，原本命中 {sum(it['rank'] == 1 for it in S)}；"
      f"正確答案在前 8 名的 {sum(it['rank'] <= 8 for it in S)}", file=sys.stderr)


def claude(model, prompt):
    r = subprocess.run(["claude", "-p", "--model", model, prompt], capture_output=True, text=True, timeout=900)
    rows = []
    for line in r.stdout.splitlines():
        line = line.strip()
        if line.startswith("{"):
            try: rows.append(json.loads(line))
            except json.JSONDecodeError: pass
    return rows


def cached_batches(name, model, header, render, items, size=10, need=()):
    path = OUT / f"{name}.jsonl"
    have = {json.loads(x)["key"]: json.loads(x) for x in path.read_text().splitlines()} if path.exists() else {}
    todo = [it for it in items if it["key"] not in have]
    for _ in range(3):                       # 漏掉的再補兩輪
        for b in range(0, len(todo), size):
            batch = todo[b:b + size]
            rows = claude(model, header + "\n\n".join(render(it) for it in batch))
            keys = {it["key"] for it in batch}
            with path.open("a", encoding="utf-8") as f:
                for r in rows:
                    if r.get("key") in keys and r["key"] not in have and all(r.get(k) for k in need):
                        have[r["key"]] = r; f.write(json.dumps(r, ensure_ascii=False) + "\n")
            print(f"  {name}: {len(have)}/{len(items)}", file=sys.stderr, flush=True)
        todo = [it for it in items if it["key"] not in have]
        if not todo: break
    return have


ASK = """你是網頁開發知識庫的搜尋助理。使用者的查詢太模糊，搜尋結果前 8 名都可能相關。請只問使用者**一個**問題，讓你能分辨他要的是哪一個。
規則：
- 問題用繁體中文，一兩句。可以列 2～5 個選項，但選項要用使用者聽得懂的話描述「他遇到的狀況」，不要出現 API、屬性、元素名稱。
- 問的是能最有效區分這些候選的那個差異。
每題輸出一行 JSON：{"key": "...", "question": "..."}，只輸出 JSON 行。
"""
def render_raw(it):
    cands = []
    for n, j in enumerate(it["order"][:8], 1):
        _, c = context(L[j], width=350)
        cands.append(f"  候選{n}（來自指南《{L[j]['guide']}》的原文段落）：{c}")
    return f'### key: {it["key"]}\n查詢：{it["query"]}\n' + "\n".join(cands)
def render_slot(it):
    cands = []
    for n, j in enumerate(it["order"][:8], 1):
        l = L[j]
        cands.append(f"  候選{n}：{l['title']}\n    動作＋對象：{l['action']}\n    被什麼擋：{l['blocker']}\n    戰報：{l['outcome']}")
    return f'### key: {it["key"]}\n查詢：{it["query"]}\n' + "\n".join(cands)

GENERIC_Q = "可以多說一點你遇到的狀況嗎？"
ANSWER = """你在扮演一位網頁開發者。每題給你：你剛才打的模糊查詢、你**真正的處境**（一段英文的技術說明，描述你實際碰到的問題）、搜尋助理問你的問題。
請照真正的處境回答助理的問題，像真人一樣：
- 繁體中文，一兩句，只回答被問到的部分，不要把處境整段說出來。
- 用你自己的話；如果助理列了選項，說出你選的是哪種狀況並用自己的話描述，不要逐字照抄選項文字。
- 不要說出 API、屬性、元素名稱（你不知道它們叫什麼）。
- 如果選項都不符合，就說都不是，並用一句話說你真正的狀況。
另外，每題再寫一個 "full"：假設沒人問你，你一次把自己的處境完整講清楚（繁中，兩三句，同樣不說 API 名稱）。
每題輸出一行 JSON：{"key": "...", "generic": "...", "raw": "...", "slot": "...", "full": "..."}，只輸出 JSON 行。
"""

if __name__ == "__main__":
    qr = cached_batches("questions-raw", "sonnet", ASK, render_raw, S, need=("question",))
    qs = cached_batches("questions-slot", "sonnet", ASK, render_slot, S, need=("question",))
    def render_ans(it):
        _, c = context(L[ID[it["id"]]], width=700)
        return (f'### key: {it["key"]}\n你的查詢：{it["query"]}\n你真正的處境：{c}\n'
                f'問題 generic：{GENERIC_Q}\n問題 raw：{qr[it["key"]]["question"]}\n問題 slot：{qs[it["key"]]["question"]}')
    ok = [it for it in S if it["key"] in qr and it["key"] in qs]
    an = cached_batches("answers", "haiku", ANSWER, render_ans, ok, need=("generic", "raw", "slot", "full"))
    ok = [it for it in ok if it["key"] in an]

    arms = {
        "direct": lambda it: it["query"],
        "generic": lambda it: it["query"] + "\n" + an[it["key"]]["generic"],
        "raw_targeted": lambda it: it["query"] + "\n" + an[it["key"]]["raw"],
        "slot_targeted": lambda it: it["query"] + "\n" + an[it["key"]]["slot"],
        "full": lambda it: an[it["key"]]["full"],
    }
    ranks = {a: [] for a in arms}
    for it in ok:
        g = ID[it["id"]]
        for a, f in arms.items():
            ranks[a].append(it["rank"] if a == "direct" else search(f(it)).index(g) + 1)
    json.dump({"keys": [it["key"] for it in ok], "ranks": ranks, "orig_rank": [it["rank"] for it in ok]},
              open(OUT / "ranks.json", "w"), ensure_ascii=False)
    print(f"{len(ok)} 題完成", file=sys.stderr)
