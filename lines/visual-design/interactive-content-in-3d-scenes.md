---
guide: interactive-content-in-3d-scenes
category: visual-design
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/visual-design/interactive-content-in-3d-scenes.md
first_seen: 2026-11-16（v1.0.0，回溯拆出；上游自 v0.0.177 起就有這份指南）
license: CC-BY-4.0（上游指南）
---

# 在 3D 場景裡放可互動的 HTML 內容

%% line-start id="mwg:interactive-content-in-3d-scenes" %%
## 把真 DOM 投影進 3D 場景，互動交還給瀏覽器
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：把 `drawable` 的 HTML 元素複製成貼圖（WebGL `texElementSubImage2D()`、WebGPU `drawElementImageToTexture()`、Three.js `HTMLTexture`），再用 `canvas.updateElementGeometry()` 把元素的位置對到 3D 畫面上
- 被什麼擋：（缺）只說不必再寫複雜的 raycasting 或自訂事件處理，沒說手寫版在哪個情境出錯（引用："they retain full interactivity—allowing users to click buttons, select text, and trigger focus states natively without requiring complex raycasting or custom event handling"）
- 戰報：僵持——元素留在 DOM 排版樹裡，按鈕點擊、文字選取、焦點狀態都由瀏覽器處理；但只有 Chrome 157 起支援，其他瀏覽器的 fallback 是把 HTML 用 CSS 疊在 canvas 上，或用 `three-html-render` polyfill（官方宣稱）

經過：3D 場景裡的面板以前是一張貼圖，點擊要自己用 raycasting 換算、再手動派送事件。新 API 讓貼圖背後仍是真元素，開發者只要每一幀把 MVP 矩陣換算成 `canvasTransform` 告訴瀏覽器它畫在哪裡。對手只被描述成「複雜」，屬於工作量而不是可觀察的失敗；矩陣同步仍得自己做，Three.js 則由 `InteractionManager` 代勞。
%% line-end %%

### 細節（不索引）
- 對手組：canvas裡手寫互動
- 支援狀態：HTML-in-Canvas：Limited（Chrome 157 起，2026-11-03 進穩定版；Firefox、Safari 不支援）。指南的 fallback 段落仍寫 "HTML-in-canvas is not natively supported by any major browser yet."，已過時，照 PROMPT.md「已驗證的支援資料偏差」判
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：3D 場景裡的螢幕、看板、控制面板可以是真的表單和按鈕：能打字、能選字、能用鍵盤聚焦，不必自己寫 raycasting 轉事件。適合產品展示、3D 編輯器裡的屬性面板。目前僅 Chrome 157 起
- 現成 demo：[webGL](https://wicg.github.io/html-in-canvas/Examples/webGL.html)（`texElementSubImage2D()` 把 HTML 貼在 3D 卡片上）；README 另連到 three.js `HTMLTexture` 的實驗版範例（WICG 範例，尚未自己實測）
- 規格來源：https://github.com/WICG/html-in-canvas （四槽只依上游指南判定，這裡僅供追蹤）
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出（使用者指定 HTML-in-Canvas 的四份指南；不在每週差異內）；2026-11-16 支援狀態由「無瀏覽器支援」更正為 Limited（Chrome 157 已於 2026-11-03 進穩定版，指南 fallback 段落過時）
