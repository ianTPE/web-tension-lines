"""把仲裁結果套到線檔與譯文。用法：apply_fixes.py fixes.json
fixes.json：{line_id: {"fallback": [分類, 中文一句, 英文一句]} 或 {"unlock": [中文一句或（缺）, 英文一句或空字串]}}
戰報與槽判定由腳本依規則重算；之後要跑 rebuild_ledger.py 與 check_lines.py。"""
import re, csv, json, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]
FIX = json.load(open(sys.argv[1], encoding="utf-8"))
R = {r["line_id"]: r for r in csv.DictReader(open(ROOT / "ledger.csv", encoding="utf-8", newline=""))}
def derive(lv, fb): return "勝" if lv in ("Widely", "不適用") else "部分改善" if (lv == "Newly" or fb == "保住主要行為") else "僵持"
en = json.load(open(ROOT / "i18n/en.json", encoding="utf-8"))
done = set()
for p in (ROOT / "lines").glob("*/*.md"):
    t = p.read_text(encoding="utf-8"); orig = t
    for lid, f in FIX.items():
        m = re.search(rf'(%% line-start id="{re.escape(lid)}" %%\n.*?)(?=%% line-start|\Z)', t, re.S)
        if not m: continue
        seg = new = m.group(1); notes = []
        if "fallback" in f:
            cat, zh, e = f["fallback"]
            new = re.sub(r"^- 退路：.+$", f"- 退路：{cat}——{zh}", new, count=1, flags=re.M)
            new = re.sub(r"^- 戰報：.+$", f"- 戰報：{derive(R[lid]['支援狀態'], cat)}（由支援狀態與退路推出）", new, count=1, flags=re.M)
            en["lines"][lid]["fallback"] = e; notes.append(f"退路改為「{cat}」")
        if "unlock" in f:
            zh, e = f["unlock"]
            new = re.sub(r"^- 解鎖：.+$", f"- 解鎖：{zh}", new, count=1, flags=re.M)
            en["lines"][lid]["unlock"] = e; notes.append("解鎖改為" + ("缺" if zh.startswith("（缺）") else "有"))
        opp = re.search(r"^- 對手：(.+)$", new, re.M).group(1); un = re.search(r"^- 解鎖：(.+)$", new, re.M).group(1)
        new = re.sub(r"^- 槽判定：.+$", f"- 槽判定：對手 {'缺' if opp.startswith('（缺）') else '有'}／解鎖 {'缺' if un.startswith('（缺）') else '有'}", new, count=1, flags=re.M)
        new = re.sub(r"^(- 變更紀錄：.+)$", rf"\1；2026-11-18 交叉核對仲裁：{'、'.join(notes)}", new, count=1, flags=re.M)
        t = t.replace(seg, new); done.add(lid)
    if t != orig: p.write_text(t, encoding="utf-8")
missing = set(FIX) - done
json.dump(en, open(ROOT / "i18n/en.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(ROOT / "i18n/en.json", "a").write("\n")
print(f"套用 {len(done)} 條" + (f"；找不到 {missing}" if missing else ""))
