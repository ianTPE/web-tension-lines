#!/usr/bin/env python3
"""把 lines/ 與 ledger.csv 組成一頁可搜尋、可展開的 docs/index.html。"""
import csv, html, json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = "https://github.com/ianTPE/web-tension-lines/blob/main"

def inline(s):
    s = html.escape(s, quote=False)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", s)

ledger = {r["line_id"]: r for r in csv.DictReader(open(ROOT / "ledger.csv", encoding="utf-8"))}
state = json.load(open(ROOT / "state.json"))

items = []
for p in sorted((ROOT / "lines").rglob("*.md")):
    text = p.read_text(encoding="utf-8")
    fm = dict(re.findall(r"^(\w+): (.+)$", text.split("---")[1], re.M))
    gtitle = re.search(r"^# (.+)$", text, re.M).group(1)
    for m in re.finditer(r'%% line-start id="([^"]+)" %%\n(.*?)%% line-end %%\n(.*?)(?=%% line-start|\Z)', text, re.S):
        lid, body, detail = m.groups()
        title = re.search(r"^## (.+)$", body, re.M).group(1)
        slots = dict(re.findall(r"^- (誰在做|動作＋對象|被什麼擋|戰報)：(.+)$", body, re.M))
        story = re.search(r"^經過：(.+)$", body, re.M)
        det = dict(re.findall(r"^- ([^：\n]+)：(.+)$", detail, re.M))
        led = ledger.get(lid, {})
        items.append(dict(
            id=lid, title=title, guide=fm.get("guide", ""), gtitle=gtitle,
            category=fm.get("category", ""), upstream=fm.get("upstream", ""),
            file=str(p.relative_to(ROOT)), slots=slots, story=story.group(1) if story else "",
            unlock=det.get("解鎖（發想，非指南原文）", ""), support=det.get("支援狀態", ""),
            group=led.get("對手組", det.get("對手組", "")), kind=led.get("類型", det.get("類型", "")),
            result=led.get("戰報", ""), level=led.get("支援狀態", ""), release=led.get("版本", ""),
        ))

def card(it):
    s = it["slots"]
    rows = "".join(f"<dt>{k}</dt><dd>{inline(s[k])}</dd>" for k in ("誰在做", "動作＋對象", "被什麼擋", "戰報") if k in s)
    unlock = f'<div class="unlock"><span class="tag">解鎖・發想</span>{inline(it["unlock"])}</div>' if it["unlock"] else ""
    return f'''<details class="line" data-kind="{it["kind"]}" data-result="{it["result"]}" data-group="{html.escape(it["group"])}" data-guide="{it["guide"]}">
<summary><span class="t">{inline(it["title"])}</span>
<span class="badges"><span class="b k-{it["kind"]}">{it["kind"]}</span><span class="b r-{it["result"]}">{it["result"]}</span><span class="b lv">{it["level"]}</span></span>
<span class="meta">{html.escape(it["gtitle"])} · {html.escape(it["group"])}</span></summary>
<div class="body">{unlock}<dl>{rows}</dl><p class="story">{inline(it["story"])}</p>
<p class="support"><b>支援</b> {inline(it["support"])}</p>
<p class="links"><code>{it["id"]}</code> · <a href="{it["upstream"]}">上游指南</a> · <a href="{REPO}/{it["file"]}">線檔</a> · {it["release"]}</p></div></details>'''

def chips(name, values):
    b = f'<button type="button" class="chip" aria-pressed="true" data-f="{name}" data-v="">全部</button>'
    return b + "".join(f'<button type="button" class="chip" aria-pressed="false" data-f="{name}" data-v="{v}">{v}</button>' for v in values)

kinds = ["新能力", "糾錯"]
results = ["勝", "部分改善", "僵持", "缺"]
n_new = sum(1 for i in items if i["kind"] == "新能力")
cards = "\n".join(card(i) for i in items)

