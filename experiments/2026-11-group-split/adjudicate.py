"""對手組歸類不一致的線，交給 Opus 匿名仲裁。"""
import json, random, re, subprocess, pathlib
from concurrent.futures import ThreadPoolExecutor
HERE = pathlib.Path(__file__).parent
M = json.load(open(HERE / "merged.json"))
REN = {"沒偵測就呼叫新功能": "沒防護不支援的瀏覽器"}
for side in ("kimi", "agy"):
    for v in M[side].values(): v["group"] = REN.get(v["group"], v["group"])
json.dump(M, open(HERE / "merged.json", "w"), ensure_ascii=False, indent=1)
inp = json.load(open(HERE / "input.json")); I = {x["key"]: x for x in inp["items"]}
NEW = {"沒防護不支援的瀏覽器": "不支援新功能的瀏覽器忽略屬性或沒有該 API，沒有偵測或退路，功能因此壞掉或沒反應",
       "瀏覽器實作有缺陷": "某個瀏覽器的實作 bug 讓照規格寫的程式出錯，需要針對性繞路",
       "兩套機制重複作用": "同一件事同時用兩種機制宣告或註冊，結果重複觸發或互相抵消",
       "相對網址解析基準錯": "相對網址相對於錯的檔案解析，指到錯的資源",
       "邏輯方向與實體方向脫鉤": "一部分跟著書寫方向（邏輯方向），另一部分用實體方向，RTL 時對不上"}
groups = "\n".join(f"- {g['name']}（{g['count']} 條）：例 {'；'.join(g['examples'][:2])}" for g in inp["existing_groups"])
cands = "\n".join(f"- {c['name']}：{c['definition']}" for c in inp["candidate_new_groups"]) + "\n" + "\n".join(f"- {k}：{v}" for k, v in NEW.items())
def one(k):
    a = [M["kimi"][k]["group"], M["agy"][k]["group"]]; random.Random(k).shuffle(a)
    it = I[k]
    prompt = f"""你是仲裁者。對手組描述的是「舊做法或錯誤用法在哪裡出事」的共同形狀：不同功能，只要出事的機制相同就是同一組。請判斷這條線該歸哪一組。

線：{it['title']}
做法：{it['action']}
對手：{it['opponent']}
經過：{it['story']}

兩個判讀者的答案：甲「{a[0]}」、乙「{a[1]}」

現有的組：
{groups}

新組（定義）：
{cands}

優先選甲或乙；兩者都明顯不對才選其他組。只輸出一行 JSON：{{"group": "組名", "agree": "甲|乙|都不對", "reason": "一句"}}"""
    out = subprocess.run(["claude", "-p", "--model", "opus", prompt], capture_output=True, text=True, timeout=900).stdout
    m = re.search(r"\{.*\}", out, re.S)
    try: v = json.loads(m.group(0))
    except Exception: v = {"group": (re.search(r'"group"\s*:\s*"([^"]*)', out) or [None, ""])[1], "agree": "", "reason": out[-200:]}
    side = {"甲": a[0], "乙": a[1]}.get(v.get("agree"))
    v["sided"] = "kimi" if side == M["kimi"][k]["group"] else "agy" if side == M["agy"][k]["group"] else "neither"
    return k, v
res = {}
with ThreadPoolExecutor(4) as ex:
    for k, v in ex.map(one, M["dis"]):
        res[k] = v; print(k, v.get("group"), v["sided"], flush=True)
json.dump(res, open(HERE / "adjudication.json", "w"), ensure_ascii=False, indent=1)
