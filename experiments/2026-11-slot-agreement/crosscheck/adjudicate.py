"""兩邊盲測判讀不一致的退路，交給 Opus 依 PROMPT.md 規則與上游原文仲裁（兩個答案匿名、順序隨機）。"""
import json, random, subprocess, pathlib, re
HERE = pathlib.Path(__file__).parent; ROOT = HERE.parents[2]
rule = re.search(r"3\. \*\*退路\*\*.*?(?=\n4\. \*\*解鎖\*\*)", (ROOT / "PROMPT.md").read_text(encoding="utf-8"), re.S).group(0)
cases = []
for orig, new, inp in (("kimi.json", "agy.jsonl", "input.json"), ("agy-original.json", "kimi.jsonl", "input-agy-lines.json")):
    O = json.load(open(HERE / orig)); N = {json.loads(x)["key"]: json.loads(x) for x in open(HERE / new)}
    I = {x["key"]: x for x in json.load(open(HERE / inp))}
    for k in O:
        if O[k]["fallback"] != N[k]["fallback"]:
            a = O[k]["fallback_text"]; b = f'{N[k]["fallback"]}——{N[k]["fallback_text"]}'
            cases.append(dict(key=k, item=I[k], answers=[("orig", a), ("blind", b)]))
rng = random.Random(5)
done_p = HERE / "adjudication.jsonl"
done = {json.loads(x)["key"] for x in done_p.read_text().splitlines()} if done_p.exists() else set()
def parse(s):
    m = re.search(r"\{.*\}", s, re.S)
    if m:
        try: return json.loads(m.group(0))
        except json.JSONDecodeError: pass
    g = lambda k: (re.search(rf'"{k}"\s*:\s*"([^"]*)', s) or [None, ""])[1]
    return {"fallback": g("fallback"), "agree": g("agree"), "reason": (re.search(r'"reason"\s*:\s*"(.*)', s, re.S) or [None, s[-300:]])[1][:400]}
for c in cases:
    ans = c["answers"][:]; rng.shuffle(ans)
    if c["key"] in done: continue
    it = c["item"]; guide = (ROOT / it["upstream"]).read_text(encoding="utf-8")
    prompt = f"""你是仲裁者。依下面的規則與指南原文，判斷這條線的「退路」應該是哪一類。只根據指南原文，不要用外部知識。

規則：
{rule}

線：{it['title']}
做法：{it['action']}
對手：{it['opponent']}
支援狀態：{it['support']}

兩個判讀者的答案：
甲：{ans[0][1]}
乙：{ans[1][1]}

指南全文：
{guide}

先想清楚「這條線的對手」是什麼，再判斷退回後那個對手有沒有回來。只輸出一行 JSON：{{"fallback": "不需要|保住主要行為|失去主要好處|沒說", "agree": "甲|乙|都不對", "reason": "一兩句，引用原文關鍵句"}}"""
    r = subprocess.run(["claude", "-p", "--model", "opus", prompt], capture_output=True, text=True, timeout=900)
    v = parse(r.stdout)
    side = {"甲": ans[0][0], "乙": ans[1][0]}.get(v.get("agree"), "neither")
    with done_p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(dict(key=c["key"], verdict=v, sided_with=side, answers=dict(c["answers"])), ensure_ascii=False) + "\n")
    print(c["key"], v.get("fallback"), side, flush=True)
