#!/usr/bin/env python3
"""產生英文版的對手組關係圖：docs/en/graph/index.html。

節點是對手組（大小＝線數，顏色＝新能力占比），兩組出現在同一份指南就連線（粗細＝共同指南數）。
點節點列出該組的線，連回英文主頁。資料從 ledger.csv 與 i18n/en.json 讀，每週由 weekly.sh 重建。
"""
import csv, collections, itertools, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "en" / "graph" / "index.html"
LINE_RE = re.compile(r'%% line-start id="([^"]+)" %%\n(.*?)%% line-end %%', re.S)

en = json.load(open(ROOT / "i18n/en.json", encoding="utf-8"))
rows = [r for r in csv.DictReader(open(ROOT / "ledger.csv", encoding="utf-8", newline="")) if r["狀態"] == "有效"]
zh_title = {}
for p in (ROOT / "lines").glob("*/*.md"):
    for lid, body in LINE_RE.findall(p.read_text(encoding="utf-8")):
        zh_title[lid] = re.search(r"^## (.+)$", body, re.M).group(1).strip()

RESULT = en["result"]; KIND = en["kind"]
groups = collections.defaultdict(list)
guide_groups = collections.defaultdict(set)
for r in rows:
    groups[r["對手組"]].append(r)
    guide_groups[r["guide_id"]].add(r["對手組"])

names = sorted(groups, key=lambda g: (-len(groups[g]), g))
index = {g: i for i, g in enumerate(names)}
nodes = []
for g in names:
    rs = sorted(groups[g], key=lambda r: (r["類型"] != "新能力", r["guide_id"], r["line_id"]))
    lines = []
    for r in rs:
        t = en["lines"].get(r["line_id"], {})
        lines.append(dict(id=r["line_id"].replace(":", "--"), t=t.get("title") or zh_title.get(r["line_id"], r["line_id"]),
                          g=en["guides"].get(r["guide_id"], r["guide_id"]), r=RESULT.get(r["戰報"], r["戰報"]),
                          k=r["類型"] == "新能力"))
    nodes.append(dict(name=en["groups"].get(g, g), zh=g, n=len(rs), guides=len({r["guide_id"] for r in rs}),
                      newcap=sum(r["類型"] == "新能力" for r in rs),
                      res={RESULT.get(k, k): v for k, v in collections.Counter(r["戰報"] for r in rs).items()}, lines=lines))
co = collections.Counter()
for gs in guide_groups.values():
    for a, b in itertools.combinations(sorted(gs), 2):
        co[(a, b)] += 1
links = [dict(s=index[a], t=index[b], w=w) for (a, b), w in co.items()]
data = dict(nodes=nodes, links=links, total=len(rows), guides=len(guide_groups), win=RESULT["勝"], part=RESULT["部分改善"], stall=RESULT["僵持"])

