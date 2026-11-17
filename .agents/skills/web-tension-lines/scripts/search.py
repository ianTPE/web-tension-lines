#!/usr/bin/env python3
"""依症狀、對手或功能檢索問題線，不需要第三方套件。"""
import argparse
import csv
import json
import pathlib
import re


def find_root():
    for parent in pathlib.Path(__file__).resolve().parents:
        if (parent / "ledger.csv").is_file() and (parent / "lines").is_dir():
            return parent
    raise SystemExit("找不到 ledger.csv 與 lines/；請確認 skill 位於 web-tension-lines 專案內。")


def load_data(root):
    with (root / "ledger.csv").open(encoding="utf-8", newline="") as f:
        ledger = {r["line_id"]: r for r in csv.DictReader(f)}
    en = json.loads((root / "i18n" / "en.json").read_text(encoding="utf-8"))
    items = []
    for path in sorted((root / "lines").rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        frontmatter = dict(re.findall(r"^(\w+): (.+)$", text.split("---")[1], re.M))
        guide_title = re.search(r"^# (.+)$", text, re.M).group(1)
        matches = re.finditer(
            r'%% line-start id="([^"]+)" %%\n(.*?)%% line-end %%\n(.*?)(?=%% line-start|\Z)',
            text,
            re.S,
        )
        for match in matches:
            line_id, body, detail = match.groups()
            row = ledger.get(line_id, {})
            if row.get("狀態", "有效") != "有效":
                continue
            slots = dict(re.findall(r"^- (做法|對手|退路|解鎖)：(.+)$", body, re.M))
            story = re.search(r"^經過：(.+)$", body, re.M)
            details = dict(re.findall(r"^- ([^：\n]+)：(.+)$", detail, re.M))
            unlock_raw = slots.get("解鎖", "")
            items.append({
                "id": line_id,
                "guide_id": frontmatter.get("guide", ""),
                "guide_title": guide_title,
                "category": frontmatter.get("category", ""),
                "upstream": frontmatter.get("upstream", ""),
                "file": str(path.relative_to(root)),
                "feature": row.get("功能", ""),
                "group": row.get("對手組", details.get("對手組", "")),
                "kind": row.get("類型", details.get("類型", "")),
                "fallback_cat": row.get("退路", ""),
                "result": row.get("戰報", ""),
                "level": row.get("支援狀態", ""),
                "evidence": row.get("證據", "宣稱"),
                "release": row.get("版本", ""),
                "title": re.search(r"^## (.+)$", body, re.M).group(1),
                "action": slots.get("做法", ""),
                "opponent": slots.get("對手", ""),
                "fallback": slots.get("退路", ""),
                "unlock": "" if unlock_raw.startswith("（缺）") else unlock_raw,
                "idea": details.get("發想（非指南原文）", row.get("發想", "")),
                "story": story.group(1) if story else "",
                "support": details.get("支援狀態", ""),
            })
    return items, en


def view(item, lang, en):
    if lang == "zh":
        return {k: item[k] for k in (
            "id", "guide_id", "guide_title", "category", "upstream", "file", "feature",
            "group", "kind", "fallback_cat", "result", "level", "evidence", "release", "title",
            "action", "opponent", "fallback", "unlock", "idea", "story", "support",
        )}
    translated = en["lines"].get(item["id"], {})
    result = en["result"].get(item["result"], item["result"])
    fb_cat = en["fallback"].get(item["fallback_cat"], item["fallback_cat"])
    return {
        **{k: item[k] for k in ("id", "guide_id", "category", "upstream", "file", "feature", "release")},
        "guide_title": en["guides"].get(item["guide_id"], item["guide_title"]),
        "group": en["groups"].get(item["group"], item["group"]),
        "kind": en["kind"].get(item["kind"], item["kind"]),
        "fallback_cat": fb_cat,
        "result": result,
        "level": en["level"].get(item["level"], item["level"]),
        "evidence": "Tested" if item["evidence"] == "實測" else "Claimed",
        "title": translated.get("title", item["title"]),
        "action": translated.get("action", item["action"]),
        "opponent": translated.get("opponent", item["opponent"]),
        "fallback": f'{fb_cat} — {translated["fallback"]}' if translated else item["fallback"],
        "unlock": translated.get("unlock", item["unlock"]),
        "idea": translated.get("idea", item["idea"]),
        "story": translated.get("story", item["story"]),
        "support": translated.get("support", item["support"]),
    }


def terms(query):
    stop = {"可以", "現在", "以前", "什麼", "時候", "一個", "想要", "因為", "所以", "如果", "這個", "那個"}
    english_stop = {"a", "an", "and", "are", "be", "can", "could", "for", "how", "i", "is", "of", "or", "the", "to", "want", "with"}
    found = []
    for token in re.findall(r"[a-z0-9]+(?:[_.+:-][a-z0-9]+)*|[\u3400-\u9fff]+", query.casefold()):
        if re.search(r"[\u3400-\u9fff]", token):
            if token not in stop:
                found.append(token)
            found.extend(token[i:i + 2] for i in range(len(token) - 1) if token[i:i + 2] not in stop)
        elif token not in english_stop:
            found.append(token)
    return list(dict.fromkeys(found))


def search_fields(item, lang, en):
    primary = view(item, lang, en)
    alternate = view(item, "en" if lang == "zh" else "zh", en)
    weighted = []
    for data in (primary, alternate):
        for keys, weight in (
            (("id", "guide_id", "feature"), 6),
            (("title", "group", "guide_title"), 5),
            (("opponent", "action"), 4),
            (("unlock", "idea", "story"), 3),
            (("fallback", "support"), 2),
        ):
            weighted.append((weight, " ".join(data[key] for key in keys).casefold()))
    return weighted


def rank(items, query, lang, en):
    query_terms = terms(query)
    if not query_terms:
        return []
    phrase = query.casefold().strip()
    ranked = []
    for item in items:
        fields = search_fields(item, lang, en)
        matched = 0
        score = 0
        for term in query_terms:
            weights = [weight for weight, text in fields if term in text]
            if weights:
                matched += 1
                score += max(weights) + min(len(weights) - 1, 2)
        if not matched:
            continue
        score += 8 * matched / len(query_terms)
        if phrase and any(phrase in text for _, text in fields):
            score += 8
        ranked.append((score, item))
    ranked.sort(key=lambda pair: (-pair[0], pair[1]["id"]))
    return ranked


def main():
    parser = argparse.ArgumentParser(description="依舊阻礙、對手或功能檢索 Web 問題線")
    parser.add_argument("query", nargs="?", help="兩到六個核心關鍵字，以空白分隔")
    parser.add_argument("--id", help="直接讀取一個 line ID")
    parser.add_argument("--kind", choices=("新能力", "糾錯"), help="篩選問題線類型")
    parser.add_argument("--result", choices=("勝", "部分改善", "僵持"), help="篩選戰報")
    parser.add_argument("--group", help="以中英文對手組名稱的一部分篩選")
    parser.add_argument("--lang", choices=("zh", "en"), default="zh", help="輸出語言，預設 zh")
    parser.add_argument("--limit", type=int, default=5, help="最多回傳幾條，預設 5")
    parser.add_argument("--json", action="store_true", help="輸出 JSON")
    args = parser.parse_args()
    if not (args.query or args.id or args.group):
        parser.error("請提供查詢關鍵字、--id 或 --group")
    if args.limit < 1:
        parser.error("--limit 必須大於 0")

    root = find_root()
    items, en = load_data(root)
    if args.id:
        selected = [(0, item) for item in items if item["id"] == args.id]
    else:
        selected = [(0, item) for item in items]
    if args.kind:
        selected = [pair for pair in selected if pair[1]["kind"] == args.kind]
    if args.result:
        selected = [pair for pair in selected if pair[1]["result"] == args.result]
    if args.group:
        group = args.group.casefold()
        selected = [pair for pair in selected if group in pair[1]["group"].casefold() or group in en["groups"].get(pair[1]["group"], "").casefold()]
    if args.query and not args.id:
        selected = rank([item for _, item in selected], args.query, args.lang, en)
    selected = selected[:args.limit]

    results = [view(item, args.lang, en) for _, item in selected]
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return
    if not results:
        print("沒有符合的問題線。請換用症狀、對手或功能關鍵字；不要捏造結果。" if args.lang == "zh" else "No matching problem lines. Try symptom, opponent, or feature keywords; do not invent a match.")
        return
    for index, item in enumerate(results, 1):
        if args.lang == "en":
            print(f'## {index}. {item["title"]}\n')
            print(f'- ID: `{item["id"]}`')
            print(f'- Type / outcome / support: {item["kind"]} / {item["result"]} / {item["level"]}')
            print(f'- Opponent group: {item["group"]}')
            print(f'- Feature: {item["feature"]}')
            print(f'- Action: {item["action"]}')
            print(f'- Opponent: {item["opponent"]}')
            print(f'- Fallback: {item["fallback"]}')
            if item["unlock"]:
                print(f'- Unlock: {item["unlock"]}')
            if item["idea"]:
                print(f'- Idea (brainstorm, not guide text): {item["idea"]}')
            print(f'- Support details: {item["support"]}')
            print(f'- Evidence: {item["evidence"]}')
            print(f'- Upstream: {item["upstream"]}')
            print(f'- Line file: `{item["file"]}`\n')
        else:
            print(f'## {index}. {item["title"]}\n')
            print(f'- ID：`{item["id"]}`')
            print(f'- 類型／戰報／支援：{item["kind"]}／{item["result"]}／{item["level"]}')
            print(f'- 對手組：{item["group"]}')
            print(f'- 功能：{item["feature"]}')
            print(f'- 做法：{item["action"]}')
            print(f'- 對手：{item["opponent"]}')
            print(f'- 退路：{item["fallback"]}')
            if item["unlock"]:
                print(f'- 解鎖：{item["unlock"]}')
            if item["idea"]:
                print(f'- 發想（非指南原文）：{item["idea"]}')
            print(f'- 支援狀態：{item["support"]}')
            print(f'- 證據：{item["evidence"]}')
            print(f'- 上游指南：{item["upstream"]}')
            print(f'- 線檔：`{item["file"]}`\n')


if __name__ == "__main__":
    main()
