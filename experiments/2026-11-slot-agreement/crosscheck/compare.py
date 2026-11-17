"""比對盲測結果和原判讀：退路分類一致率、kappa、解鎖有／缺一致率，列出不一致的線。"""
import json, sys, collections
orig, new, name_o, name_n = sys.argv[1:5]
O = json.load(open(orig, encoding="utf-8"))
N = {json.loads(x)["key"]: json.loads(x) for x in open(new, encoding="utf-8") if x.strip()}
keys = [k for k in O if k in N]
def kappa(a, b):
    n = len(a); po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = collections.Counter(a), collections.Counter(b)
    pe = sum(ca[c] * cb[c] for c in set(a) | set(b)) / n / n
    return po, (po - pe) / (1 - pe)
a = [O[k]["fallback"] for k in keys]; b = [N[k]["fallback"] for k in keys]
po, k_ = kappa(a, b)
ua = ["缺" if O[k]["unlock"].startswith("（缺）") else "有" for k in keys]
ub = ["缺" if N[k]["unlock"].strip().startswith("（缺）") else "有" for k in keys]
pu, ku = kappa(ua, ub)
print(f"{len(keys)} 題｜退路一致 {po:.2f}（kappa {k_:.2f}）｜解鎖有缺一致 {pu:.2f}（kappa {ku:.2f}）")
print("退路（原 → 盲測）:", collections.Counter((x, y) for x, y in zip(a, b) if x != y).most_common())
for k in keys:
    if O[k]["fallback"] != N[k]["fallback"]:
        print(f"\n{k}\n  {name_o}: {O[k]['fallback_text'][:140]}\n  {name_n}: {N[k]['fallback']}——{N[k]['fallback_text'][:120]}")
for k, x, y in zip(keys, ua, ub):
    if x != y:
        print(f"\n[解鎖] {k}\n  {name_o}: {O[k]['unlock'][:110]}\n  {name_n}: {N[k]['unlock'][:110]}")
