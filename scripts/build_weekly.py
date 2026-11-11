#!/usr/bin/env python3
"""把 weekly/*.md 轉成 docs/weekly/<日期>.html，並產生 docs/weekly/index.html 目錄。

只支援週記用到的 Markdown：標題、段落、清單（含縮排續行）、粗體、行內程式碼、連結。
週記裡的 `mwg:<line_id>` 會連到主頁上對應的線。
"""
import html, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "weekly"

def anchor(lid):
    return lid.replace(":", "--")

def inline(s):
    s = html.escape(s, quote=False)
    def code(m):
        c = m.group(1)
        if re.fullmatch(r"mwg:[\w-]+(?::\d+)?", c):
            return f'<a class="lid" href="../#{anchor(c)}"><code>{c}</code></a>'
        return f"<code>{c}</code>"
    parts = re.split(r"(`[^`]+`)", s)
    out = []
    for p in parts:
        if p.startswith("`") and p.endswith("`") and len(p) > 1:
            out.append(code(re.match(r"`(.+)`", p)))
        else:
            p = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", p)
            p = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', p)
            p = re.sub(r'(?<!href=")(https?://[^\s<）)]+)', r'<a href="\1">\1</a>', p)
            out.append(p)
    return "".join(out)

def md(text):
    lines = text.split("\n")
    out, i = [], 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1; continue
        m = re.match(r"^(#{1,3}) (.+)$", ln)
        if m:
            n = len(m.group(1))
            out.append(f"<h{n}>{inline(m.group(2))}</h{n}>"); i += 1; continue
        m = re.match(r"^(-|\d+\.) ", ln)
        if m:
            tag = "ul" if m.group(1) == "-" else "ol"
            items = []
            while i < len(lines) and (re.match(r"^(-|\d+\.) ", lines[i]) or (lines[i].startswith("   ") and items) or (not lines[i].strip() and i + 1 < len(lines) and re.match(r"^\d+\. ", lines[i + 1]) and tag == "ol")):
                l = lines[i]
                if re.match(r"^(-|\d+\.) ", l):
                    items.append([re.sub(r"^(-|\d+\.) ", "", l)])
                elif l.strip():
                    items[-1].append(l.strip())
                i += 1
            lis = "".join("<li>" + "<br>".join(inline(x) for x in it) + "</li>" for it in items)
            out.append(f"<{tag}>{lis}</{tag}>"); continue
        para = []
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,3} |-|\d+\. )", lines[i]):
            para.append(lines[i].strip()); i += 1
        out.append("<p>" + inline(" ".join(para)) + "</p>")
    return "\n".join(out)

CSS = """
:root{--bg:#fbfaf7;--fg:#1f1d1a;--mute:#6b665e;--line:#e4e0d8;--card:#fff;--accent:#2f5d50;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#161513;--fg:#ece8e1;--mute:#a19b91;--line:#34312c;--card:#1e1c19;--accent:#8cc3b0;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#161513;--fg:#ece8e1;--mute:#a19b91;--line:#34312c;--card:#1e1c19;--accent:#8cc3b0;color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.75 system-ui,"Noto Sans TC","PingFang TC",sans-serif}
main{max-width:46rem;margin:0 auto;padding:2rem 16px 4rem}
nav{font-size:.9rem;color:var(--mute);margin-bottom:1.5rem;display:flex;flex-wrap:wrap;gap:.25rem 1rem}
a{color:var(--accent)} a:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
h1{font-size:1.6rem;line-height:1.35;text-wrap:balance;margin:0 0 1rem}
h2{font-size:1.2rem;margin:2.25rem 0 .75rem;padding-top:1rem;border-top:1px solid var(--line)}
h3{font-size:1rem;margin:1.5rem 0 .5rem}
p,li{text-wrap:pretty;overflow-wrap:anywhere}
li{margin:.35rem 0} ol>li{margin:1rem 0}
ol>li>strong:first-child{font-size:1.05rem}
code{font-family:ui-monospace,Menlo,monospace;font-size:.88em;background:color-mix(in srgb,var(--line) 60%,transparent);padding:.05em .3em;border-radius:3px}
a.lid{text-decoration:none} a.lid:hover code{outline:1px solid var(--accent)}
.list{list-style:none;padding:0}
.list li{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:.85rem 1rem;margin:.6rem 0}
.list a{font-weight:600;text-decoration:none} .list a:hover{text-decoration:underline}
.list .sub{display:block;color:var(--mute);font-size:.88rem;margin-top:.2rem}
.pager{display:flex;justify-content:space-between;gap:1rem;margin-top:3rem;padding-top:1rem;border-top:1px solid var(--line);font-size:.9rem}
footer{color:var(--mute);font-size:.85rem;margin-top:3rem}
"""

def page(title, body, nav):
    return f"""<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="modern-web-guidance 問題線的每週週記：這週的對手、僵持中的線、本週靈感">
<style>{CSS}</style></head><body><main>
<nav>{nav}</nav>
{body}
<footer>上游指南為 CC-BY 4.0（GoogleChrome/modern-web-guidance）。「本週靈感」是發想，不是指南原文。這頁由 <code>scripts/build_weekly.py</code> 從 <code>weekly/</code> 產生。</footer>
</main></body></html>
"""

NAV = '<a href="../">← 所有問題線</a><a href="./">週記目錄</a><a href="https://github.com/ianTPE/web-tension-lines/tree/main/weekly">原始檔</a>'

notes = sorted((ROOT / "weekly").glob("*.md"), reverse=True)
OUT.mkdir(parents=True, exist_ok=True)
index = []
for k, p in enumerate(notes):
    text = p.read_text(encoding="utf-8")
    title = re.search(r"^# (.+)$", text, re.M).group(1)
    stat = re.search(r"^- 本週拆出：(.+)$", text, re.M)
    idea = len(re.findall(r"^\d+\. \*\*", text.split("## 本週靈感")[1].split("\n## ")[0], re.M)) if "## 本週靈感" in text else 0
    newer = notes[k - 1].stem if k > 0 else None
    older = notes[k + 1].stem if k + 1 < len(notes) else None
    pager = '<div class="pager"><span>' + (f'<a href="{older}.html">← {older}</a>' if older else "") + "</span><span>" + (f'<a href="{newer}.html">{newer} →</a>' if newer else "") + "</span></div>"
    (OUT / f"{p.stem}.html").write_text(page(title, md(text) + pager, NAV), encoding="utf-8")
    sub = "；".join(x for x in [stat.group(1) if stat else "", f"{idea} 個應用點子" if idea else ""] if x)
    index.append(f'<li><a href="{p.stem}.html">{html.escape(title)}</a><span class="sub">{html.escape(sub)}</span></li>')

body = f'<h1>週記</h1>\n<p>每週拆完 modern-web-guidance 的新指南後寫一篇：這週出現的對手、還在等瀏覽器支援的線，以及用新能力組出的應用點子。共 {len(notes)} 篇，新的在前。</p>\n<ul class="list">{"".join(index)}</ul>'
(OUT / "index.html").write_text(page("週記・Web 張力線", body, '<a href="../">← 所有問題線</a><a href="https://github.com/ianTPE/web-tension-lines/tree/main/weekly">原始檔</a>'), encoding="utf-8")
print(f"docs/weekly/: {len(notes)} notes")
