---
guide: scroll-snap-realtime-feedback
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/scroll-snap-realtime-feedback.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 捲動吸附的即時回饋

%% line-start id="mwg:scroll-snap-realtime-feedback" %%
## 用 `scrollsnapchanging` 在手指還沒放開時就標出即將吸附的項目
- 做法：在捲動容器上聽 `scrollsnapchanging`，用 `event.snapTargetInline`（或 `snapTargetBlock`）替對應縮圖加 `pending` 樣式；再聽 `scrollsnapchange` 在真正吸附後設成 `active` 並更新 `aria-current`
- 對手：傳統的捲動吸附只在手勢結束、元素停穩之後才有回饋（引用："Traditional scroll snap only provides feedback *after* the scroll gesture completes and the element settles."）
- 退路：保住主要行為——偵測不支援時改用 scroll 加 rAF 與距離計算模擬即時預告，搭 scrollend 與防抖定案
- 解鎖：捲動手勢還沒放開前就能由原生事件即時預告即將吸附的項目，不必等滑完停穩才同步介面

經過：相簿往左滑，下方縮圖列要等滑完、停穩才換高亮，手指還在動時看不出會停在哪張。原生事件能提前告知「快要停在這張」，但目前只有 Chromium 給。
%% line-end %%

### 細節（不索引）
- 對手組：回饋落後於手勢（新開，見下）
- 支援狀態：Scroll snap events：Limited availability，Supported by: Chrome 129, Edge 129；Unsupported in: Firefox, Safari（Scroll snap 本身為 Widely）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前吸附的回饋只能等停穩 → 現在轉盤式選擇器（日期、時間、數量）、相簿縮圖列可以在拖動中就預告結果，像實體轉盤一樣邊轉邊亮。目前僅 Chromium
- 新開對手組理由：既有組「捲動連動效果靠JS監聽」講的是用 JS 取代 CSS 效果，「完成時機靠猜」講的是不知道何時結束；這條的對手是「回饋只在結束後才來」，形狀不同
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:scroll-snap-realtime-feedback:2" %%
## 載入時捲動位置被還原，要自己同步一次初始狀態
- 做法：頁面載入（`load` 或 `readyState === 'complete'`）時跑一次幾何計算，找出最接近中心的項目並設成 active
- 對手：瀏覽器透過歷史紀錄或錨點還原捲動位置時，`scrollsnapchange` 與 `scroll` 都不會自動觸發（引用："Neither `scrollsnapchange` nor `scroll` events will fire automatically."）
- 退路：保住主要行為——載入時的一次性幾何計算不依賴吸附事件，原生環境與 scroll 退路皆能同步初始狀態
- 解鎖：（缺）

經過：按上一頁回到相簿，畫面停在第五張，縮圖列卻還亮著第一張。
%% line-end %%

### 細節（不索引）
- 對手組：生命週期假設錯
- 支援狀態：Scroll snap events：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 3 個糾錯提醒未拆：控制鈕的 `aria-current` 要和內容同步；控制鈕組用 `focusgroup="toolbar wrap"`（同 `mwg:toolbar:2`）；捲動容器要可聚焦並有名稱與角色
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
