---
guide: expose-canvas-content-to-browser-features
category: visual-design
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/visual-design/expose-canvas-content-to-browser-features.md
first_seen: 2026-11-16（v1.0.0，回溯拆出；上游自 v0.0.177 起就有這份指南）
license: CC-BY-4.0（上游指南）
---

# 讓 canvas 內容被瀏覽器功能看見

%% line-start id="mwg:expose-canvas-content-to-browser-features" %%
## 把真 DOM 畫進 canvas，讓內容不再對瀏覽器隱形
- 做法：在 `<canvas content="drawable">` 裡放真正的 HTML 子元素（標 `drawable`），在 `onpaint` 用 `drawElementImage()` 畫出來（WebGL／WebGPU 則複製成貼圖）
- 對手：一般 `<canvas>` 畫出來的內容，螢幕閱讀器、搜尋索引、翻譯工具、頁內搜尋、列印全都看不到（引用："Regular `<canvas>` content is not exposed to browser features such as screen readers, indexing, translation tools, accessibility assistive tools, find-in-page, print, etc."）
- 退路：保住主要行為——退回把 HTML 用 CSS 疊在 canvas 上或用 polyfill，內容仍是真 DOM，只失去畫進 canvas 的效果
- 解鎖：把真實 DOM 放進 `<canvas content="drawable">` 繪製，讓內容同時保留讀屏、翻譯、搜尋與列印

經過：canvas 一向是一塊不透明的像素：畫上去的字不能選、不能搜尋、不能翻譯，輔助技術也讀不到。新 API 讓 canvas 的子元素照常排版、留在 DOM 樹裡，canvas 只負責決定怎麼畫，2D 情境下連點擊位置都由瀏覽器自動對齊。跨來源內容不能畫進去，而且只有 Chrome 支援，要顧到其他瀏覽器就得同時維護 fallback。
%% line-end %%

### 細節（不索引）
- 對手組：canvas內容對瀏覽器隱形
- 支援狀態：HTML-in-Canvas：Limited（Chrome 157 起，2026-11-03 進穩定版；Firefox、Safari 不支援）。v1.0.1 起指南的 fallback 段落已改為 "Browser support for HTML-in-canvas: Limited availability. Supported by: Chrome 157 (Nov 2026) and Edge 157 (Nov 2026)."，與先前依 PROMPT.md「已驗證的支援資料偏差」所做的判定一致
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：圖表、白板、地圖標籤這類畫在 canvas 上的文字可以被 Ctrl+F 找到、被翻譯、被螢幕閱讀器讀出來，不必另外維護一份隱藏的 DOM 副本。目前僅 Chrome 157 起
- 現成 demo：[pie-chart](https://wicg.github.io/html-in-canvas/Examples/pie-chart.html)（多行標籤的圓餅圖，`drawElementImage()`）、[complex-text](https://wicg.github.io/html-in-canvas/Examples/complex-text.html)（旋轉的複雜文字）、[nested-sparkles](https://wicg.github.io/html-in-canvas/Examples/nested-sparkles.html)（巢狀 `drawable`）（WICG 範例，尚未自己實測）
- 本 repo demo：https://iantpe.github.io/web-tension-lines/demos/ledger-chart/ （`docs/demos/ledger-chart/`）。圖表標籤是畫進 canvas 的真 DOM 按鈕，頁內搜尋、選字、Tab 鍵都能用。2026-11-16 在 Chrome 157 上跑過，但只是自己寫的 demo 能動，不等於驗證了指南的戰報，ledger 的證據仍是 `宣稱`
- 規格來源：https://github.com/WICG/html-in-canvas （四槽只依上游指南判定，這裡僅供追蹤）
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出（使用者指定 HTML-in-Canvas 的四份指南；不在每週差異內）；2026-11-16 支援狀態由「無瀏覽器支援」更正為 Limited（Chrome 157 已於 2026-11-03 進穩定版，指南 fallback 段落過時）；2026-11-18 改為槽 v2；2026-11-18 退路經交叉核對與仲裁更正為「保住主要行為」；2026-11-18（v1.0.1）上游 fallback 段落改為 Limited（Chrome／Edge 157），與既有判定一致，支援狀態與戰報不變
