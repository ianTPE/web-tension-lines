---
guide: identify-heavy-scripts
category: performance
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/performance/identify-heavy-scripts.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 找出執行沉重的 JavaScript

%% line-start id="mwg:identify-heavy-scripts" %%
## 用 Long Animation Frames 在實際使用者端找出最拖時間的腳本
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：以 `PerformanceObserver` 觀察 `long-animation-frame`（`buffered: true`），累積每個條目的 `scripts`，依 `sourceURL` 分組加總 `duration`，排出最重的腳本（含第三方聊天、影片、分析腳本）並送到分析服務
- 被什麼擋：實驗室資料只重現一小部分真實使用情境，與實地資料差很多，讓效能差、尤其互動慢的根因很難找到；改用 JS Self-Profiling API 則執行負擔較高（引用："field data is often very different to lab data, which only replicates a small subset of real user scenarios."）
- 戰報：部分改善——輕量的 API 就能在實地資料裡點名拖慢畫面的腳本，包括單次很長或多次累積的；只有 Chrome／Edge 支援，但不支援的瀏覽器會忽略它，指南稱找出的問題多半也適用其他瀏覽器（官方宣稱）

經過：頁面在使用者手上卡，開發機上跑卻很順，profile 也抓不到。LoAF 讓每一個超過 50ms 的影格自己報出是哪些腳本、各跑了多久，在正式環境就能知道是哪個第三方在拖。
%% line-end %%

### 細節（不索引）
- 對手組：效能量測失真或有盲點
- 支援狀態：Long animation frames performance entries：Limited availability。Supported by: Chrome 123, Edge 123；Unsupported in: Firefox, Safari
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：可以做一個「第三方腳本帳單」面板：每個外部腳本在真實使用者端總共吃掉多少主執行緒時間，拿來決定要不要換掉某個聊天外掛或廣告 SDK。資料只來自 Chromium 使用者
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出
