#!/usr/bin/env python3
"""將問題線由舊槽純機械轉換為槽 v2；預設處理全部線檔。"""
import argparse
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
LINE_RE = re.compile(
    r'%% line-start id="([^"]+)" %%\n(.*?)%% line-end %%\n(.*?)(?=%% line-start|\Z)',
    re.S,
)


def replace_once(text, pattern, replacement, label, line_id):
    text, count = re.subn(pattern, replacement, text, count=1, flags=re.M)
    if count != 1:
        raise ValueError(f"{line_id}: 找不到唯一的{label}")
    return text


def migrate_line(match):
    line_id, body, detail = match.groups()
    if all(f"- {slot}：" in body for slot in ("做法", "對手", "退路", "解鎖")):
        return match.group(0), False

    body = replace_once(body, r"^- 誰在做：.*\n", "", "「誰在做」", line_id)
    body = replace_once(body, r"^- 動作＋對象：", "- 做法：", "「動作＋對象」", line_id)
    body = replace_once(body, r"^- 被什麼擋：", "- 對手：", "「被什麼擋」", line_id)
    body = replace_once(
        body,
        r"^- 戰報：.*\n",
        "- 退路：TODO——TODO\n- 解鎖：TODO\n",
        "線內「戰報」",
        line_id,
    )

    detail = replace_once(
        detail,
        r"^- 解鎖（發想，非指南原文）：",
        "- 發想（非指南原文）：",
        "舊「解鎖」細節（若原本存在）",
        line_id,
    ) if re.search(r"^- 解鎖（發想，非指南原文）：", detail, re.M) else detail
    detail = replace_once(
        detail,
        r"(^- 支援狀態：.*\n)",
        r"\1- 戰報：TODO\n",
        "「支援狀態」",
        line_id,
    )
    opponent = re.search(r"^- 對手：(.*)$", body, re.M).group(1)
    opponent_state = "缺" if opponent.startswith("（缺）") else "有"
    detail = replace_once(
        detail,
        r"^- 槽判定：.*$",
        f"- 槽判定：對手 {opponent_state}／解鎖 TODO",
        "「槽判定」",
        line_id,
    )
    detail = replace_once(
        detail,
        r"^- 變更紀錄：(.*)$",
        r"- 變更紀錄：\1；2026-11-18 改為槽 v2",
        "「變更紀錄」",
        line_id,
    )
    return f'%% line-start id="{line_id}" %%\n{body}%% line-end %%\n{detail}', True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=pathlib.Path)
    args = parser.parse_args()
    paths = args.paths or sorted((ROOT / "lines").glob("*/*.md"))

    results = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        migrated_lines = []
        for match in LINE_RE.finditer(text):
            replacement, changed = migrate_line(match)
            migrated_lines.append((match.span(), replacement, changed))
        results.append((path, text, migrated_lines))

    files_changed = 0
    lines_changed = 0
    for path, text, migrated_lines in results:
        if not any(changed for _, _, changed in migrated_lines):
            continue
        pieces = []
        position = 0
        for (start, end), replacement, changed in migrated_lines:
            pieces.append(text[position:start])
            pieces.append(replacement)
            position = end
            lines_changed += changed
        pieces.append(text[position:])
        path.write_text("".join(pieces), encoding="utf-8")
        files_changed += 1

    print(f"轉換 {files_changed} 個檔案、{lines_changed} 條線")


if __name__ == "__main__":
    main()
