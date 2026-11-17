"""抽線方式的檢索對照實驗。

任務 B（找答案）：150 條線 × 兩種查詢（symptom／goal），查詢由 Haiku 從上游英文原文生成。
任務 A（找同形狀）：每條線當查詢，同對手組、不同指南的線算相關。
"""
import json, re, sys, collections, pathlib
import numpy as np
from lines import load, guide_text
from voyage import embed, rerank

HERE = pathlib.Path(__file__).parent
L = load()
ID = {l["id"]: i for i, l in enumerate(L)}
Q = [json.loads(x) for x in open(HERE / "queries.jsonl", encoding="utf-8")]
Q = [q for q in Q if q["id"] in ID]

noquote = lambda s: re.sub(r'（?引用：[「"].+?[」"]）?', "", s)
REPS = {
    "完整線（現行）":       lambda l: l["block"],
    "完整線去英文引文":     lambda l: noquote(l["block"]),
    "四槽":                lambda l: "\n".join([l["action"], l["blocker"], l["outcome"]]),
    "只有被什麼擋":         lambda l: l["blocker"],
    "只有英文引文":         lambda l: l["quote"] or l["blocker"],
    "只有標題":            lambda l: l["title"],
    "標題＋被什麼擋":       lambda l: l["title"] + "\n" + l["blocker"],
    "動作＋被什麼擋":       lambda l: l["action"] + "\n" + l["blocker"],
    "只有經過":            lambda l: l["story"] or l["blocker"],
    "完整線＋解鎖":         lambda l: l["block"] + ("\n解鎖：" + l["unlock"] if l["unlock"] else ""),
}

def unit(m):
    m = np.asarray(m, dtype=np.float32); return m / np.linalg.norm(m, axis=1, keepdims=True)

V = {name: unit(embed([f(l) for l in L], "document")) for name, f in REPS.items()}

# 不抽線的基準：整份上游指南、依 ## 標題切塊
guides = sorted({l["guide"] for l in L})
GV = unit(embed([guide_text(g)[:60000] for g in guides], "document", batch=8))
chunks, chunk_guide = [], []
for g in guides:
    for c in re.split(r"\n(?=## )", guide_text(g)):
        if len(c.strip()) > 80:
            chunks.append(c[:12000]); chunk_guide.append(g)
CV = unit(embed(chunks, "document", batch=32))
print(f"{len(L)} lines, {len(guides)} guides, {len(chunks)} chunks, {len(Q)} queries", file=sys.stderr)

line_guide = np.array([l["guide"] for l in L])

def line_metrics(ranks):
    r = np.array(ranks)
    return dict(R1=(r <= 1).mean(), R5=(r <= 5).mean(), R10=(r <= 10).mean(), MRR=(1 / r).mean())

def guide_rank(order_guides, gold):
    seen = []
    for g in order_guides:
        if g not in seen:
            seen.append(g)
            if g == gold:
                return len(seen)
    return len(guides)

results = {}
for kind in ("symptom", "goal"):
    QV = unit(embed([q[kind] for q in Q], "query"))
    gold = [ID[q["id"]] for q in Q]
    rows = {}
    for name, M in V.items():
        S = QV @ M.T
        order = np.argsort(-S, axis=1)
        lr = [int(np.where(order[i] == g)[0][0]) + 1 for i, g in enumerate(gold)]
        gr = [guide_rank(line_guide[order[i]], L[g]["guide"]) for i, g in enumerate(gold)]
        rows[name] = dict(line=line_metrics(lr), guide=line_metrics(gr), order=order, lr=lr, gr=gr)
    for name, M, owner in (("不抽線：整份指南", GV, np.array(guides)), ("不抽線：依標題切塊", CV, np.array(chunk_guide))):
        order = np.argsort(-(QV @ M.T), axis=1)
        gr = [guide_rank(owner[order[i]], L[g]["guide"]) for i, g in enumerate(gold)]
        rows[name] = dict(line=None, guide=line_metrics(gr), gr=gr)
    # 重排：用現行完整線的前 30 名，交給 rerank-2.5
    for base in ("完整線（現行）", "標題＋被什麼擋"):
        lr, gr = [], []
        for i, g in enumerate(gold):
            top = list(rows[base]["order"][i][:30])
            rr = rerank(Q[i][kind], [L[j]["block"] for j in top])
            new = [top[k] for k, _ in rr] + [j for j in rows[base]["order"][i][30:]]
            lr.append(new.index(g) + 1)
            gr.append(guide_rank(line_guide[new], L[g]["guide"]))
        rows[f"{base} → 重排前 30"] = dict(line=line_metrics(lr), guide=line_metrics(gr), lr=lr, gr=gr)
    results[kind] = rows

# 任務 A：找同形狀
grp = np.array([l["group"] for l in L])
A = {}
for name, M in V.items():
    S = M @ M.T
    aps, aucs = [], []
    for i in range(len(L)):
        mask = line_guide != line_guide[i]          # 只比不同指南的線
        rel = (grp == grp[i]) & mask
        if rel.sum() == 0:
            continue
        s = S[i][mask]; y = rel[mask]
        order = np.argsort(-s); y_sorted = y[order]
        hits = np.cumsum(y_sorted)
        aps.append((hits[y_sorted] / (np.where(y_sorted)[0] + 1)).mean())
        pos, neg = s[y], s[~y]
        aucs.append((pos[:, None] > neg[None, :]).mean())
    A[name] = dict(MAP=float(np.mean(aps)), AUC=float(np.mean(aucs)), n=len(aps))

def fmt(m): return "—" if m is None else f'{m["R1"]:.2f} / {m["R5"]:.2f} / {m["R10"]:.2f} / {m["MRR"]:.2f}'
out = []
for kind, title in (("symptom", "找答案：描述症狀"), ("goal", "找答案：描述想做的東西")):
    out.append(f"\n## {title}（{len(Q)} 題）\n\n| 抽法 | 找到那一條線 R@1 / R@5 / R@10 / MRR | 找到對的指南 R@1 / R@5 / R@10 / MRR |\n|---|---|---|")
    for name, r in sorted(results[kind].items(), key=lambda kv: -kv[1]["guide"]["MRR"]):
        out.append(f"| {name} | {fmt(r['line'])} | {fmt(r['guide'])} |")
out.append(f"\n## 找同形狀（同對手組、不同指南）\n\n| 抽法 | MAP | AUC |\n|---|---|---|")
for name, r in sorted(A.items(), key=lambda kv: -kv[1]["MAP"]):
    out.append(f"| {name} | {r['MAP']:.3f} | {r['AUC']:.3f} |")
import pickle
pickle.dump({k: {n: {kk: vv for kk, vv in r.items() if kk in ("lr", "gr")} for n, r in rows_.items()} for k, rows_ in results.items()}, open(HERE / "ranks.pkl", "wb"))
text = "\n".join(out)
(HERE / "results.md").write_text(text + "\n", encoding="utf-8")
print(text)