HTML = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Opponent Graph · Web Tension Lines</title>
<meta name="description" content="Which old problems keep showing up together in modern-web-guidance: opponent groups linked when they appear in the same guide">
<style>
:root{--bg:#fbfaf7;--fg:#1f1d1a;--mute:#6b665e;--line:#e4e0d8;--card:#fff;--accent:#2f5d50;--edge:#b9b2a6;--lo:#c9d8cf;--hi:#2f5d50;--hl:#c4572e;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#161513;--fg:#ece8e1;--mute:#a19b91;--line:#34312c;--card:#1e1c19;--accent:#8cc3b0;--edge:#4a4640;--lo:#34433c;--hi:#8cc3b0;--hl:#f08a5d;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#161513;--fg:#ece8e1;--mute:#a19b91;--line:#34312c;--card:#1e1c19;--accent:#8cc3b0;--edge:#4a4640;--lo:#34433c;--hi:#8cc3b0;--hl:#f08a5d;color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:76rem;margin:0 auto;padding:1.5rem 16px 3rem}
a{color:var(--accent)} :focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.switch{font-size:.85rem;color:var(--mute);margin:0 0 .5rem}
h1{font-size:1.6rem;margin:0 0 .4rem;text-wrap:balance}
.lead{color:var(--mute);margin:0 0 1rem;max-width:52rem;text-wrap:pretty}
.controls{display:flex;flex-wrap:wrap;gap:.75rem 1.25rem;align-items:center;margin:0 0 .75rem;font-size:.9rem}
.controls input[type=search]{font:inherit;padding:.4rem .6rem;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--fg);min-width:14rem;flex:1 1 14rem;max-width:22rem}
.controls label{display:flex;gap:.5rem;align-items:center;color:var(--mute)}
.legend{display:flex;gap:.5rem;align-items:center;color:var(--mute);font-size:.82rem}
.legend .bar{width:70px;height:10px;border-radius:5px;background:linear-gradient(90deg,var(--lo),var(--hi))}
.wrap{display:grid;grid-template-columns:minmax(0,1fr) 22rem;gap:1rem}
@media (max-width:860px){.wrap{grid-template-columns:1fr}}
.stage{border:1px solid var(--line);border-radius:12px;background:var(--card);overflow:hidden;position:relative}
svg{display:block;width:100%;height:68vh;min-height:420px;touch-action:none;cursor:grab}
svg:active{cursor:grabbing}
.edge{stroke:var(--edge);stroke-linecap:round;stroke-opacity:.55}
.node circle{stroke:var(--card);stroke-width:1.5;cursor:pointer}
.node text{font-size:12px;fill:var(--fg);pointer-events:none;paint-order:stroke;stroke:var(--card);stroke-width:3px;stroke-linejoin:round}
.dim{opacity:.12}
.node.sel circle{stroke:var(--hl);stroke-width:3}
.edge.hot{stroke:var(--hl)}
.hint{position:absolute;left:10px;bottom:8px;font-size:.78rem;color:var(--mute);margin:0}
aside{border:1px solid var(--line);border-radius:12px;background:var(--card);padding:1rem;max-height:68vh;overflow:auto;min-height:420px}
@media (max-width:860px){aside{max-height:none;min-height:0}}
aside h2{font-size:1.1rem;margin:0 0 .2rem}
aside .zh{color:var(--mute);font-size:.85rem;margin:0 0 .6rem}
aside .stats{font-size:.85rem;color:var(--mute);margin:0 0 .75rem}
aside h3{font-size:.85rem;text-transform:uppercase;letter-spacing:.04em;color:var(--mute);margin:1rem 0 .4rem}
aside ul{list-style:none;margin:0;padding:0}
aside li{padding:.4rem 0;border-top:1px solid var(--line);font-size:.9rem}
aside li .m{display:block;color:var(--mute);font-size:.78rem}
.tag{display:inline-block;font-size:.72rem;padding:0 .4rem;border-radius:999px;border:1px solid var(--line);margin-left:.3rem;color:var(--mute)}
.tag.new{border-color:var(--accent);color:var(--accent)}
.nb{display:flex;flex-wrap:wrap;gap:.35rem}
.nb button,.list button{font:inherit;font-size:.82rem;border:1px solid var(--line);background:var(--bg);color:var(--fg);border-radius:999px;padding:.15rem .6rem;cursor:pointer}
.nb button:hover,.list button:hover{border-color:var(--accent)}
.list{margin-top:1.5rem}
.list h2{font-size:1rem;margin:0 0 .5rem}
.list .chips{display:flex;flex-wrap:wrap;gap:.35rem}
.list button span{color:var(--mute);margin-left:.3rem}
footer{color:var(--mute);font-size:.82rem;margin-top:2rem}
</style></head><body><main>
<p class="switch"><a href="../">← All problem lines</a> · <a href="../../">繁體中文</a> · <a href="../../weekly/">Weekly notes (Chinese)</a></p>
<h1>Opponent graph</h1>
<p class="lead">Each circle is an <b>opponent group</b>: one recurring way that old techniques fail. Two groups are linked when they appear in the same upstream guide, so groups that cluster together are problems that tend to come up together. Circle size is the number of lines; darker means more of them are <b>new capabilities</b>. <span id="summary"></span></p>
<div class="controls">
  <input type="search" id="q" placeholder="Find a group…" aria-label="Find an opponent group">
  <label>Show links shared by at least <input type="range" id="min" min="1" max="4" value="2"> <b id="minv">2</b> guides</label>
  <span class="legend">fewer new capabilities <span class="bar"></span> more</span>
</div>
<div class="wrap">
  <div class="stage"><svg id="g" role="img" aria-label="Force-directed graph of opponent groups"></svg><p class="hint">Drag to pan, scroll or pinch to zoom, click a circle for details.</p></div>
  <aside id="panel" aria-live="polite"><h2>Pick a group</h2><p class="stats">Click a circle, use the search box, or choose from the list below the graph.</p></aside>
