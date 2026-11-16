---
guide: identify-inp-causes
category: performance
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/performance/identify-inp-causes.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 找出 INP 不佳的原因

%% line-start id="mwg:identify-inp-causes" %%
## 用 Event Timing 把 INP 拆成三段，先分清是哪一段慢
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：用 `web-vitals/attribution` 的 `onINP()` 取得最慢互動的 `inputDelay`、`processingDuration`、`presentationDelay` 與互動目標，送回分析服務
- 被什麼擋：互動慢與否取決於使用者操作、裝置與網路，實驗室資料只重現一小部分真實情境，很難診斷；不拆分就容易直接跳去改互動處理程式（引用："Lab data only replicates a small subset of real user scenarios so measuring the causes of slow INP in the field is essential."）
- 戰報：部分改善——拆成三段後可以判斷問題出在其他已在跑的程式、這次互動的處理程式，還是之後的渲染；不支援 Event Timing 的瀏覽器量不到 INP（官方宣稱）

經過：INP 很差，第一反應是去優化按鈕的 click handler，結果慢的其實是點擊前就在跑的別的腳本，或是之後的重繪。三段拆分先指出方向，再往下挖。
%% line-end %%

### 細節（不索引）
- 對手組：效能量測失真或有盲點
- 支援狀態：Event timing performance entries：Newly available（2025-12-12）。Supported by: Chrome 76, Edge 79, Firefox 89, Safari 26.2
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：四大瀏覽器都能回報「哪個按鈕、慢在哪一段」，可以做一張依互動目標排序的慢互動清單，直接指到要修的元件
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:identify-inp-causes:2" %%
## 用 LoAF 分開樣式重算與排版的時間，取代沉重的 JS Self-Profiling
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：從 LoAF 讀 `forcedStyleDuration`／`forcedLayoutDuration`（腳本內強制同步）與 `styleDuration`／`layoutDuration`（影格渲染階段），分開送回；不支援分開欄位時退回合併的 `forcedStyleAndLayoutDuration`、`totalStyleAndLayoutDuration`
- 被什麼擋：用 JS Self-Profiling API 做完整效能追蹤太重，本身就可能造成效能問題（引用："A full performance trace using the JS Self-Profiling API is a heavyweight solution that is liable to cause performance problems."）
- 戰報：部分改善——輕量 API 就能分辨是選擇器太貴或失效範圍太廣（樣式），還是幾何計算或讀寫交錯的 layout thrashing（排版），兩者修法不同；僅 Chrome／Edge 支援，可不加 fallback 直接用（官方宣稱）

經過：知道「處理時間長」還不夠，樣式與排版是兩種病。以前要靠完整 profile 才看得出來，但在正式環境開 profiler 自己就拖慢頁面。LoAF 直接把兩者拆開報。
%% line-end %%

### 細節（不索引）
- 對手組：效能量測失真或有盲點
- 支援狀態：Long animation frames performance entries：Limited availability。Supported by: Chrome 123, Edge 123；Unsupported in: Firefox, Safari
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：正式環境的慢互動報告可以直接標「這次是樣式重算」或「這次是強制排版」，附上觸發的腳本與函式位置，修的人不用先在本機重現。資料只來自 Chromium
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出
