#!/usr/bin/env python3
"""檢查線檔、ledger.csv、i18n/en.json 是否符合槽 v2，並核對引文逐字出自上游指南。

用法：
  python3 scripts/check_lines.py                 全部檢查
  python3 scripts/check_lines.py lines/a/b.md …  只檢查這些線檔的格式與規則（不檢查 ledger 與 i18n）
"""
import csv, json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
UP = ROOT / ".cache/upstream/skills/modern-web-guidance/guides"
SLOTS = ["做法", "對手", "退路", "解鎖"]
OLD_SLOTS = ["誰在做", "動作＋對象", "被什麼擋", "戰報"]
FALLBACK = ["不需要", "保住主要行為", "失去主要好處", "沒說"]
LEVELS = ["Widely", "Newly", "Limited", "無瀏覽器支援", "不適用"]
HEADER = "日期,版本,guide_id,line_id,功能,對手組,對手有無,對手,退路,戰報,支援狀態,證據,類型,解鎖,發想,狀態".split(",")
LINE_RE = re.compile(r'%% line-start id="([^"]+)" %%\n(.*?)%% line-end %%\n(.*?)(?=%% line-start|\Z)', re.S)

errors = []
def err(where, msg): errors.append(f"{where}: {msg}")

def derive(level, fallback):
    if level in ("Widely", "不適用"): return "勝"
    if level == "Newly" or fallback == "保住主要行為": return "部分改善"
    return "僵持"

def norm(s):
    s = re.sub(r"\n\s*//\s*", " ", re.sub(r"</?kbd>", "", s))
    return re.sub(r"\s+", " ", re.sub(r"[`*]", "", s.replace("’", "'").replace("“", '"').replace("”", '"'))).strip()

def quote_ok(q, src):
    if norm(q) in src: return True
    parts = [norm(x) for x in re.split(r"\s*(?:…|\.\.\.)\s*", q) if x.strip()]
    return len(parts) > 1 and all(p in src for p in parts)

def read_lines(paths):
    out = {}
    for p in paths:
        text = p.read_text(encoding="utf-8")
        if "%% line-start" not in text: continue
        rel = p.relative_to(ROOT)
        upstream = UP / p.parent.name / p.name
        src = norm(upstream.read_text(encoding="utf-8")) if upstream.exists() else None
        for lid, body, detail in LINE_RE.findall(text):
            w = f"{rel} {lid}"
            slots = dict(re.findall(r"^- ([^：\n]+)：(.+)$", body, re.M))
            det = dict(re.findall(r"^- ([^：\n]+)：(.+)$", detail.split("%% line-start")[0], re.M))
            for s in OLD_SLOTS:
                if s in slots: err(w, f"線內還有舊槽「{s}」")
            for s in SLOTS:
                if not slots.get(s, "").strip(): err(w, f"缺少槽「{s}」")
            if not re.search(r"^## .+", body, re.M): err(w, "缺少 ## 標題")
            if not re.search(r"^經過：.+", body, re.M): err(w, "缺少「經過：」")
            fb = slots.get("退路", "")
            m = re.match(r"(" + "|".join(FALLBACK) + r")——(.+)", fb)
            if not m: err(w, f"退路格式不對（要「分類——一句」）：{fb[:40]}")
            unlock = slots.get("解鎖", "").strip()
            opp = slots.get("對手", "")
            if src is not None:
                for q in re.findall(r'引用：[「"](.+?)[」"]）\s*$', opp, re.M):
                    if not quote_ok(q, src): err(w, f"引文對不上上游原文：{q[:60]}")
            if "解鎖（發想，非指南原文）" in det: err(w, "細節還是舊的「解鎖（發想…）」，要改成「發想（非指南原文）」")
            if not re.match(r"(勝|部分改善|僵持)（由支援狀態與退路推出）$", det.get("戰報", "")): err(w, f"細節的戰報格式不對：{det.get('戰報', '')[:30]}")
            if "TODO" in body + detail.split("%% line-start")[0]: err(w, "還有 TODO")
            if not unlock: err(w, "解鎖空白")
            if unlock and not unlock.startswith("（缺）") and len(unlock) < 8: err(w, f"解鎖太短：{unlock}")
            sj = det.get("槽判定", "")
            if sj != f"對手 {'缺' if opp.startswith('（缺）') else '有'}／解鎖 {'缺' if unlock.startswith('（缺）') else '有'}": err(w, f"槽判定與槽內容不符：{sj}")
            out[lid] = dict(where=w, fallback=m.group(1) if m else None, verdict=re.match(r"(勝|部分改善|僵持)", det.get("戰報", "")),
                            opp_missing=opp.startswith("（缺）"), unlock_missing=unlock.startswith("（缺）"),
                            support_detail=det.get("支援狀態", ""), group=det.get("對手組", ""))
    return out

