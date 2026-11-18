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
- 做法：有分析資料就呼叫 `fetchLater(url, { body, activateAfter, signal })`；時間窗內又有新事件時，以 `AbortController` 取消前一個請求、帶著整個佇列重新排程；`result.activated` 為真時清空佇列
- 對手：缺——指南說這是在即時更新與減少 beacon 之間的最佳做法，且使用者在逾時前離開也能可靠送出，但沒說舊做法在哪個時刻出問題
- 退路：保住主要行為——退回 `visibilitychange` 搭 `keepalive`／`sendBeacon` 仍可防抖批次送出，改在頁面隱藏時送
- 解鎖：用 `fetchLater()` 的 `activateAfter` 讓瀏覽器把時間窗內的事件併成一筆送出，離開頁面也不掉

經過：每個點擊都打一次 beacon 太多，全部攢到離開頁面才送又不即時，還可能在關分頁時遺失。`fetchLater()` 把「10 秒內沒新事件就送，或使用者先離開就立刻送」交給瀏覽器排程。目前只有 Chromium 原生支援。
%% line-end %%

### 細節（不索引）
- 對手組：背景送出不可靠或過量
- 支援狀態：fetchLater：Limited availability。Supported by: Chrome 135, Edge 135；Unsupported in: Firefox, Safari
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：自架的輕量分析、編輯器的自動草稿、閱讀進度同步，都能「攢一小段再送、關分頁也不掉」，不必自己拼 visibilitychange 加 sendBeacon。目前僅 Chromium，其他靠 polyfill
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:batch-analytics-events:2" %%
## fetchLater() 有配額，要限制批次大小並包 try/catch
- 做法：設定佇列上限（例如 100 筆）以免超過每個來源約 64KB 的配額，呼叫包在 `try/catch` 裡；body 不用 `ReadableStream`
- 對手：批次太大會超出 `fetchLater()` 的配額而丟出錯誤；用 `ReadableStream` 當 body 也會出錯（引用："DO check to ensure you do not batch too many events together and exceed the `fetchLater()` quota (currently roughly 64KB per origin)."）
- 退路：保住主要行為——退回 `visibilitychange` 搭 `keepalive`／`sendBeacon` 仍適用佇列上限與錯誤保護
- 解鎖：（缺）

經過：佇列無限累積，某次重新排程時超過配額直接拋錯，後面的事件再也沒排上。加上上限與 try/catch，最壞情況是重置佇列而不是整條管線停擺。
%% line-end %%

### 細節（不索引）
- 對手組：參數或格式用錯就丟例外
- 支援狀態：fetchLater：Limited availability（同上）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 對手組由「新功能的副作用」改為「參數或格式用錯就丟例外」
