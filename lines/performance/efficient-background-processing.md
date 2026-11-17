---
guide: efficient-background-processing
category: performance
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/performance/efficient-background-processing.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 有效率的背景處理

%% line-start id="mwg:efficient-background-processing" %%
## 用 contentvisibilityautostatechange 在元件不被渲染時暫停動畫與輪詢
- 做法：對重元件設 `content-visibility: auto` 與 `contain-intrinsic-size`，監聽 `contentvisibilityautostatechange`：`event.skipped` 為真時停掉 canvas 動畫、WebGL 渲染、高頻 WebSocket 輪詢，否則恢復
- 對手：缺——指南只說要在元件沒被渲染時暫停重工作以節省系統資源與電量，沒說工作照跑時具體出了什麼事
- 退路：保住主要行為——不支援時退回 `IntersectionObserver` 加 `rootMargin` 仍可近似暫停工作，但失去渲染時機連動
- 解鎖：監聽 `contentvisibilityautostatechange` 緊貼渲染生命週期，元件被跳過渲染時自動暫停重活

經過：捲出畫面的模擬、圖表、即時資料面板照樣每一幀在算。綁上這個事件後，瀏覽器決定不渲染它時就停，準備渲染時再開。和 `IntersectionObserver` 不同，它對應的是渲染時機而不是幾何上的可見。
%% line-end %%

### 細節（不索引）
- 對手組：工作花在看不到的地方
- 支援狀態：content-visibility：Newly available（2025-09-15）。Supported by: Chrome 108, Edge 108, Firefox 130, Safari 26（指南把 `contentvisibilityautostatechange` 一併列在此狀態下）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：一頁放很多個即時 canvas（多支股票走勢、多個物理模擬、多個 WebGL 預覽），只有接近畫面的幾個在跑，其他自動暫停，筆電風扇不再狂轉
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:efficient-background-processing:2" %%
## contentvisibilityautostatechange 在部分實作不冒泡，委派要用 capture
- 做法：把監聽器直接掛在設了 `content-visibility: auto` 的元素上；要在父層委派時加 `{ capture: true }`
- 對手：這個事件在部分瀏覽器實作中不冒泡，掛在父層的一般監聽器收不到（引用："The `contentvisibilityautostatechange` event does not bubble in some browser implementations."）
- 退路：保住主要行為——不支援此事件時退回 `IntersectionObserver` 偵測畫面進出，不涉及冒泡漏接
- 解鎖：（缺）

經過：照一般事件委派的習慣在 `document` 上監聽，某些瀏覽器裡事件不往上傳，暫停邏輯從來沒跑過，而且不會報錯。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：content-visibility：Newly available（同上）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
