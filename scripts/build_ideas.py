#!/usr/bin/env python3
"""靈感頁：只列新能力的線，依「現在能不能用」分區、依主題篩選。

產生 docs/ideas/index.html（中文）與 docs/en/ideas/index.html（英文）。
每張卡片：解鎖（能指回原文）＋發想（延伸點子）＋不支援時會怎樣。資料取自線檔、ledger 與 i18n。
"""
import csv, html, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
LINE_RE = re.compile(r'%% line-start id="([^"]+)" %%\n(.*?)%% line-end %%', re.S)
EN = json.load(open(ROOT / "i18n/en.json", encoding="utf-8"))

THEMES = {  # 分類目錄 → 主題
    "ui-components": ("元件", "Components"), "ui-behaviors": ("互動與動畫", "Interaction & motion"),
    "ui-atoms": ("介面細節", "UI details"), "css": ("CSS 版面與樣式", "CSS layout & styling"),
    "visual-design": ("視覺效果", "Visual design"), "forms": ("表單", "Forms"), "html": ("HTML 與元件", "HTML & components"),
    "js": ("JavaScript", "JavaScript"), "performance": ("效能", "Performance"), "security": ("安全與登入", "Security & sign-in"),
    "privacy": ("隱私", "Privacy"), "built-in-ai": ("內建 AI", "Built-in AI"), "webmcp": ("AI 代理", "AI agents"),
    "pwa": ("可安裝的 web app", "Installable apps"), "wasm": ("WebAssembly", "WebAssembly"),
    "accessibility": ("無障礙", "Accessibility"), "user-experience": ("使用體驗", "User experience"),
}
TIERS = [  # (key, 中文, 英文, 說明中, 說明英)
    ("ready", "今天就能用", "Use it today", "已進入 Baseline 或不涉及瀏覽器支援；不支援時主要功能照常。",
     "Newly in Baseline, or not tied to browser support; without it, the core still works."),
    ("enhance", "漸進增強", "Progressive enhancement", "只有部分瀏覽器支援，但不支援時保住主要行為，可以放心當加分項。",
     "Only some browsers support it, but the core behavior survives without it, so it is safe as an enhancement."),
    ("demo", "只在支援的瀏覽器有效", "Works only where supported", "不支援時會失去主要好處；適合先做 demo、內部工具，或給特定瀏覽器的體驗。",
     "Without support you lose the main benefit; good for demos, internal tools, or browser-specific experiences."),
    ("watch", "先追蹤", "Watch", "還沒有瀏覽器支援，先記下來。", "No browser supports it yet; keep an eye on it."),
]

# 有可以直接試的 demo 的線（docs/demos/<路徑>/）
DEMOS = {"mwg:dynamic-sibling-animations": "stagger", "mwg:anchor-positioning-tab-underline": "tab-underline",
         "mwg:scroll-entry-exit-effects": "scroll-entry-exit", "mwg:accordion:3": "accordion", "mwg:contrast-color": "contrast-color",
         "mwg:declarative-dialog-popover-control": "invoker-commands", "mwg:custom-button-actions": "invoker-commands",
         "mwg:hovercard:8": "hovercard", "mwg:dark-mode:3": "light-dark"}

def tier(level, fb):
    if level == "無瀏覽器支援": return "watch"
    if level == "不適用" or (level == "Newly" and fb == "保住主要行為"): return "ready"
    if fb == "保住主要行為": return "enhance"
    return "demo"

ledger = {r["line_id"]: r for r in csv.DictReader(open(ROOT / "ledger.csv", encoding="utf-8", newline=""))}
items = []
for p in sorted((ROOT / "lines").glob("*/*.md")):
    for lid, body in LINE_RE.findall(p.read_text(encoding="utf-8")):
        r = ledger.get(lid)
        if not r or r["狀態"] != "有效" or r["類型"] != "新能力":
            continue
        s = dict(re.findall(r"^- ([^：\n]+)：(.+)$", body, re.M))
        fb_cat, _, fb_text = s.get("退路", "").partition("——")
        e = EN["lines"].get(lid, {})
        items.append(dict(id=lid, anchor=lid.replace(":", "--"), cat=p.parent.name, tier=tier(r["支援狀態"], r["退路"]),
                          level=r["支援狀態"], fb=r["退路"], guide=r["guide_id"],
                          zh=dict(title=re.search(r"^## (.+)$", body, re.M).group(1).strip(), unlock=r["解鎖"], idea=r["發想"], fbt=fb_text.strip()),
                          en=dict(title=e.get("title", ""), unlock=e.get("unlock", ""), idea=e.get("idea", ""), fbt=e.get("fallback", ""))))

