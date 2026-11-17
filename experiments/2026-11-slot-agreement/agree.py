"""判讀一致率：類別欄位算 Cohen's kappa，文字欄位比較兩邊寫的意思是否相同。
用法：agree.py <rater A 檔名尾> <rater B 檔名尾>，例如 agree.py claude kimi
原本寫線的 Opus（ledger）當第三個判讀者 ledger。"""
import csv, json, re, sys, pathlib, collections
import numpy as np
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "2026-11-line-retrieval"))
from voyage import embed

def ratings(name):
    if name == "ledger":
        R = {r["line_id"]: r for r in csv.DictReader(open(HERE.parents[1] / "ledger.csv", encoding="utf-8", newline=""))}
        out = {}
        for p in (HERE.parents[1] / "lines").glob("*/*.md"):
            for lid, body in re.findall(r'%% line-start id="([^"]+)" %%\n(.*?)%% line-end %%', p.read_text(encoding="utf-8"), re.S):
                if lid in R:
                    r = R[lid]; who = re.search(r"^- 誰在做：(.+)$", body, re.M)
                    out[lid] = dict(actor="開發者" if who and who.group(1).startswith("開發者") else (who.group(1) if who else ""),
                                    kind=r["類型"], opponent_present=r["槽3"], opponent=r["對手"], support=r["支援狀態"],
                                    outcome=r["戰報"], outcome_derived=r["戰報"], unlock_present="有" if r["解鎖"].strip() else "缺", unlock=r["解鎖"])
        return out
    return {json.loads(x)["key"]: json.loads(x) for x in (HERE / f"ratings-{name}.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()}

def norm(f, v):
    v = (v or "").strip()
    if f == "actor": return "開發者" if v.startswith("開發者") else "其他"
    return v

def kappa(a, b):
    n = len(a); cats = sorted(set(a) | set(b))
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = collections.Counter(a), collections.Counter(b)
    pe = sum(ca[c] * cb[c] for c in cats) / n / n
    return po, (po - pe) / (1 - pe) if pe < 1 else float("nan")

CAT = ["actor", "kind", "opponent_present", "support", "outcome", "effect_claim", "fallback", "outcome_derived", "cost_present", "unlock_present"]
TXT = [("opponent", "opponent_present"), ("cost", "cost_present"), ("fallback_text", "fallback"), ("unlock", "unlock_present")]

def derive(r):
    """v2：由三個小判斷依規則推出戰報。"""
    if "effect_claim" not in r: return r
    s, f = r.get("support", ""), r.get("fallback", "")
    if r["effect_claim"] == "缺": o = "缺"
    elif s in ("Widely", "不適用"): o = "勝"
    elif s == "Newly" or f == "保住主要行為": o = "部分改善"
    else: o = "僵持"
    return dict(r, outcome_derived=o)

def compare(na, nb, inp="input.json"):
    A, B = ratings(na), ratings(nb)
    A = {k: derive(v) for k, v in A.items()}; B = {k: derive(v) for k, v in B.items()}
    keys = sorted(set(A) & set(B) & {it["key"] for it in json.loads((HERE / inp).read_text())["items"]})
    rows = [f"### {na} vs {nb}（{len(keys)} 題）", "", "| 欄位 | 一致率 | kappa | 分布 {} | 分布 {} |".format(na, nb), "|---|---|---|---|---|"]
    for f in CAT:
        if not all(f in A[k] and f in B[k] for k in keys): continue
        a = [norm(f, A[k][f]) for k in keys]; b = [norm(f, B[k][f]) for k in keys]
        po, k_ = kappa(a, b)
        dist = lambda xs: "、".join(f"{c} {n}" for c, n in collections.Counter(xs).most_common())
        rows.append(f"| {f} | {po:.2f} | {k_:.2f} | {dist(a)} | {dist(b)} |")
    for f, gate in TXT:
        both = [k for k in keys if f in A[k] and f in B[k] and A[k].get(f, "").strip() and B[k].get(f, "").strip()]
        if len(both) < 5: continue
        va = np.array(embed([A[k][f] for k in both], "document")); vb = np.array(embed([B[k][f] for k in both], "document"))
        va /= np.linalg.norm(va, axis=1, keepdims=True); vb /= np.linalg.norm(vb, axis=1, keepdims=True)
        S = va @ vb.T; diag = np.diag(S)
        auc = np.mean([(diag[i] > np.delete(S[i], i)).mean() for i in range(len(both))])
        rows.append(f"| {f}（文字，{len(both)} 題兩邊都有寫） | 同題相似度 {diag.mean():.2f}，不同題 {S[~np.eye(len(both), dtype=bool)].mean():.2f} | 配對 AUC {auc:.2f} | | |")
    return "\n".join(rows) + "\n"

if __name__ == "__main__":
    print(compare(sys.argv[1], sys.argv[2], *(sys.argv[3:4])))
