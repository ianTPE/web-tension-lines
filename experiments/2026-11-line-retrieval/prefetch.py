"""平行預先算好所有回答者需要的重排結果，寫進同一份快取，讓 score_ask.py 只讀快取。"""
import json, hashlib, sys
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import ask, voyage
from score_ask import ANSWERERS, FIELD, load, items

texts = []
for who, fn in ANSWERERS.items():
    p = ask.OUT / fn
    if not p.exists():
        continue
    for k, a in load(p).items():
        q = items[k]["query"]
        texts += [q + "\n" + a[f] for f in FIELD.values()] + [a["full"]]
texts = list(dict.fromkeys(texts))
qv = ask.unit(voyage.embed(texts, "query"))          # 一次批次嵌入
name = "rerank-rerank-2.5.json"
cache = voyage._load(name)
jobs = []
for t, v in zip(texts, qv):
    top = list(np.argsort(-(ask.DV @ v))[:30])
    docs = [ask.DOCS[j] for j in top]
    k = hashlib.sha1(json.dumps([t, docs]).encode()).hexdigest()
    if k not in cache:
        jobs.append((k, t, docs))
print(f"{len(texts)} texts, {len(jobs)} reranks to fetch", file=sys.stderr, flush=True)

def one(job):
    k, t, docs = job
    d = voyage._post("rerank", {"model": "rerank-2.5", "query": t, "documents": docs})
    return k, [(r["index"], r["relevance_score"]) for r in d["data"]]

done = 0
with ThreadPoolExecutor(8) as ex:
    for k, v in ex.map(one, jobs):
        cache[k] = v; done += 1
        if done % 100 == 0:
            print(f"  {done}/{len(jobs)}", file=sys.stderr, flush=True)
(voyage.CACHE / name).write_text(json.dumps(cache))
print("done", file=sys.stderr)
