---
guide: calculate-event-differentials
category: js
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/js/calculate-event-differentials.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 用 Temporal 計算事件時間差並格式化時長

%% line-start id="mwg:calculate-event-differentials" %%
## 用 ZonedDateTime 的 since()／until() 算時間差，不用 Date 毫秒相減
- 做法：兩端點都做成 `Temporal.ZonedDateTime`（指定 IANA 時區），用 `.since()`／`.until()` 搭配 `largestUnit`、`smallestUnit` 算出 `Temporal.Duration`；比較時長用 `Temporal.Duration.compare(d1, d2, { relativeTo })`，到期與否看 `.sign`
- 對手：缺——指南只說舊 `Date` 只記毫秒，讓跨月計算、日光節約轉換與單位進位「容易出錯」，以前得靠手算或外部函式庫，沒指出哪個具體情境算錯（引用："The legacy `Date` object only tracks epoch milliseconds, making calendar-month arithmetic, Daylight Saving Time (DST) transitions, and unit balancing error-prone."）
- 退路：保住主要行為——Safari 沒有原生 API 時動態載入 temporal-polyfill，時間差照樣算得出來
- 解鎖：以前算跨月與日光節約的時間差要手算或載 date-fns；現在用 Temporal 的時區感知運算，差值直接以曆法單位算

經過：試用剩幾天、訂閱何時到期、SLA 還剩多久，用毫秒相減再除以 86400000，遇到日光節約或大小月就差一點。`ZonedDateTime` 讓差值以曆法單位計算並依需求進位。注意預設 `largestUnit` 是 hour，要人看的拆解得自己指定 day 或 month。
%% line-end %%

### 細節（不索引）
- 對手組：時間模型失真
- 支援狀態：Temporal：Limited availability。Supported by: Chrome 144, Edge 144, Firefox 139；Unsupported in: Safari
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：倒數、試用剩餘、「距離上次 X 已經 3 個月又 2 天」這類以曆法單位顯示的時間差可以直接算，不必載 moment／date-fns。Safari 要 polyfill
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:calculate-event-differentials:2" %%
## 用 Intl.DurationFormat 輸出在地化時長，不要手拼單位字串
- 做法：`duration.toLocaleString(locale, { style })` 或 `new Intl.DurationFormat(locale, { style: 'long' | 'short' | 'narrow' | 'digital' })`；`toString()` 只用在 ISO 8601 機器格式
- 對手：缺——指南只說不要手動內插 `${duration.years}y ${duration.months}m...`，沒說手拼版在哪個時刻出錯
- 退路：沒說——指南只給 Temporal 的 polyfill 退路，沒有交代 `Intl.DurationFormat` 不支援時怎麼辦
- 解鎖：以前顯示時長要自己拼單位字串，換語系就得重寫；現在單位、順序與分隔符交給語系資料處理

經過：時長要顯示給人看，常見的是自己拼「1h 30m」，換語系就整串要重寫。`Intl.DurationFormat` 把單位、順序、分隔符交給語系資料處理。
%% line-end %%

### 細節（不索引）
- 對手組：時間模型失真
- 支援狀態：Intl.DurationFormat：Newly（2025-03-04）。Supported by: Chrome 129, Edge 129, Firefox 136, Safari 16.4
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：多語系介面的「已用時間」「預計剩餘」「影片長度」可以一行輸出各語言正確的時長文字，連「1:30:00」這種數位樣式也有
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

另有 2 個糾錯提醒未拆：日期與時間字串用 Temporal 方法組合，不要內插成 ISO 字串；`PlainTime` 輸出 `HH:MM` 用 `toString({ smallestUnit: 'minute' })` 而非 `.slice(0, 5)`。
