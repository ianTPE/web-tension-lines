"""Voyage embeddings / rerank，結果快取在 repo 的 .cache/retrieval/（不進 git）。"""
import hashlib, json, os, time, urllib.request, urllib.error, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
CACHE = ROOT / ".cache/retrieval"; CACHE.mkdir(parents=True, exist_ok=True)
KEY = os.environ.get("VOYAGE_API_KEY") or next(
    l.split("=", 1)[1].strip().strip('"\'') for l in (ROOT / ".env").read_text().splitlines() if l.startswith("VOYAGE_API_KEY="))


def _post(path, payload):
    for i in range(8):
        req = urllib.request.Request("https://api.voyageai.com/v1/" + path, json.dumps(payload).encode(),
                                     {"Authorization": f"Bearer {KEY}", "content-type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and i < 7:
                time.sleep(2 ** i); continue
            raise RuntimeError(f"{e.code} {e.read()[:300]}")


def _load(name):
    p = CACHE / name
    return json.loads(p.read_text()) if p.exists() else {}


def embed(texts, input_type, model="voyage-3.5", batch=64):
    name = f"emb-{model}-{input_type}.json"
    cache = _load(name)
    h = lambda t: hashlib.sha1(t.encode()).hexdigest()
    todo = list({h(t): t for t in texts if h(t) not in cache}.items())
    for i in range(0, len(todo), batch):
        part = todo[i:i + batch]
        d = _post("embeddings", {"model": model, "input": [t for _, t in part], "input_type": input_type})
        for (k, _), row in zip(part, d["data"]):
            cache[k] = row["embedding"]
        (CACHE / name).write_text(json.dumps(cache))
    return [cache[h(t)] for t in texts]


def rerank(query, docs, model="rerank-2.5"):
    name = f"rerank-{model}.json"
    cache = _load(name)
    k = hashlib.sha1(json.dumps([query, docs]).encode()).hexdigest()
    if k not in cache:
        d = _post("rerank", {"model": model, "query": query, "documents": docs})
        cache[k] = [(r["index"], r["relevance_score"]) for r in d["data"]]
        cache_now = _load(name); cache_now[k] = cache[k]
        (CACHE / name).write_text(json.dumps(cache_now))
    return cache[k]
