# web-tension-lines

**繁體中文** · [English](README.en.md)

**[線上瀏覽](https://iantpe.github.io/web-tension-lines/)**（可搜尋、可篩選、可展開；[英文版](https://iantpe.github.io/web-tension-lines/en/)、[週記](https://iantpe.github.io/web-tension-lines/weekly/)、[demo](https://iantpe.github.io/web-tension-lines/demos/ledger-chart/)、[靈感](https://iantpe.github.io/web-tension-lines/ideas/)、[對手組關係圖（英文）](https://iantpe.github.io/web-tension-lines/en/graph/)）

每週檢查 [GoogleChrome/modern-web-guidance](https://github.com/GoogleChrome/modern-web-guidance) 的新指南，用張力句四槽（做法／對手／退路／解鎖）拆成問題線。拆出來的不是功能清單，而是「哪個新做法擋掉了哪個老問題、退回時怎麼辦」，再從「解鎖」與「發想」去想新應用。

## 什麼是「問題線」

一條問題線用四個槽記下一個問題的形狀：

| 槽 | 問的是 | 例子（`dynamic-sort` 指南） |
|---|---|---|
| 做法 | 用什麼做法處理什麼 | 排序時用 `moveBefore()` 把既有節點搬到新順序 |
| 對手 | 舊做法具體在哪個時刻出事 | 用 `innerHTML` 重建清單，焦點、捲動位置、圖片狀態全部丟失 |
| 退路 | 不支援時怎麼退、失去什麼 | 保住主要行為——Safari 缺 `moveBefore()` 改用 `append()`，順序正確但項目內焦點與狀態會重設 |
| 解鎖 | 從指南原文來看現在做得到什麼 | 不用重建 DOM 就能把既有項目直接搬到新順序，保住項目內焦點、iframe 與動畫狀態 |

重點在對手、退路與解鎖。「對手」要指得出一個看得到的現象，「效能不好」「寫起來麻煩」這種只有標籤的不算。「退路」四選一並寫出退回後失去什麼。「解鎖」必須能指回指南原文；指南沒寫到的對手或解鎖就記「缺」，不替它補。

這樣拆的好處是：好幾份指南擋的如果是同一個對手（例如都在處理「隱藏方式把鍵盤使用者擋在外面」），在 `ledger.csv` 按「對手組」一篩就看得到。

四槽來自 [ctxfst](https://github.com/ctxfst) 的張力句四槽教練，原始定義見 [skill-line-coach/references/four-slot-coach.md](https://github.com/ctxfst/skill-line-coach/blob/main/references/four-slot-coach.md)。原本是寫筆記時用的教練規則，這裡把它拿來拆別人寫的功能指南；遷移到槽 v2 的調整（包括退路分類、由規則推出戰報）寫在 [PROMPT.md](PROMPT.md)。

## 結構

| 路徑 | 內容 |
|---|---|
| `lines/<分類>/<guide-id>.md` | 一份指南一個檔，裡面一到三條問題線。每條線包在 `%% line-start id="…" %%` 和 `%% line-end %%` 之間（Obsidian 的註解語法，畫面上看不到），格式照 [CtxFST 規格](https://github.com/ctxfst/skill-line-coach/blob/main/references/ctxfst-spec.md)，可直接用 skill-line-coach 的 `shape_layer.py` 逐條建索引；標記外的「細節」是給人看的補充 |
| `ledger.csv` | 累積表，一條線一列；按「對手組」篩選可以看到哪些老問題被反覆對付 |
| `weekly/<日期>.md` | 每期週記：這週的對手、僵持中的線、**本週靈感**（用新能力組出的應用點子與小 demo） |
| `docs/index.html`、`docs/en/index.html` | 一頁看完所有線（中文版、英文版）：可搜尋（Ctrl+F 也找得到摺起來的內容）、按類型和戰報篩選、按對手組或指南分組。由 `scripts/build_page.py` 產生，每週自動重建 |
| `docs/ideas/`、`docs/en/ideas/` | 靈感頁：只列新能力的線，依「現在能不能用」分成今天就能用、漸進增強、只在支援的瀏覽器有效、先追蹤，可依主題篩選。由 `scripts/build_ideas.py` 每週重建 |
| `docs/en/graph/` | 對手組關係圖（英文網頁）：每個對手組一個圓，出現在同一份指南就連線，點進去看該組的線。由 `scripts/build_graph.py` 每週重建 |
| `docs/weekly/` | 週記的網頁版：目錄頁加每篇一頁，週記裡的 `mwg:…` 可以點，會跳到主頁並展開那條線。由 `scripts/build_weekly.py` 產生 |
| `docs/demos/` | 用新能力做的模組 demo。目前有 `ledger-chart/`：用 HTML-in-Canvas 畫的對手組戰報圖，標籤是真 DOM，可搜尋、可匯出（僅 Chrome 157 起，其他瀏覽器走 fallback）。資料由 `scripts/build_demo.py` 從 `ledger.csv` 產生；英文版在 `docs/en/demos/ledger-chart/` |
| `groups/` | 每個對手組一頁的 Obsidian 索引（加一頁 `對手組總覽`）：列出該組的線、常一起出現的組。用 Obsidian 開這個 repo、打開關係圖，就看得到哪些對手常在同一份指南出現。由 `scripts/build_groups.py` 每週重建 |
| `docs/demos/` 底下其餘 | 可以直接在瀏覽器試的新能力小範例（錯開進場、滑動底線、捲動進出場、手風琴、自動對比文字、宣告式按鈕、預覽卡、深淺色 token），每頁先檢查支援度、不支援時示範退路。總覽在 `docs/demos/index.html`；英文版在 `docs/en/demos/`。手寫，不由腳本產生 |
| `i18n/en.json` | 英文版網頁用的譯文。線檔維持中文，每週任務會替新線補上譯文；缺譯時英文頁退回顯示中文 |
| `wants.md` | 你自己「想做但卡住的事」。有寫東西時，週記會多一節「對到你的清單」，列出剛好擋掉這些問題的新功能 |
| `.agents/skills/web-tension-lines/` | 顧問型 Agent Skill：從開發者描述的阻礙檢索相關線，回報新做法、戰報、限制與原文 |
| `PROMPT.md` | 每週自動任務的完整指示 |
| `scripts/weekly.sh` | 抓上游、算差異、叫 `claude -p` 跑 PROMPT.md |
| `state.json` | 上次處理到的上游 commit |

## 判讀

- **退路**：瀏覽器不支援時怎麼退、失去什麼，四選一加一句說明：`不需要`（`Widely` 或 `不適用`）、`保住主要行為`、`失去主要好處`、`沒說`。
- **戰報**：不直接判，由 `支援狀態` 與 `退路` 規則推出：`勝`（`Widely` 或 `不適用`）、`部分改善`（`Newly` 或退路為 `保住主要行為`）、`僵持`（其餘）。不再有 `缺`。
- **證據**：一律 `宣稱`，因為資料來自官方指南。自己在瀏覽器實測過的，手動改成 `實測`。
- **類型**：`新能力`（新平台功能讓某件事變得可行）或 `糾錯`（糾正常見錯誤，用的是早就能用的功能）。找靈感時只看新能力。
- **解鎖**：來自指南原文的具體可達成能力，能指回原句；沒有就寫 `（缺）`。
- **發想（非指南原文）**：新能力的線才有的延伸應用點子，「以前卡在哪 → 現在能做出什麼」，不是指南原文。
- **對手有無 = 缺**：指南推薦了新做法，卻沒說舊做法具體壞在哪。

## Agent Skill

Kimi Code 會自動發現專案內的 `.agents/skills/web-tension-lines/SKILL.md`。可手動呼叫：

```text
/skill:web-tension-lines 以前不敢做可拖曳的儀表板，因為圖表一搬就重新載入
```

skill 會用症狀與對手檢索一到三條相關線，附上戰報、支援限制、證據狀態與上游指南；不會自動改碼或開 issues。其他支援 Agent Skills 的工具可把同一目錄複製或連結到自己的 skills 掃描目錄。

也可不透過代理直接檢索，只需要 Python 3，沒有第三方依賴：

```bash
python3 .agents/skills/web-tension-lines/scripts/search.py --kind 新能力 --limit 3 "拖曳 圖表 重新載入"
python3 .agents/skills/web-tension-lines/scripts/search.py --id mwg:move-dom-element-without-losing-state --json
```

查詢同時比對中英文；加 `--lang en` 可輸出英文。詳細選項見 `--help`。

## 排程

使用者 crontab，每週三 09:00（上游多在週一、週二發版）：

```
0 9 * * 3 /path/to/web-tension-lines/scripts/weekly.sh
```

上游沒有新 commit 就直接結束，不呼叫 claude。有拆出新線時，腳本會自動 commit 並 push 到 `origin main`。執行紀錄在 `logs/<日期>.log`（不進 git）。手動跑一次：`scripts/weekly.sh`。

## 附錄：HTML-in-Canvas 速查

[HTML-in-Canvas](https://github.com/WICG/html-in-canvas)（WICG 提案）讓 `<canvas>` 的子元素照常排版、留在 DOM 裡，再由你決定畫進 canvas 的哪裡。畫出來的是瀏覽器真正繪製的結果，文字仍然能被搜尋、選取、翻譯、被螢幕閱讀器讀到。

**支援**：Chrome、Edge 157 起（2026-11 進穩定版）；Firefox、Safari 不支援。上游指南標為 Limited。

### 什麼時候用

| 做法 | 文字能搜尋、選取、讀屏 | 直接存成 PNG 或影片 | 像素特效、WebGL、大量資料點 |
|---|---|---|---|
| 一般 HTML／SVG | ✅ 天生就可以 | ❌ 要靠 html2canvas 等函式庫重畫，新的 CSS 常畫錯 | ❌ |
| 一般 canvas | ❌ 文字變成像素，要另外維護隱藏的 DOM | ✅ `toBlob()` | ✅ |
| HTML-in-Canvas | ✅ | ✅ | ✅ |

**不需要 canvas 的東西，用一般 HTML 就好**，所有瀏覽器都支援。HTML-in-Canvas 值得用在本來就必須用 canvas 的地方：輸出影片或圖片、套 shader 或 WebGL、3D 場景裡的真表單、整個畫面都在 canvas 上的遊戲、白板、地圖。

### 五個基本元件

| 元件 | 作用 |
|---|---|
| `<canvas content="drawable">` | 讓 canvas 的子元素參與排版（預設的 `fallback` 只當替代內容） |
| 子元素加 `drawable` | 標記可以被畫進 canvas 的元素；巢狀的 `drawable` 會被排除，要另外畫 |
| `paint` 事件、`canvas.requestPaint()` | 子元素外觀改變時觸發 `paint`，在裡面畫；需要每幀重畫時呼叫 `requestPaint()` |
| `ctx.drawElementImage(el, x, y)` | 2D：畫出元素最新的快照，瀏覽器自動把點擊位置和焦點框對齊到畫的位置。WebGL 用 `texElementSubImage2D()`、WebGPU 用 `drawElementImageToTexture()` 畫進貼圖 |
| `canvas.updateElementGeometry(el, { canvasTransform })` | 3D 時要自己告訴瀏覽器元素畫在哪裡，點擊和讀屏才對得上；2D 由 `drawElementImage()` 自動處理 |

另有 `canvas.captureElementImage(el)`：取得元素快照（例如拿來決定貼圖大小，或傳到 worker 給 `OffscreenCanvas` 畫）。

### 最小範例：畫一個可輸入的表單，並匯出成 PNG

```html
<canvas id="canvas" content="drawable" style="width: 400px; height: 200px;">
  <form id="form" drawable>
    <label>名字 <input></label>
  </form>
</canvas>
<button id="download">下載 PNG</button>

<script>
  const canvas = document.getElementById("canvas");
  const ctx = canvas.getContext("2d");
  const form = document.getElementById("form");

  if (!("content" in HTMLCanvasElement.prototype)) {
    // 不支援：退路是把 HTML 用 CSS 疊在 canvas 上，或乾脆不用 canvas
  }

  canvas.onpaint = () => {
    ctx.reset();
    ctx.drawElementImage(form, 20, 20); // 點擊與打字會自動對到這個位置
  };

  // canvas 格線對齊裝置像素，避免模糊；不要寫在 onpaint 裡
  new ResizeObserver(([entry]) => {
    const box = entry.devicePixelContentBoxSize?.[0];
    canvas.width = box ? box.inlineSize : Math.round(entry.contentRect.width * devicePixelRatio);
    canvas.height = box ? box.blockSize : Math.round(entry.contentRect.height * devicePixelRatio);
    canvas.requestPaint();
  }).observe(canvas, { box: "device-pixel-content-box" });

  // 匯出用 canvas 既有的方法，輸出包含表單的樣子
  document.getElementById("download").onclick = () =>
    canvas.toBlob(blob => {
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = "form.png";
      a.click();
    });
</script>
```

錄影改用 `canvas.captureStream()` 接 `MediaRecorder`；需要逐幀精確的影片，要自己逐幀畫、再用 WebCodecs 編碼。

### 注意

- **跨來源內容畫不進去**：跨來源的 `<iframe>`、圖片、`url()` 背景都不會出現在畫面上。拼字錯誤標記、已造訪連結的顏色、自動填入中的值等隱私資訊也會被排除。
- **焦點框和游標會被畫出來**，不必自己補。
- **3D 情境要每幀呼叫 `updateElementGeometry()`**，否則點不到、讀屏的位置也不對。
- **退路**：疊一層 HTML 在 canvas 上（失去匯出和特效），或用 `three-html-render` polyfill。匯出則退回 html2canvas 等函式庫。

### 範例在哪裡

- **WICG 官方 demo**（要用 Chrome 157 以上開）：
  - [complex-text](https://wicg.github.io/html-in-canvas/Examples/complex-text.html)：旋轉的複雜文字
  - [pie-chart](https://wicg.github.io/html-in-canvas/Examples/pie-chart.html)：多行標籤的圓餅圖
  - [webGL](https://wicg.github.io/html-in-canvas/Examples/webGL.html)：把 HTML 貼在 3D 卡片上
  - [webgpu-jelly-slider](https://wicg.github.io/html-in-canvas/Examples/webgpu-jelly-slider/)：果凍效果的滑桿
  - [nested-sparkles](https://wicg.github.io/html-in-canvas/Examples/nested-sparkles.html)：巢狀的 `drawable` 元素
- **本 repo 的 demo**：[對手組戰報圖](https://iantpe.github.io/web-tension-lines/demos/ledger-chart/)（[英文](https://iantpe.github.io/web-tension-lines/en/demos/ledger-chart/)），示範匯出 PNG 和錄影。
- **實際產品**：Remotion 的瀏覽器端渲染可以選用 HTML-in-Canvas 截取每一幀（[文件](https://www.remotion.dev/docs/client-side-rendering/html-in-canvas)）。
- **四條相關的問題線**（附上游指南全文連結）：`mwg:expose-canvas-content-to-browser-features`、`mwg:export-html-media-from-canvas`、`mwg:interactive-content-in-3d-scenes`、`mwg:apply-webgl-shaders`，在 `lines/visual-design/`。

## 授權

上游指南為 CC-BY 4.0。這裡的引文與摘要若要公開發表，請標註來源：GoogleChrome/modern-web-guidance。