def inline(s):
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", html.escape(s or "", quote=False))

UI = {
    "zh": dict(lang="zh-Hant", title="靈感：新能力", h1="新能力・靈感",
               lead=lambda n: f"從 {n} 條「新能力」問題線整理：平台新增了什麼，讓以前做不到或很難的事變得可行。依<b>現在能不能用</b>分區；每張卡片的「解鎖」能指回指南原文，「發想」是延伸的點子，不是指南原文。",
               nav='<a href="../">← 所有問題線</a> · <a href="../demos/">Demo</a> · <a href="../en/ideas/">English</a> · <a href="../weekly/">週記</a> · <a href="../en/graph/">對手組關係圖（英文）</a>',
               ph="搜尋：功能、想做的東西…", all="全部主題", unlock="解鎖", idea="發想", fb="不支援時", guide="指南", line="看這條線",
               up="https://github.com/GoogleChrome/modern-web-guidance", empty="沒有符合的卡片", unit="張", main="../#", demos="../demos/", trydemo="▶ 試試 demo"),
    "en": dict(lang="en", title="Ideas: New capabilities", h1="New capabilities · Ideas",
               lead=lambda n: f"{n} problem lines marked <b>new capability</b>: what the platform added that makes something newly possible or much cheaper. Grouped by <b>whether you can use it now</b>. On each card, <b>Unlock</b> points back to the guide; <b>Idea</b> is brainstorming, not guide text.",
               nav='<a href="../">← All problem lines</a> · <a href="../../demos/">Demos (Chinese)</a> · <a href="../../ideas/">繁體中文</a> · <a href="../graph/">Opponent graph</a> · <a href="../../weekly/">Weekly notes (Chinese)</a>',
               ph="Search: feature, something you want to build…", all="All themes", unlock="Unlock", idea="Idea", fb="Without support", guide="Guide", line="View line",
               up="https://github.com/GoogleChrome/modern-web-guidance", empty="No matching cards", unit="cards", main="../#", demos="../../demos/", trydemo="▶ Try the demo (Chinese)"),
}

