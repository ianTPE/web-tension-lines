#!/usr/bin/env python3
"""從線檔與現有 ledger.csv 重建槽 v2 欄位的 ledger.csv（可重複執行）。"""
import csv
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FALLBACK = ("不需要", "保住主要行為", "失去主要好處", "沒說")
NEW_HEADER = [
    "日期", "版本", "guide_id", "line_id", "功能", "對手組", "對手有無",
    "對手", "退路", "戰報", "支援狀態", "證據", "類型", "解鎖", "發想", "狀態",
]
LINE_RE = re.compile(
    r'%% line-start id="([^"]+)" %%\n(.*?)%% line-end %%\n',
    re.S,
)


def derive(level: str, fallback: str) -> str:
    """由支援狀態與退路推出戰報，對齊 check_lines.py 規則。"""
    if level in ("Widely", "不適用"):
        return "勝"
    if level == "Newly" or fallback == "保住主要行為":
        return "部分改善"
    return "僵持"


def parse_lines() -> dict[str, dict]:
    """讀取所有線檔的對手有無、退路分類與解鎖文字。"""
    parsed: dict[str, dict] = {}
    for p in sorted((ROOT / "lines").glob("*/*.md")):
        text = p.read_text(encoding="utf-8")
        for lid, body in LINE_RE.findall(text):
            slots = dict(re.findall(r"^- ([^：\n]+)：(.+)$", body, re.M))
            fb_raw = slots.get("退路", "").strip()
            m = re.match(r"(" + "|".join(FALLBACK) + r")——(.+)", fb_raw)
            if not m:
                raise ValueError(f"{p.relative_to(ROOT)} {lid}: 無法解析退路「{fb_raw}」")
            unlock_raw = slots.get("解鎖", "").strip()
            unlock = "" if unlock_raw.startswith("（缺）") else unlock_raw
            opp = slots.get("對手", "").strip()
            parsed[lid] = {
                "fallback": m.group(1),
                "unlock": unlock,
                "opp_missing": opp.startswith("（缺）"),
            }
        # 對手組以線檔細節為準
        for lid, detail in re.findall(r'%% line-start id="([^"]+)" %%.*?%% line-end %%\n(.*?)(?=%% line-start|\Z)', text, re.S):
            g = re.search(r"^- 對手組：(.+)$", detail, re.M)
            if lid in parsed and g:
                parsed[lid]["group"] = g.group(1).strip()
    return parsed


def main() -> int:
    lines = parse_lines()
    ledger_path = ROOT / "ledger.csv"
    with ledger_path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    if not rows:
        print("✗ ledger.csv 為空", file=sys.stderr)
        return 1

    old_header = rows[0]
    is_v2 = "發想" in old_header and "退路" in old_header
    out_rows = [NEW_HEADER]
    missing = []

    for row in rows[1:]:
        d = dict(zip(old_header, row))
        lid = d["line_id"]
        info = lines.get(lid)
        if info is None:
            missing.append(lid)
            continue

        opp_exists = "缺" if info["opp_missing"] else "有"
        fallback = info["fallback"]
        level = d["支援狀態"]
        verdict = derive(level, fallback)
        unlock = info["unlock"]
        idea = d["發想"] if is_v2 else d["解鎖"]

        out_rows.append([
            d["日期"],
            d["版本"],
            d["guide_id"],
            lid,
            d["功能"],
            info.get("group") or d["對手組"],
            opp_exists,
            d["對手"],
            fallback,
            verdict,
            level,
            d["證據"],
            d["類型"],
            unlock,
            idea,
            d["狀態"],
        ])

    if missing:
        print(f"✗ 線檔中找不到 {len(missing)} 條：{missing[:5]}", file=sys.stderr)
        return 1

    with ledger_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(out_rows)

    print(f"✓ 已重建 ledger.csv：{len(out_rows) - 1} 條線（{len(NEW_HEADER)} 欄）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
