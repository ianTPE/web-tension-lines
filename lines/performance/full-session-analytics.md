---
guide: full-session-analytics
category: performance
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/performance/full-session-analytics.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 可靠地量測整段造訪的分析與遙測

%% line-start id="mwg:full-session-analytics" %%
## 用 fetchLater() 取代 unload 裡的追蹤像素，整段造訪的資料離開時由瀏覽器送出
- 做法：資料一有就呼叫 `fetchLater()` 排程；狀態更新時用 `AbortController` 取消前一個，再以完整的最新快照重新排程；離開或關分頁時由瀏覽器送出最後一次排程的內容；不支援時用指南附的 polyfill（內部用 `fetch` keepalive 或 `sendBeacon()`）
- 對手：在 `unload` 監聽器裡建立 `<img>` 像素的舊技巧極不可靠（行動裝置尤其），還會讓頁面失去 bfcache 資格（引用："Older technique like creating an `<img>` pixel in an `unload` event listener are notoriously unreliably (especially on mobile) and can negatively impact performance (by making pages ineligible for bfcache)."）
- 退路：保住主要行為——Firefox 與 Safari 退回 `visibilitychange` 搭 `keepalive`／`sendBeacon`，仍能送出且不傷 bfcache
- 解鎖：用 `fetchLater()` 一路更新造訪快照，由瀏覽器在離開頁面時可靠送出且不傷 bfcache

經過：停留時長、整段 CWV、錯誤紀錄要等到最後才知道，舊做法是在 unload 時硬送，手機上常常根本沒送出，還拖累上一頁／下一頁的快取。`fetchLater()` 讓頁面一路更新「離開時要送的東西」，送的時機交給瀏覽器。
%% line-end %%

### 細節（不索引）
- 對手組：背景送出不可靠或過量
- 支援狀態：fetchLater：Limited availability。Supported by: Chrome 135, Edge 135；Unsupported in: Firefox, Safari
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：長文閱讀頁可以一路更新「讀到第幾段、停了多久」，關掉分頁時最後的狀態照樣送達，又不會讓頁面失去 bfcache。Chromium 原生，其他靠 polyfill
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:full-session-analytics:2" %%
## fetchLater() 有每來源約 64KB 的配額，要縮小 payload 並包 try/catch
- 做法：把 payload 縮到最小，`fetchLater()` 呼叫包在 `try/catch` 裡處理配額錯誤；body 不用 `ReadableStream`
- 對手：超過配額時 `fetchLater()` 會丟錯；用 `ReadableStream` 當 body 也會出錯（引用："DO NOT use a `ReadableStream` object for the request body, as that will error."）
- 退路：保住主要行為——退回 `visibilitychange` 搭 `keepalive`／`sendBeacon` 仍適用縮小 payload 與錯誤捕捉
- 解鎖：（缺）

經過：每 10 秒重排一次的 beacon 帶著整段資料，資料越堆越大，某次超過配額就在 `fetchLater()` 呼叫處拋錯。指南要求事先縮小 payload，並把錯誤接住自行處理。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：fetchLater：Limited availability（同上）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另見 mwg:batch-analytics-events:2（同一個配額對手）
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
