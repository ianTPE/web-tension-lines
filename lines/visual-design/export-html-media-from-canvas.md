---
guide: export-html-media-from-canvas
category: visual-design
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/visual-design/export-html-media-from-canvas.md
first_seen: 2026-11-16（v1.0.0，回溯拆出；上游自 v0.0.177 起就有這份指南）
license: CC-BY-4.0（上游指南）
---

# 把 HTML 內容從 canvas 匯出成圖片或影片

%% line-start id="mwg:export-html-media-from-canvas" %%
## 讓瀏覽器自己把 HTML 畫進 canvas 再匯出，不用函式庫重畫 DOM
- 做法：把要匯出的 HTML 放進 `<canvas content="drawable">`，用 `drawElementImage()` 畫出後，以 `toDataURL()`、`toBlob()`、`captureStream()` 匯出成圖片或影片
- 對手：舊做法靠肥大的第三方函式庫逐一解析 DOM 節點和 CSS 屬性、在 canvas 上重建一份仿製品，運算量大、容易出錯，而且常常不支援新的 CSS 排版功能（引用："This approach is computationally expensive, error-prone, and frequently fails to support modern CSS layout features."）
- 退路：失去主要好處——退回 `html2canvas`、`dom-to-image`、`snapdom`、`rrweb` 等第三方函式庫（或顯示不支援警告），肥大、易錯且不支援現代 CSS 排版的問題又回來了
- 解鎖：由瀏覽器原生渲染引擎把真實 DOM 子樹精準畫進 canvas，能直接用 `toDataURL()`、`toBlob()`、`captureStream()` 高效率匯出像素級一致的圖片或影片串流

經過：「把這塊畫面存成圖」一直得靠函式庫在 JS 裡重新實作一次瀏覽器的排版與繪製，遇到新的 CSS 功能就畫錯。新 API 讓真正的渲染引擎把 HTML 子樹畫進 canvas，之後用 canvas 既有的匯出方法即可。在 Chrome 以外，退路就是原本那些函式庫，對手原封不動。
%% line-end %%

### 細節（不索引）
- 對手組：手工重現瀏覽器渲染
- 支援狀態：HTML-in-Canvas：Limited（Chrome 157 起，2026-11-03 進穩定版；Firefox、Safari 不支援）。v1.0.1 起指南的 fallback 段落已改為 "Browser support for HTML-in-canvas: Limited availability. Supported by: Chrome 157 (Nov 2026) and Edge 157 (Nov 2026)."，與先前依 PROMPT.md「已驗證的支援資料偏差」所做的判定一致
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：儀表板、排好版的文件、互動圖表可以一鍵存成和畫面一模一樣的 PNG，或用 `captureStream()` 把一段 HTML 互動錄成影片，不必載入截圖函式庫。目前僅 Chrome 157 起
- 現成 demo：無。WICG 範例沒有示範 `toBlob()`／`captureStream()` 匯出；相關討論見 https://github.com/WICG/html-in-canvas/issues/81 （截圖函式庫 snapdom 的使用情境）
- 本 repo demo：https://iantpe.github.io/web-tension-lines/demos/ledger-chart/ （`docs/demos/ledger-chart/`）。同一張圖用 `toBlob()` 下載 PNG、用 `captureStream()` 錄 5 秒 WebM，輸出含標籤文字。2026-11-16 在 Chrome 157 上跑過，但只是自己寫的 demo 能動，不等於驗證了指南的戰報，ledger 的證據仍是 `宣稱`
- 規格來源：https://github.com/WICG/html-in-canvas （四槽只依上游指南判定，這裡僅供追蹤）
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出（使用者指定 HTML-in-Canvas 的四份指南；不在每週差異內）；2026-11-16 支援狀態由「無瀏覽器支援」更正為 Limited（Chrome 157 已於 2026-11-03 進穩定版，指南 fallback 段落過時）；2026-11-18 改為槽 v2；2026-11-18（v1.0.1）上游 fallback 段落改為 Limited（Chrome／Edge 157），與既有判定一致，支援狀態與戰報不變