</div>
<section class="list"><h2>All groups</h2><div class="chips" id="chips"></div></section>
<footer>Upstream guides are CC-BY 4.0 (GoogleChrome/modern-web-guidance). Lines are written in Chinese and translated; this page is generated by <code>scripts/build_graph.py</code>.</footer>
</main>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js"></script>
<script>
const DATA = __DATA__;
const N = DATA.nodes, L = DATA.links;
document.getElementById("summary").textContent = `${N.length} groups, ${DATA.total} lines from ${DATA.guides} guides.`;
const svg = d3.select("#g"), root = svg.append("g");
const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const share = d => d.n ? d.newcap / d.n : 0;
const color = d => d3.interpolateRgb(css("--lo"), css("--hi"))(Math.min(1, share(d) * 1.6));
const r = d => 5 + Math.sqrt(d.n) * 3.2;
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const code = s => esc(s).replace(/`([^`]+)`/g, "<code>$1</code>");
N.forEach((d, i) => d.i = i);
const nb = N.map(() => []);
L.forEach(l => { nb[l.s].push([l.t, l.w]); nb[l.t].push([l.s, l.w]); });

let minW = 2, selected = null;
const LABEL = matchMedia("(max-width:600px)").matches ? 25 : 15;
const edgeG = root.append("g"), nodeG = root.append("g");
const sim = d3.forceSimulation(N)
  .force("charge", d3.forceManyBody().strength(-260).distanceMax(420))
  .force("collide", d3.forceCollide(d => r(d) + 7))
  .force("x", d3.forceX().strength(.04)).force("y", d3.forceY().strength(.06));
let edges, nodes;

function draw() {
  const ls = L.filter(l => l.w >= minW).map(l => ({source: N[l.s], target: N[l.t], w: l.w}));
  edges = edgeG.selectAll("line").data(ls, d => d.source.i + "-" + d.target.i)
    .join("line").attr("class", "edge").attr("stroke-width", d => Math.min(6, .6 + d.w * .7));
  nodes = nodeG.selectAll("g.node").data(N, d => d.i).join(enter => {
    const g = enter.append("g").attr("class", "node").attr("tabindex", 0).attr("role", "button")
      .attr("aria-label", d => `${d.name}, ${d.n} lines`)
      .on("click", (e, d) => select(d)).on("keydown", (e, d) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); select(d); } })
      .on("mouseenter", (e, d) => hover(d)).on("mouseleave", () => hover(null))
      .call(d3.drag().on("start", (e, d) => { if (!e.active) sim.alphaTarget(.2).restart(); d.fx = d.x; d.fy = d.y; })
        .on("drag", (e, d) => { d.fx = e.x; d.fy = e.y; })
        .on("end", (e, d) => { if (!e.active) sim.alphaTarget(0); d.fx = null; d.fy = null; }));
    g.append("circle");
    g.append("text").attr("text-anchor", "middle");
    return g;
  });
  nodes.select("circle").attr("r", r).attr("fill", color);
  nodes.select("text").text(d => d.name).attr("dy", d => r(d) + 12).style("display", d => d.n >= LABEL ? null : "none");
  sim.force("link", d3.forceLink(ls).distance(d => 150 - Math.min(80, d.w * 14)).strength(d => Math.min(.6, .08 * d.w)));
  sim.alpha(.8).restart();
}
sim.on("tick", () => {
  edges.attr("x1", d => d.source.x).attr("y1", d => d.source.y).attr("x2", d => d.target.x).attr("y2", d => d.target.y);
  nodes.attr("transform", d => `translate(${d.x},${d.y})`);
});

function focusSet(d) {
  if (!d) return null;
  const s = new Set([d.i]); nb[d.i].forEach(([j, w]) => { if (w >= minW) s.add(j); }); return s;
}
function paint(d) {
  const s = focusSet(d);
  nodes.classed("dim", n => s && !s.has(n.i)).classed("sel", n => selected && n.i === selected.i);
  nodes.select("text").style("display", n => (n.n >= LABEL || (s && s.has(n.i))) ? null : "none");
  edges.classed("dim", e => s && !(e.source.i === d.i || e.target.i === d.i)).classed("hot", e => s && (e.source.i === d.i || e.target.i === d.i));
}
function hover(d) { paint(d || selected); }

function select(d) {
  selected = d; paint(d);
  const res = Object.entries(d.res).map(([k, v]) => `${esc(k)} ${v}`).join(" · ");
  const near = nb[d.i].slice().sort((a, b) => b[1] - a[1]).slice(0, 12);
  document.getElementById("panel").innerHTML = `
    <h2>${esc(d.name)}</h2><p class="zh">${esc(d.zh)}</p>
    <p class="stats">${d.n} lines from ${d.guides} guides · ${d.newcap} new capabilities<br>${res}</p>
    ${near.length ? `<h3>Often appears with</h3><div class="nb">${near.map(([j, w]) => `<button type="button" data-i="${j}">${esc(N[j].name)} <span>${w}</span></button>`).join("")}</div>` : ""}
    <h3>Lines</h3><ul>${d.lines.map(l => `<li><a href="../#${l.id}">${code(l.t)}</a>${l.k ? '<span class="tag new">new capability</span>' : ""}<span class="m">${esc(l.g)} · ${esc(l.r)}</span></li>`).join("")}</ul>`;
  document.querySelectorAll("#panel .nb button").forEach(b => b.onclick = () => select(N[+b.dataset.i]));
  if (matchMedia("(max-width:860px)").matches) document.getElementById("panel").scrollIntoView({behavior: "smooth", block: "start"});
}

// 標籤與外框不隨縮放變小
const zoom = d3.zoom().scaleExtent([.2, 5]).on("zoom", e => {
  root.attr("transform", e.transform);
  const k = e.transform.k;
  nodeG.selectAll("text").style("font-size", `${12 / k}px`).style("stroke-width", `${3 / k}px`);
});
svg.call(zoom);
// 佈局穩定後，把視野對準有連線的節點
function fit(animate) {
  const {width, height} = svg.node().getBoundingClientRect();
  const deg = new Set(); L.forEach(l => { if (l.w >= minW) { deg.add(l.s); deg.add(l.t); } });
  const pts = N.filter(n => deg.has(n.i) && n.x != null);
  if (!pts.length) return;
  const x0 = d3.min(pts, d => d.x - r(d)), x1 = d3.max(pts, d => d.x + r(d)), y0 = d3.min(pts, d => d.y - r(d)), y1 = d3.max(pts, d => d.y + r(d));
  const k = Math.min(3, .92 * Math.min(width / (x1 - x0), height / (y1 - y0)));
  const tr = d3.zoomIdentity.translate(width / 2, height / 2).scale(k).translate(-(x0 + x1) / 2, -(y0 + y1) / 2);
  (animate ? svg.transition().duration(500) : svg).call(zoom.transform, tr);
}
svg.call(zoom.transform, d3.zoomIdentity.translate(svg.node().getBoundingClientRect().width / 2, svg.node().getBoundingClientRect().height / 2).scale(.6));
let fitted = false;
sim.on("end.fit", () => { if (!fitted) { fitted = true; fit(true); } });
addEventListener("resize", () => fit(false));

document.getElementById("min").oninput = e => { minW = +e.target.value; document.getElementById("minv").textContent = minW; draw(); paint(selected); };
document.getElementById("q").oninput = e => {
  const q = e.target.value.trim().toLowerCase();
  if (!q) return paint(selected);
  const hit = new Set(N.filter(n => n.name.toLowerCase().includes(q) || n.zh.includes(q)).map(n => n.i));
  nodes.classed("dim", n => !hit.has(n.i));
  nodes.select("text").style("display", n => hit.has(n.i) ? null : "none");
  edges.classed("dim", true);
};
document.getElementById("q").onkeydown = e => {
  if (e.key !== "Enter") return;
  const q = e.target.value.trim().toLowerCase();
  const m = N.find(n => n.name.toLowerCase().includes(q) || n.zh.includes(q));
  if (m) select(m);
};
document.getElementById("chips").innerHTML = N.map(n => `<button type="button" data-i="${n.i}">${esc(n.name)}<span>${n.n}</span></button>`).join("");
document.querySelectorAll("#chips button").forEach(b => b.onclick = () => select(N[+b.dataset.i]));
matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => nodes.select("circle").attr("fill", color));
draw();
</script>
</body></html>
"""

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(HTML.replace("__DATA__", json.dumps(data, ensure_ascii=False, separators=(",", ":"))), encoding="utf-8")
print(f"docs/en/graph/index.html: {len(nodes)} groups, {len(links)} links")