def check_ledger(lines):
    rows = list(csv.reader(open(ROOT / "ledger.csv", encoding="utf-8", newline="")))
    if rows[0] != HEADER:
        err("ledger.csv", f"欄位不對：{rows[0]}"); return {}
    led = {}
    for i, r in enumerate(rows[1:], 2):
        if len(r) != len(HEADER): err(f"ledger.csv:{i}", f"欄位數 {len(r)}"); continue
        d = dict(zip(HEADER, r))
        if d["line_id"] in led: err(f"ledger.csv:{i}", f"line_id 重複 {d['line_id']}")
        led[d["line_id"]] = d
        w = f"ledger {d['line_id']}"
        if d["狀態"] != "有效": continue
        if d["支援狀態"] not in LEVELS: err(w, f"支援狀態 {d['支援狀態']}")
        if d["退路"] not in FALLBACK: err(w, f"退路 {d['退路']}")
        if d["戰報"] != derive(d["支援狀態"], d["退路"]): err(w, f"戰報 {d['戰報']} 與規則推出的 {derive(d['支援狀態'], d['退路'])} 不符")
        if (d["退路"] == "不需要") != (d["支援狀態"] in ("Widely", "不適用")): err(w, f"退路 {d['退路']} 與支援狀態 {d['支援狀態']} 不搭")
        if d["對手有無"] not in ("有", "缺"): err(w, f"對手有無 {d['對手有無']}")
        if d["類型"] not in ("新能力", "糾錯"): err(w, f"類型 {d['類型']}")
        l = lines.get(d["line_id"])
        if not l: err(w, "找不到對應的線"); continue
        if l["fallback"] and l["fallback"] != d["退路"]: err(w, f"退路與線檔不同（線檔 {l['fallback']}）")
        if l["verdict"] and l["verdict"].group(1) != d["戰報"]: err(w, f"戰報與線檔細節不同（線檔 {l['verdict'].group(1)}）")
        if l["opp_missing"] != (d["對手有無"] == "缺"): err(w, "對手有無與線檔的（缺）不一致")
        if l["group"] and l["group"] != d["對手組"]: err(w, f"對手組與線檔不同（線檔 {l['group']}）")
        if l["unlock_missing"] != (d["解鎖"].strip() == ""): err(w, "解鎖是否留空與線檔不一致")
    for lid in lines:
        if lid not in led: err(lid, "ledger 沒有這條線")
    return led

def check_i18n(led):
    en = json.load(open(ROOT / "i18n/en.json", encoding="utf-8"))
    for k in FALLBACK:
        if k not in en.get("fallback", {}): err("i18n", f"fallback 對照缺 {k}")
    if "缺" in en.get("result", {}): err("i18n", "result 對照還有「缺」")
    want = {"title", "action", "opponent", "fallback", "unlock", "idea", "story", "support"}
    for lid, d in led.items():
        if d["狀態"] != "有效": continue
        e = en["lines"].get(lid)
        if e is None: err(f"i18n {lid}", "沒有譯文"); continue
        if set(e) != want: err(f"i18n {lid}", f"欄位 {sorted(set(e) ^ want)} 不對")
        elif not e["fallback"].strip(): err(f"i18n {lid}", "fallback 空白")
        elif bool(e["unlock"].strip()) != bool(d["解鎖"].strip()): err(f"i18n {lid}", "unlock 是否留空與 ledger 不一致")

if __name__ == "__main__":
    args = [ROOT / a if not pathlib.Path(a).is_absolute() else pathlib.Path(a) for a in sys.argv[1:]]
    lines = read_lines(args or sorted((ROOT / "lines").glob("*/*.md")))
    if not args:
        led = check_ledger(lines)
        if led: check_i18n(led)
    for e in errors[:80]: print("✗", e)
    if len(errors) > 80: print(f"…另有 {len(errors) - 80} 個錯誤")
    print(f"{len(lines)} 條線，{len(errors)} 個錯誤")
    sys.exit(1 if errors else 0)
