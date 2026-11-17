"""反問測試計分：每個回答者（Haiku、Kimi、agy、kilo）各算一次，再看方向是否一致。"""
import json, sys, pathlib
import numpy as np
import ask

OUT = ask.OUT
ANSWERERS = {"haiku": "answers.jsonl", "kimi": "answers-kimi.jsonl", "agy": "answers-agy.jsonl", "kilo": "answers-kilo.jsonl"}
ARMS = ["direct", "generic", "raw_targeted", "slot_targeted", "full"]
FIELD = {"generic": "generic", "raw_targeted": "raw", "slot_targeted": "slot"}
items = {it["key"]: it for it in ask.S}
rng = np.random.default_rng(0)


def load(p):
    rows = {}
    for x in p.read_text(encoding="utf-8").splitlines():
        try:
            r = json.loads(x)
        except json.JSONDecodeError:
            continue
        if r.get("key") in items and all(r.get(k) for k in ("generic", "raw", "slot", "full")):
            rows[r["key"]] = r
    return rows


def ranks_for(ans):
    keys = sorted(ans)
    R = {a: [] for a in ARMS}
    for k in keys:
        it, a, g = items[k], ans[k], ask.ID[items[k]["id"]]
        R["direct"].append(it["rank"])
        for arm, f in FIELD.items():
            R[arm].append(ask.search(it["query"] + "\n" + a[f]).index(g) + 1)
        R["full"].append(ask.search(a["full"]).index(g) + 1)
    return keys, {a: np.array(v) for a, v in R.items()}


def ci(d):
    bs = [d[rng.integers(0, len(d), len(d))].mean() for _ in range(5000)]
    return np.percentile(bs, [2.5, 97.5])


lines = ["# 反問測試結果", "",
         f"100 題：70 題原本（完整線＋重排）沒排到第一，30 題原本就對。正確答案在前 8 名候選內的有 {sum(it['rank'] <= 8 for it in ask.S)} 題。", ""]
summary = {}
for who, fn in ANSWERERS.items():
    p = OUT / fn
    if not p.exists():
        continue
    ans = load(p)
    if len(ans) < 50:
        print(f"skip {who}: only {len(ans)} answers", file=sys.stderr); continue
    keys, R = ranks_for(ans)
    orig = np.array([items[k]["rank"] for k in keys])
    in8 = orig <= 8
    summary[who] = {a: R[a].tolist() for a in ARMS} | {"keys": keys}
    lines += [f"## 回答者：{who}（{len(keys)} 題）", "",
              "| 條件 | 第一名命中 | 前 5 命中 | MRR | 候選內（{}題）第一名 | 候選外（{}題）第一名 | 原本對的被弄錯 |".format(in8.sum(), (~in8).sum()),
              "|---|---|---|---|---|---|---|"]
    for a in ARMS:
        r = R[a]
        broke = int(((orig == 1) & (r > 1)).sum())
        lines.append(f"| {a} | {(r == 1).mean():.2f} | {(r <= 5).mean():.2f} | {(1 / r).mean():.3f} | "
                     f"{(r[in8] == 1).mean():.2f} | {(r[~in8] == 1).mean():.2f} | {broke}/{(orig == 1).sum()} |")
    lines += ["", "逐題比較（第一名命中的勝／負，MRR 差與 95% CI）：", ""]
    for a, b in (("slot_targeted", "direct"), ("raw_targeted", "direct"), ("generic", "direct"),
                 ("slot_targeted", "raw_targeted"), ("slot_targeted", "generic"), ("raw_targeted", "generic")):
        x, y = R[a] == 1, R[b] == 1
        d = 1 / R[a] - 1 / R[b]; lo, hi = ci(d)
        lines.append(f"- {a} vs {b}：勝 {int((x & ~y).sum())}、負 {int((y & ~x).sum())}；MRR {d.mean():+.3f} [{lo:+.3f}, {hi:+.3f}]")
    lines.append("")

json.dump(summary, open(OUT / "score.json", "w"), ensure_ascii=False)
(OUT / "results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
