"""Claude（Opus）依判讀表判讀，輸出 ratings-<name>.jsonl。用法：rate_claude.py <codebook> <name>"""
import json, subprocess, sys, pathlib
HERE = pathlib.Path(__file__).parent
book = (HERE / sys.argv[1]).read_text(encoding="utf-8"); name = sys.argv[2]
d = json.loads((HERE / (sys.argv[3] if len(sys.argv) > 3 else "input.json")).read_text())
out = HERE / f"ratings-{name}.jsonl"
have = {json.loads(x)["key"] for x in out.read_text().splitlines()} if out.exists() else set()
todo = [it for it in d["items"] if it["key"] not in have]
FIELDS = ("kind", "opponent_present", "support", "unlock_present")
for rnd in range(3):
    for b in range(0, len(todo), 6):
        batch = todo[b:b + 6]
        gs = list(dict.fromkeys(it["guide"] for it in batch))
        body = "\n\n".join(f"===== 指南 {g} 全文 =====\n{d['guides'][g]}" for g in gs)
        tasks = "\n".join(f'- key: {it["key"]}｜指南：{it["guide"]}｜目標功能：{it["target_feature"]}｜原文句：{it["target_quote"]}' for it in batch)
        prompt = f"{book}\n\n## 指南全文\n\n{body}\n\n## 要判的題目（{len(batch)} 題）\n\n{tasks}\n\n只輸出 JSON 行。"
        r = subprocess.run(["claude", "-p", "--model", "opus", prompt], capture_output=True, text=True, timeout=1200)
        keys = {it["key"] for it in batch}
        with out.open("a", encoding="utf-8") as f:
            for line in r.stdout.splitlines():
                line = line.strip()
                if not line.startswith("{"): continue
                try: x = json.loads(line)
                except json.JSONDecodeError: continue
                if x.get("key") in keys and x["key"] not in have and all(k in x for k in FIELDS):
                    have.add(x["key"]); f.write(json.dumps(x, ensure_ascii=False) + "\n")
        print(f"{name}: {len(have)}/{len(d['items'])}", file=sys.stderr, flush=True)
    todo = [it for it in d["items"] if it["key"] not in have]
    if not todo: break
