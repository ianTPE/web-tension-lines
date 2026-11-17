---
guide: defer-work-until-scroll-ends
category: performance
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/performance/defer-work-until-scroll-ends.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 等捲動結束再做事

%% line-start id="mwg:defer-work-until-scroll-ends" %%
## 用 scrollend 取代 debounce 猜「捲完了沒」
- 做法：在捲動容器或 document 上監聽 `scrollend`，把抓新內容、版面重算、分析 beacon 放進這個回呼
- 對手：用 `setTimeout` 對 `scroll` 做 debounce 來猜捲動何時結束，不可靠，可能在使用者還在捲的時候就觸發（引用："However, these debounced functions are notoriously unreliable. They may trigger while the user’s is still scrolling."）
- 退路：失去主要好處——不支援時退回 `scroll` 加 `setTimeout` 派發自訂事件，仍會因猜測而提前觸發
- 解鎖：監聽 `scrollend` 在捲動、轉場與手勢真正停妥時精準觸發回呼，不必再用計時器猜時機

經過：手指還按在螢幕上慢慢拖、或慣性捲動還沒停，debounce 的 100ms 就到了，抓資料、重算版面在捲動中途開跑。`scrollend` 由瀏覽器判定真正的結束點，不用再猜等待時間。
%% line-end %%

### 細節（不索引）
- 對手組：完成時機靠猜
- 支援狀態：scrollend：Newly available（2025-12-12）。Supported by: Chrome 114, Edge 114, Firefox 109, Safari 26.2
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：「捲到哪一章就記住閱讀位置」「停在哪張圖就載高解析版」可以在使用者真的停下時才做一次，不會在慣性捲動中途被觸發好幾次
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:defer-work-until-scroll-ends:2" %%
## 重活不要放在 scroll 回呼裡
- 做法：`scroll` 回呼只做輕量的即時回饋，版面相依的更新與資料抓取移到 `scrollend`
- 對手：捲動期間執行版面重算、分析 beacon、動態 DOM 更新，會塞滿主執行緒，造成掉幀與版面抖動（引用："Executing heavy tasks—such as layout recalculations, analytics data beacons tracking, or dynamic DOM updates—during scrolling can saturate the main thread, resulting in dropped frames and layout thrashing."）
- 退路：失去主要好處——退回 debounce 猜捲動結束，重活仍可能落在捲動途中
- 解鎖：（缺）

經過：每個 `scroll` 事件都去量版面、送 beacon，捲動變得一頓一頓。把這些搬到捲動結束之後，捲動本身就保持順暢。
%% line-end %%

### 細節（不索引）
- 對手組：主執行緒被重活卡住
- 支援狀態：scrollend：Newly available（同上）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 交叉核對仲裁：退路改為「失去主要好處」
