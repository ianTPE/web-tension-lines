"""解鎖有／缺不一致的線，交給 Opus 依規則與原文仲裁。用法：adjudicate_unlock.py <子目錄> <盲判檔>"""
import json, re, subprocess, pathlib, glob, sys
from concurrent.futures import ThreadPoolExecutor
HERE = pathlib.Path(__file__).parent; ROOT = HERE.parents[2]
SUB, BLIND = sys.argv[1], sys.argv[2]
rule = re.search(r"4\. \*\*解鎖\*\*.*?(?=\n\n)", (ROOT / "PROMPT.md").read_text(encoding="utf-8"), re.S).group(0)
O = json.load(open(HERE / f"{SUB}-original.json"))
N = {json.loads(x)["key"]: json.loads(x) for x in open(HERE / SUB / BLIND) if x.strip()}
I = {x["key"]: x for f in sorted(glob.glob(str(HERE / SUB / "input-*.json"))) for x in json.load(open(f))}
miss = lambda s: s.strip().startswith("（缺）")
out_p = HERE / SUB / "adjudication-unlock.jsonl"
done = {json.loads(x)["key"] for x in out_p.read_text().splitlines()} if out_p.exists() else set()
cases = [k for k in O if k in N and miss(O[k]["unlock"]) != miss(N[k]["unlock"]) and k not in done]
print(len(cases), "unlock cases", flush=True)

def one(k):
    it = I[k]; cand = O[k]["unlock"] if not miss(O[k]["unlock"]) else N[k]["unlock"]
    guide = (ROOT / it["upstream"]).read_text(encoding="utf-8")
    prompt = f"""你是仲裁者。依規則與指南原文，判斷這條線的「解鎖」該是「有」還是「缺」。只根據指南原文。

規則：
{rule}

線：{it['title']}
做法：{it['action']}
對手：{it['opponent']}
類型：{it['kind']}
有人提出的解鎖句：{cand}

指南全文：
{guide}

這句解鎖能不能指回指南原文、說的是「以前做不到或很難、現在做得到」的具體一件事？若是，判「有」，並可微調成更貼原文的一句（60 字內）；若只是把做法換句話說、是常識性改善、或指不回原文，判「缺」。只輸出一行 JSON：{{"unlock": "有|缺", "text": "有的話給一句，缺就空字串", "reason": "一句"}}"""
    r = subprocess.run(["claude", "-p", "--model", "opus", prompt], capture_output=True, text=True, timeout=900)
    m = re.search(r"\{.*\}", r.stdout, re.S)
    try: v = json.loads(m.group(0)) if m else {}
    except json.JSONDecodeError:
        v = {"unlock": (re.search(r'"unlock"\s*:\s*"([^"]*)', r.stdout) or [None, ""])[1], "text": (re.search(r'"text"\s*:\s*"([^"]*)', r.stdout) or [None, ""])[1]}
    side = "orig" if (v.get("unlock") == "缺") == miss(O[k]["unlock"]) else "blind"
    return dict(key=k, owner=O[k].get("owner"), verdict=v, sided_with=side, orig=O[k]["unlock"], blind=N[k]["unlock"])

with ThreadPoolExecutor(4) as ex:
    for res in ex.map(one, cases):
        with out_p.open("a", encoding="utf-8") as f:
            f.write(json.dumps(res, ensure_ascii=False) + "\n")
        print(res["key"], res["verdict"].get("unlock"), res["sided_with"], flush=True)
