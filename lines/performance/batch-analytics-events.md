---
guide: batch-analytics-events
category: performance
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/performance/batch-analytics-events.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 防抖並批次送出分析事件

%% line-start id="mwg:batch-analytics-events" %%
## 用 fetchLater() 的 activateAfter 把一段時間內的事件併成一個 beacon
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：有分析資料就呼叫 `fetchLater(url, { body, activateAfter, signal })`；時間窗內又有新事件時，以 `AbortController` 取消前一個請求、帶著整個佇列重新排程；`result.activated` 為真時清空佇列
- 被什麼擋：缺——指南說這是在即時更新與減少 beacon 之間的最佳做法，且使用者在逾時前離開也能可靠送出，但沒說舊做法在哪個時刻出問題
- 戰報：部分改善——支援的瀏覽器把時間窗內的事件併成一次送出，離開頁面時由瀏覽器保證送出；Firefox 與 Safari 不支援，改用 polyfill，差別是改在 `visibilityState` 變成 hidden 時送（官方宣稱）

經過：每個點擊都打一次 beacon 太多，全部攢到離開頁面才送又不即時，還可能在關分頁時遺失。`fetchLater()` 把「10 秒內沒新事件就送，或使用者先離開就立刻送」交給瀏覽器排程。目前只有 Chromium 原生支援。
%% line-end %%

### 細節（不索引）
- 對手組：背景送出不可靠或過量
- 支援狀態：fetchLater：Limited availability。Supported by: Chrome 135, Edge 135；Unsupported in: Firefox, Safari
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：自架的輕量分析、編輯器的自動草稿、閱讀進度同步，都能「攢一小段再送、關分頁也不掉」，不必自己拼 visibilitychange 加 sendBeacon。目前僅 Chromium，其他靠 polyfill
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:batch-analytics-events:2" %%
## fetchLater() 有配額，要限制批次大小並包 try/catch
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：設定佇列上限（例如 100 筆）以免超過每個來源約 64KB 的配額，呼叫包在 `try/catch` 裡；body 不用 `ReadableStream`
- 被什麼擋：批次太大會超出 `fetchLater()` 的配額而丟出錯誤；用 `ReadableStream` 當 body 也會出錯（引用："DO check to ensure you do not batch too many events together and exceed the `fetchLater()` quota (currently roughly 64KB per origin)."）
- 戰報：部分改善——限制大小並捕捉錯誤後，排程不會因配額而中斷；整體仍受 fetchLater 的支援度限制（官方宣稱）

經過：佇列無限累積，某次重新排程時超過配額直接拋錯，後面的事件再也沒排上。加上上限與 try/catch，最壞情況是重置佇列而不是整條管線停擺。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：fetchLater：Limited availability（同上）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出
