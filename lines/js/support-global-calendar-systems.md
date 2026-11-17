---
guide: support-global-calendar-systems
category: js
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/js/support-global-calendar-systems.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 用 Temporal 支援各地曆法

%% line-start id="mwg:support-global-calendar-systems" %%
## 用 withCalendar() 讓日期直接以希伯來曆、伊斯蘭曆、農曆運算
- 做法：先用 `Intl.supportedValuesOf('calendar')` 確認環境支援，再以 `plainDate.withCalendar('hebrew')` 等轉換，依該曆法比較（`Temporal.PlainDate.compare()`）並用 `toLocaleString('en-u-ca-hebrew', { era: 'long', … })` 顯示
- 對手：缺——指南只說 `Date` 以預推格里曆為基礎，支援其他曆法「很有挑戰」，以前得靠複雜的第三方函式庫或手算，沒指出哪個具體情境出錯（引用："Developers previously had to rely on complex third-party libraries or manual calculations to support these systems."）
- 退路：保住主要行為——Safari 沒有原生 API 時動態載入 temporal-polyfill，曆法換算照樣做得到
- 解鎖：以前要支援希伯來曆或農曆得載第三方曆法函式庫；現在日期帶著曆法識別碼，加減比較都依那套曆法

經過：要替使用者顯示希伯來曆或農曆日期，過去得載一套曆法函式庫。Temporal 讓日期帶著曆法識別碼，加減、比較、格式化都依那個曆法進行。
%% line-end %%

### 細節（不索引）
- 對手組：得送雲端或載大型函式庫
- 支援狀態：Temporal：Limited availability。Supported by: Chrome 144, Edge 144, Firefox 139；Unsupported in: Safari
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：行事曆或節日提醒可以讓使用者選自己的曆法，農曆生日、猶太節日每年自動換算到正確的公曆日期，不必內建曆法表。Safari 要 polyfill
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:support-global-calendar-systems:2" %%
## 用 monthsInYear、monthCode，不要假設一年 12 個月
- 做法：迴圈上限用 `monthsInYear`、每月天數用 `daysInMonth`；跨年識別同一個月用 `monthCode`；判斷最後一個月用 `date.month === date.monthsInYear`
- 對手：在陰陽合曆裡，閏年可能多出一整個閏月，不只多一天；寫死 12 個月或用數字月份跨年比對就會錯（引用："DO NOT assume `inLeapYear === true` implies the year is only one day longer. In lunisolar calendars, it may add a full leap month."）
- 退路：保住主要行為——polyfill 同樣提供 `monthsInYear` 與 `monthCode`，閏月照樣算得出來
- 解鎖：（缺）

經過：月曆元件寫死 12 格，換成希伯來曆的閏年就少畫一個月；用 `month === 6` 找某個節日，閏月一插進來就指到錯的月。`monthCode` 是跨年穩定的月份名稱。
%% line-end %%

### 細節（不索引）
- 對手組：時間模型失真
- 支援狀態：Temporal：Limited availability（同上）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

另有 1 個糾錯提醒未拆：使用年號的曆法（日本、佛曆）用 `toLocaleString()` 顯示年號。
