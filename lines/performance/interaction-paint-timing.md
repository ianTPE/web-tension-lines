---
guide: interaction-paint-timing
category: performance
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/performance/interaction-paint-timing.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 量測互動與軟導覽的繪製時間

%% line-start id="mwg:interaction-paint-timing" %%
## 用 interaction-contentful-paint 與 soft-navigation 量到互動之後非同步出現的內容
- 做法：以 `PerformanceObserver` 觀察 `interaction-contentful-paint` 與 `soft-navigation`（`buffered: true`），把 fetch 之後才畫出的內容、SPA 換路由後的 LCP 歸回觸發它的那次互動；或用 `web-vitals` v6 的 `{ reportSoftNavs: true }`
- 對手：LCP 在使用者第一次互動後就停止；INP 只量到下一個影格，`fetch()` 完成後才渲染的內容與 SPA 路由切換都量不到；只監看網址變化又會多報不是換路由的變化（引用："Just monitoring URL updates can over report URL changes that are not linked to route changes (for example, anchor link changes, multiple "redirects" for a single route change)."）
- 退路：失去主要好處——Firefox 與 Safari 僅保留傳統硬導覽指標，量不到互動後繪製與軟導覽 LCP
- 解鎖：用 `interaction-contentful-paint` 與 `soft-navigation` 量測非同步互動繪製與 SPA 換頁 LCP

經過：使用者按「搜尋」，按鈕馬上變色（INP 很好看），結果三秒後才出現。SPA 換頁更是完全沒有 LCP。新的條目跨越 `fetch`、`await`、`setTimeout` 追蹤因果，量的是從點下去到內容真的出現。目前只有 Chromium。
%% line-end %%

### 細節（不索引）
- 對手組：效能量測失真或有盲點
- 支援狀態：Interaction contentful paint performance entries：Limited availability（Chrome 151, Edge 151；Unsupported in: Firefox, Safari）；Soft navigation performance entries：同上
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：SPA 可以有每條路由各自的 LCP 排行，或量「按下搜尋到結果出現」的真實等待時間，拿來找出最慢的換頁與最慢的 API 回應。目前僅 Chromium
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:interaction-paint-timing:2" %%
## 軟導覽的繪製要用 interactionId 配對，時間要用 duration
- 做法：收到 `soft-navigation` 時先呼叫 `getLargestInteractionContentfulPaint()` 當初始 LCP；之後的 `interaction-contentful-paint` 用 `interactionId` 配對，不用 `navigationId`；回報時用 `entry.duration`，不直接報 `presentationTime`
- 對手：先渲染再 `history.pushState()` 的 app，早期的繪製條目帶的是前一個 `navigationId`，用它配對會漏掉；所有時間戳都從最初硬導覽的時間原點起算，不是從軟導覽開始（引用："If the application painted content *before* updating the URL (for example, rendering a view and then calling `history.pushState()`), those early `interaction-contentful-paint` entries were emitted before the `soft-navigation` entry and still carry the *previous* `navigationId`."）
- 退路：保住主要行為——Firefox 與 Safari 依功能偵測跳過註冊觀察器，不會錯配或報出錯誤時間
- 解鎖：（缺）

經過：直覺是「同一個 navigationId 就是同一頁」，但框架常先畫畫面再改網址，最重要的那次繪製反而掛在上一頁名下。直接報 `presentationTime` 則會得到從整個 app 開啟起算的數字。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：同上（Limited，僅 Chrome／Edge 151）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:interaction-paint-timing:3" %%
## 長時間開著的 SPA 不能靠 getEntriesByType('soft-navigation')
- 做法：用 `PerformanceObserver` 持續接收 `soft-navigation` 條目，不靠事後查詢 `performance.getEntriesByType('soft-navigation')`
- 對手：瀏覽器的緩衝區只保留前 50 筆軟導覽條目（引用："DO NOT rely on `performance.getEntriesByType('soft-navigation')` to monitor long-lived single-page applications, as the browser's buffer is limited to the first 50 soft navigation entries."）
- 退路：保住主要行為——Firefox 與 Safari 依功能偵測跳過觀察器，不受 50 筆緩衝限制影響
- 解鎖：（缺）

經過：後台、信箱這類一開就是一整天的 SPA，換頁很快超過 50 次。事後去查時間軸，之後的換頁全部不見，而且沒有任何錯誤提示。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：同上（Limited，僅 Chrome／Edge 151）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