CSS = """
:root{--bg:#fbfaf7;--fg:#1f1d1a;--mute:#6b665e;--line:#e4e0d8;--card:#fff;--accent:#2f5d50;--soft:#f3efe2;
--t-ready:#2f6f4f;--t-enhance:#3d6a8a;--t-demo:#8a6a12;--t-watch:#6b665e;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#161513;--fg:#ece8e1;--mute:#a19b91;--line:#34312c;--card:#1e1c19;--accent:#8cc3b0;--soft:#2a2720;
--t-ready:#7fc79f;--t-enhance:#8ab8d8;--t-demo:#e0bd5a;--t-watch:#a19b91;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#161513;--fg:#ece8e1;--mute:#a19b91;--line:#34312c;--card:#1e1c19;--accent:#8cc3b0;--soft:#2a2720;
--t-ready:#7fc79f;--t-enhance:#8ab8d8;--t-demo:#e0bd5a;--t-watch:#a19b91;color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.65 system-ui,"Noto Sans TC","PingFang TC",sans-serif}
main{max-width:64rem;margin:0 auto;padding:2rem 16px 4rem}
a{color:var(--accent)} :focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.nav{font-size:.85rem;color:var(--mute);margin:0 0 .5rem}
h1{font-size:1.6rem;margin:0 0 .4rem;text-wrap:balance}
.lead{color:var(--mute);margin:0 0 1rem;max-width:48rem;text-wrap:pretty}
.toc{display:flex;flex-wrap:wrap;gap:.5rem;margin:0 0 1rem}
.toc a{text-decoration:none;font-size:.9rem;border:1px solid var(--line);border-radius:10px;padding:.35rem .75rem;background:var(--card);color:var(--fg)}
.toc a b{font-variant-numeric:tabular-nums;margin-left:.35rem}
.bar{position:sticky;top:0;z-index:2;background:var(--bg);padding:.6rem 0;border-bottom:1px solid var(--line);margin-bottom:.5rem}
input[type=search]{width:100%;font:inherit;padding:.55rem .8rem;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--fg)}
.chips{display:flex;flex-wrap:wrap;gap:.35rem;margin-top:.55rem}
.chip{font:inherit;font-size:.82rem;padding:.2rem .65rem;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--fg);cursor:pointer}
.chip[aria-pressed=true]{background:var(--accent);border-color:var(--accent);color:var(--bg)}
.count{color:var(--mute);font-size:.85rem;margin:.4rem 0 0}
section{margin-top:1.75rem}
section > h2{font-size:1.2rem;margin:0 0 .15rem;display:flex;align-items:center;gap:.5rem}
section > h2::before{content:"";width:.7rem;height:.7rem;border-radius:50%;background:var(--tc)}
section > p{color:var(--mute);margin:0 0 .75rem;font-size:.92rem}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(19rem,1fr));gap:.75rem}
.card{background:var(--card);border:1px solid var(--line);border-top:3px solid var(--tc);border-radius:10px;padding:.85rem 1rem;display:flex;flex-direction:column;gap:.45rem}
.card h3{font-size:1rem;line-height:1.4;margin:0;text-wrap:balance}
.card .u{margin:0}
.card .u b,.card .i b,.card .f b{font-size:.75rem;letter-spacing:.03em;color:var(--mute);display:block}
.card .i{margin:0;background:var(--soft);border-radius:8px;padding:.45rem .6rem;font-size:.92rem}
.card .f{margin:0;font-size:.85rem;color:var(--mute)}
.card .m a.demo{font-weight:600}
.card .m{margin-top:auto;display:flex;flex-wrap:wrap;gap:.3rem .6rem;font-size:.78rem;color:var(--mute);align-items:center}
.tag{border:1px solid var(--line);border-radius:999px;padding:0 .45rem}
code{font-family:ui-monospace,Menlo,monospace;font-size:.86em;background:color-mix(in srgb,var(--line) 60%,transparent);padding:.05em .3em;border-radius:3px;overflow-wrap:anywhere}
.empty{color:var(--mute);display:none}
footer{color:var(--mute);font-size:.82rem;margin-top:3rem}
.t-ready{--tc:var(--t-ready)} .t-enhance{--tc:var(--t-enhance)} .t-demo{--tc:var(--t-demo)} .t-watch{--tc:var(--t-watch)}
"""