page = f'''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Web 張力線</title>
<meta name="description" content="把 modern-web-guidance 的新指南拆成問題線：哪個新做法擋掉了哪個老問題">
<style>
:root{{--bg:#fbfaf7;--fg:#1f1d1a;--mute:#6b665e;--line:#e4e0d8;--card:#fff;--accent:#2f5d50;--unlock:#f3efe2;
--win:#2f6f4f;--part:#8a6a12;--stuck:#9a3b2f;--miss:#6b665e;--new:#2f5d50;--fix:#6b665e;color-scheme:light}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#161513;--fg:#ece8e1;--mute:#a19b91;--line:#34312c;--card:#1e1c19;--accent:#8cc3b0;--unlock:#2a2720;
--win:#7fc79f;--part:#e0bd5a;--stuck:#ee8f7f;--miss:#a19b91;--new:#8cc3b0;--fix:#a19b91;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#161513;--fg:#ece8e1;--mute:#a19b91;--line:#34312c;--card:#1e1c19;--accent:#8cc3b0;--unlock:#2a2720;
--win:#7fc79f;--part:#e0bd5a;--stuck:#ee8f7f;--miss:#a19b91;--new:#8cc3b0;--fix:#a19b91;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.65 system-ui,"Noto Sans TC","PingFang TC",sans-serif}}
main{{max-width:52rem;margin:0 auto;padding:2rem 16px 4rem}}
h1{{font-size:1.6rem;margin:0 0 .25rem;text-wrap:balance}}
.lead{{color:var(--mute);margin:0 0 1.5rem;text-wrap:pretty}}
.lead a,.links a{{color:var(--accent)}}
.bar{{position:sticky;top:0;z-index:2;background:var(--bg);padding:.75rem 0;border-bottom:1px solid var(--line);margin-bottom:1rem}}
input[type=search]{{width:100%;font:inherit;padding:.6rem .8rem;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--fg)}}
input[type=search]:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.row{{display:flex;flex-wrap:wrap;gap:.4rem;align-items:center;margin-top:.6rem}}
.row .lbl{{color:var(--mute);font-size:.85rem;min-inline-size:3em}}
.chip,.act{{font:inherit;font-size:.85rem;padding:.25rem .7rem;min-block-size:2rem;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--fg);cursor:pointer}}
.chip[aria-pressed=true]{{background:var(--accent);border-color:var(--accent);color:var(--bg)}}
.chip:focus-visible,.act:focus-visible,summary:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.count{{color:var(--mute);font-size:.85rem;margin-inline-start:auto}}
h2{{font-size:1rem;color:var(--mute);margin:1.75rem 0 .5rem;font-weight:600}}
.line{{background:var(--card);border:1px solid var(--line);border-radius:10px;margin:.5rem 0}}
.line summary{{cursor:pointer;padding:.75rem 1rem;list-style:none;display:grid;gap:.25rem}}
.line summary::-webkit-details-marker{{display:none}}
.t{{font-weight:600}}
.t::before{{content:"▸";display:inline-block;margin-inline-end:.4rem;color:var(--mute);transition:rotate .2s}}
.line[open] .t::before{{rotate:90deg}}
.meta{{color:var(--mute);font-size:.82rem}}
.badges{{display:flex;flex-wrap:wrap;gap:.3rem}}
.b{{font-size:.75rem;padding:.05rem .5rem;border-radius:4px;border:1px solid currentColor}}
.k-新能力{{color:var(--new);font-weight:600}}.k-糾錯{{color:var(--fix)}}
.r-勝{{color:var(--win)}}.r-部分改善{{color:var(--part)}}.r-僵持{{color:var(--stuck)}}.r-缺{{color:var(--miss)}}.lv{{color:var(--mute)}}
.body{{padding:0 1rem 1rem}}
dl{{display:grid;grid-template-columns:max-content 1fr;gap:.35rem 1rem;margin:.5rem 0}}
dt{{color:var(--mute);font-size:.9rem}} dd{{margin:0;overflow-wrap:anywhere}}
@media (max-width:560px){{dl{{grid-template-columns:1fr}} dt{{margin-top:.4rem}}}}
.story,.support{{margin:.6rem 0;text-wrap:pretty;overflow-wrap:anywhere}}
.support{{font-size:.9rem;color:var(--mute)}}
.unlock{{background:var(--unlock);border-radius:8px;padding:.6rem .8rem;margin:.25rem 0 .75rem}}
.unlock .tag{{display:block;font-size:.75rem;color:var(--accent);font-weight:600;margin-bottom:.2rem}}
.links{{font-size:.85rem;color:var(--mute);margin:.5rem 0 0;overflow-wrap:anywhere}}
code{{font-family:ui-monospace,Menlo,monospace;font-size:.88em;background:color-mix(in srgb,var(--line) 60%,transparent);padding:.05em .3em;border-radius:3px}}
mark{{background:color-mix(in srgb,var(--part) 35%,transparent);color:inherit;border-radius:2px}}
.empty{{color:var(--mute);text-align:center;padding:2rem 0}}
@supports (interpolate-size:allow-keywords){{
 :root{{interpolate-size:allow-keywords}}
 .line::details-content{{block-size:0;overflow:clip;transition:block-size .25s ease,content-visibility .25s allow-discrete}}
 .line[open]::details-content{{block-size:auto}}
}}
@media (prefers-reduced-motion:reduce){{.line::details-content,.t::before{{transition:none}}}}
footer{{color:var(--mute);font-size:.85rem;margin-top:3rem}}
</style></head><body><main>
<h1>Web 張力線</h1>
<p class="lead">把 <a href="https://github.com/GoogleChrome/modern-web-guidance">modern-web-guidance</a> 的新指南拆成問題線：誰在做、做了什麼、被什麼擋、做完之後擋住的東西退了沒。找靈感時看<b>新能力</b>那幾條的「解鎖」。
共 {len(items)} 條線（新能力 {n_new} 條），處理到上游 {state["last_release"]}。<a href="https://github.com/ianTPE/web-tension-lines">repo</a></p>
<div class="bar">
<input type="search" id="q" placeholder="搜尋：功能名、對手、指南…（Ctrl+F 也找得到摺起來的內容）" aria-label="搜尋問題線">
<div class="row"><span class="lbl">類型</span>{chips("kind", kinds)}</div>
<div class="row"><span class="lbl">戰報</span>{chips("result", results)}</div>
<div class="row"><span class="lbl">分組</span><button type="button" class="chip" aria-pressed="true" data-g="group">對手組</button><button type="button" class="chip" aria-pressed="false" data-g="guide">指南</button>
<button type="button" class="act" id="all">全部展開</button><span class="count" id="count" role="status"></span></div>
</div>
<div id="list">{cards}</div>
<p class="empty" id="empty" hidden>沒有符合的線</p>
<footer>上游指南為 CC-BY 4.0（GoogleChrome/modern-web-guidance）。「解鎖」是發想，不是指南原文。這頁由 <code>scripts/build_page.py</code> 從 <code>lines/</code> 產生。</footer>
</main>
<script>
const list=document.getElementById('list'),q=document.getElementById('q'),cnt=document.getElementById('count'),empty=document.getElementById('empty');
const cards=[...list.querySelectorAll('details.line')];
const orig=new Map(cards.map(c=>[c,c.innerHTML]));
const f={{kind:'',result:''}};let groupBy='group';
function esc(s){{return s.replace(/[.*+?^${{}}()|[\\]\\\\]/g,'\\\\$&')}}
function highlight(c,term){{
  c.innerHTML=orig.get(c);
  if(!term)return;
  const re=new RegExp(esc(term),'gi');
  const w=document.createTreeWalker(c,NodeFilter.SHOW_TEXT);const nodes=[];
  while(w.nextNode())nodes.push(w.currentNode);
  for(const n of nodes){{if(!re.test(n.data))continue;re.lastIndex=0;
    const span=document.createElement('span');span.innerHTML=n.data.replace(/[&<>]/g,m=>({{'&':'&amp;','<':'&lt;','>':'&gt;'}}[m])).replace(re,m=>'<mark>'+m+'</mark>');
    n.replaceWith(...span.childNodes);}}
}}
function render(){{
  const term=q.value.trim();let shown=0;
  const groups=new Map();
  for(const c of cards){{
    const ok=(!f.kind||c.dataset.kind===f.kind)&&(!f.result||c.dataset.result===f.result)&&(!term||c.textContent.toLowerCase().includes(term.toLowerCase()));
    c.hidden=!ok;if(ok)shown++;
    highlight(c,term);
    if(term&&ok)c.open=true;
    const key=groupBy==='group'?c.dataset.group:c.querySelector('.meta').textContent.split(' · ')[0];
    if(!groups.has(key))groups.set(key,[]);groups.get(key).push(c);
  }}
  list.replaceChildren();
  [...groups.entries()].sort((a,b)=>b[1].filter(c=>!c.hidden).length-a[1].filter(c=>!c.hidden).length).forEach(([k,cs])=>{{
    const vis=cs.filter(c=>!c.hidden).length;
    const h=document.createElement('h2');h.textContent=k+'（'+vis+'）';h.hidden=!vis;list.append(h,...cs);
  }});
  cnt.textContent=shown+' / '+cards.length+' 條';empty.hidden=shown>0;
}}
document.querySelectorAll('.chip[data-f]').forEach(b=>b.addEventListener('click',()=>{{
  f[b.dataset.f]=b.dataset.v;
  document.querySelectorAll('.chip[data-f="'+b.dataset.f+'"]').forEach(x=>x.setAttribute('aria-pressed',x===b));render();}}));
document.querySelectorAll('.chip[data-g]').forEach(b=>b.addEventListener('click',()=>{{
  groupBy=b.dataset.g;document.querySelectorAll('.chip[data-g]').forEach(x=>x.setAttribute('aria-pressed',x===b));render();}}));
const all=document.getElementById('all');
all.addEventListener('click',()=>{{const open=all.textContent==='全部展開';cards.forEach(c=>{{if(!c.hidden)c.open=open}});all.textContent=open?'全部收合':'全部展開';}});
let t;q.addEventListener('input',()=>{{clearTimeout(t);t=setTimeout(render,120)}});
render();
</script></body></html>
'''
(ROOT / "docs").mkdir(exist_ok=True)
(ROOT / "docs" / "index.html").write_text(page, encoding="utf-8")
print(f"docs/index.html: {len(items)} lines ({n_new} 新能力)")
