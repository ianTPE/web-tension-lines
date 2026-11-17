"""全面交叉核對的仲裁：full-original.json（原判讀）vs full/kimi.jsonl（盲判），退路不一致的交給 Opus 匿名仲裁，平行 4 路，逐條存檔可續跑。"""
import json, random, re, subprocess, pathlib, glob, sys
from concurrent.futures import ThreadPoolExecutor
HERE = pathlib.Path(__file__).parent; ROOT = HERE.parents[2]
rule = re.search(r"3\. \*\*退路\*\*.*?(?=\n4\. \*\*解鎖\*\*)", (ROOT / "PROMPT.md").read_text(encoding="utf-8"), re.S).group(0)
SUB = sys.argv[1] if len(sys.argv) > 1 else "full"
O = json.load(open(HERE / f"{SUB}-original.json"))
N = {json.loads(x)["key"]: json.loads(x) for x in open(HERE / SUB / (sys.argv[2] if len(sys.argv) > 2 else "kimi.jsonl")) if x.strip()}
I = {x["key"]: x for f in sorted(glob.glob(str(HERE / SUB / "input-*.json"))) for x in json.load(open(f))}
out_p = HERE / SUB / "adjudication.jsonl"
done = {json.loads(x)["key"] for x in out_p.read_text().splitlines()} if out_p.exists() else set()
cases = [k for k in O if k in N and O[k]["fallback"] != N[k]["fallback"] and k not in done]
print(len([k for k in O if k in N]), "compared,", len(cases), "to adjudicate", flush=True)

def parse(s):
    m = re.search(r"\{.*\}", s, re.S)
    if m:
        try: return json.loads(m.group(0))
        except json.JSONDecodeError: pass
    g = lambda k: (re.search(rf'"{k}"\s*:\s*"([^"]*)', s) or [None, ""])[1]
    return {"fallback": g("fallback"), "agree": g("agree"), "reason": s[-400:]}

def one(k):
    ans = [("orig", O[k]["fallback_text"]), ("blind", f'{N[k]["fallback"]}——{N[k]["fallback_text"]}')]
    random.Random(k).shuffle(ans)
    it = I[k]; guide = (ROOT / it["upstream"]).read_text(encoding="utf-8")
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

先想清楚「這條線的對手」是什麼，再判斷退回後那個對手有沒有回來。不要用同一份指南裡其他功能的退路來補。只輸出一行 JSON：{{"fallback": "不需要|保住主要行為|失去主要好處|沒說", "agree": "甲|乙|都不對", "reason": "一兩句，引用原文關鍵句"}}"""
    r = subprocess.run(["claude", "-p", "--model", "opus", prompt], capture_output=True, text=True, timeout=900)
    v = parse(r.stdout)
    side = {"甲": ans[0][0], "乙": ans[1][0]}.get(v.get("agree"), "neither")
    return dict(key=k, owner=O[k]["owner"], verdict=v, sided_with=side, orig=O[k], blind=N[k])

with ThreadPoolExecutor(4) as ex:
    for res in ex.map(one, cases):
        with out_p.open("a", encoding="utf-8") as f:
            f.write(json.dumps(res, ensure_ascii=False) + "\n")
        print(res["key"], res["verdict"].get("fallback"), res["sided_with"], flush=True)