def page(lang):
    u = UI[lang]; zh = lang == "zh"
    cats = sorted({i["cat"] for i in items}, key=lambda c: list(THEMES).index(c) if c in THEMES else 99)
    chips = f'<button class="chip" type="button" data-cat="" aria-pressed="true">{u["all"]}</button>' + "".join(
        f'<button class="chip" type="button" data-cat="{c}" aria-pressed="false">{THEMES.get(c, (c, c))[0 if zh else 1]}</button>' for c in cats)
    toc, secs = [], []
    for key, tz, te, dz, de in TIERS:
        its = [i for i in items if i["tier"] == key]
        if not its: continue
        toc.append(f'<a href="#{key}" class="t-{key}">{tz if zh else te}<b>{len(its)}</b></a>')
        cards = []
        for i in sorted(its, key=lambda i: (list(THEMES).index(i["cat"]) if i["cat"] in THEMES else 99, i["id"])):
            t = i[lang] if (lang == "zh" or i["en"]["title"]) else i["zh"]
            unlock = f'<p class="u"><b>{u["unlock"]}</b>{inline(t["unlock"])}</p>' if t["unlock"] else ""
            idea = f'<p class="i"><b>{u["idea"]}</b>{inline(t["idea"])}</p>' if t["idea"] else ""
            fb = f'<p class="f"><b>{u["fb"]}</b>{inline(t["fbt"])}</p>' if t["fbt"] and i["fb"] != "不需要" else ""
            level = i["level"] if zh else EN["level"].get(i["level"], i["level"])
            gname = i["guide"] if zh else EN["guides"].get(i["guide"], i["guide"])
            text = html.escape(" ".join([t["title"], t["unlock"], t["idea"], i["guide"]]).lower(), quote=True)
            cards.append(f'''<article class="card t-{key}" data-cat="{i["cat"]}" data-text="{text}">
<h3>{inline(t["title"])}</h3>{unlock}{idea}{fb}
<div class="m"><span class="tag">{THEMES.get(i["cat"], (i["cat"],) * 2)[0 if zh else 1]}</span><span>{html.escape(level)}</span><span>{html.escape(gname)}</span><a href="{u["main"]}{i["anchor"]}">{u["line"]} →</a>{f'<a class="demo" href="{u["demos"]}{DEMOS[i["id"]]}/">{u["trydemo"]}</a>' if i["id"] in DEMOS else ""}</div>
</article>''')
        secs.append(f'<section id="{key}" class="t-{key}"><h2>{tz if zh else te}</h2><p>{dz if zh else de}</p><div class="grid">{"".join(cards)}</div></section>')
    return f'''<!doctype html>
<html lang="{u["lang"]}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{u["title"]}</title>
<meta name="description" content="{html.escape(re.sub('<[^>]+>', '', u["lead"](len(items))), quote=True)}">
<style>{CSS}</style></head><body><main>
<p class="nav">{u["nav"]}</p>
<h1>{u["h1"]}</h1>
<p class="lead">{u["lead"](len(items))}</p>
<nav class="toc">{"".join(toc)}</nav>
<div class="bar"><input type="search" id="q" placeholder="{u["ph"]}" aria-label="{u["ph"]}"><div class="chips" role="group">{chips}</div><p class="count" id="count" aria-live="polite"></p></div>
{"".join(secs)}
<p class="empty" id="empty">{u["empty"]}</p>
<footer>{'上游指南為 CC-BY 4.0（GoogleChrome/modern-web-guidance）。「發想」不是指南原文。這頁由 <code>scripts/build_ideas.py</code> 產生。' if zh else 'Upstream guides are CC-BY 4.0 (GoogleChrome/modern-web-guidance). "Idea" is brainstorming, not guide text. Generated by <code>scripts/build_ideas.py</code>.'}</footer>
</main>
<script>
const cards = [...document.querySelectorAll(".card")], q = document.getElementById("q"), chips = [...document.querySelectorAll(".chip")];
let cat = "";
function apply() {{
  const s = q.value.trim().toLowerCase(); let n = 0;
  for (const c of cards) {{ const ok = (!cat || c.dataset.cat === cat) && (!s || c.dataset.text.includes(s)); c.hidden = !ok; if (ok) n++; }}
  for (const sec of document.querySelectorAll("section")) sec.hidden = ![...sec.querySelectorAll(".card")].some(c => !c.hidden);
  document.getElementById("count").textContent = `${{n}} {u["unit"]}`;
  document.getElementById("empty").style.display = n ? "none" : "block";
}}
chips.forEach(b => b.onclick = () => {{ cat = b.dataset.cat; chips.forEach(x => x.setAttribute("aria-pressed", String(x === b))); apply(); }});
q.oninput = apply; apply();
</script>
</body></html>
'''

for lang, out in (("zh", ROOT / "docs/ideas/index.html"), ("en", ROOT / "docs/en/ideas/index.html")):
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(lang), encoding="utf-8")
counts = {k: sum(i["tier"] == k for i in items) for k, *_ in TIERS}
print(f"docs/ideas/ + docs/en/ideas/: {len(items)} 張新能力卡片 {counts}")
