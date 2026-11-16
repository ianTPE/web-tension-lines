---
guide: capture-location-agnostic-data
category: js
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/js/capture-location-agnostic-data.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 用 Temporal 記錄與地點無關的資料和不完整日期

%% line-start id="mwg:capture-location-agnostic-data" %%
## 生日、鬧鐘這類日期用 Temporal.PlainDate／PlainTime，擋掉跨時區少一天
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：純日期用 `Temporal.PlainDate.from()`、牆上時間用 `PlainTime`、兩者合起來用 `PlainDateTime`，直接讀 `.year`、`.month`、`.day`，比較用 `.equals()`；非得交給 `Date` 時經由 `Temporal.Instant` 明確指定時區
- 被什麼擋：`Date` 永遠代表一個瞬間並以觀看者的時區顯示，存成 `Date` 的「1990-01-01」在 UTC 以西的使用者看來是「1989-12-31」（引用："saving a date like `"1990-01-01"` can result in users west of UTC seeing `"1989-12-31"`"）
- 戰報：部分改善——Plain 類型不帶時區，在任何地方顯示都是同一天；Safari 尚未支援，需條件載入 polyfill（官方宣稱）

經過：使用者在台北填了生日，紐約的客服後台看到的是前一天。不是資料錯，而是 `Date` 本來就沒有「日曆上的某一天」這種概念。`PlainDate` 就是那一天本身，不需要選一個午夜時刻去代表它。
%% line-end %%

### 細節（不索引）
- 對手組：時間模型失真
- 支援狀態：Temporal：Limited availability。Supported by: Chrome 144, Edge 144, Firefox 139；Unsupported in: Safari
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：生日提醒、每天 9 點的鬧鐘、店家營業時間可以存成「與地點無關」的值，跨時區的使用者、伺服器、同步裝置看到的都是同一天同一刻。Safari 要 polyfill
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:capture-location-agnostic-data:2" %%
## 信用卡到期、年度紀念日用 PlainYearMonth／PlainMonthDay，不要塞假的日
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：年月用 `Temporal.PlainYearMonth`、月日用 `Temporal.PlainMonthDay`（物件建構時明確給 `calendar: 'iso8601'`）；要做運算時先 `.toPlainDate({ year })`；每月循環用 `.add({ months: 1 })` 搭配 `overflow: 'constrain'` 或 `'reject'`
- 被什麼擋：用 `Date` 表示只有月份的卡片到期日，得塞一個隨意的日子，造成溢位錯誤（引用："modeling partial dates (like a month-only card expiry) forces arbitrary placeholder days that cause overflow bugs."）
- 戰報：部分改善——沒有「日」的型別讓假日子不會滲進計算，月底加一個月時可選擇夾到月底或丟錯；Safari 需 polyfill（官方宣稱）

經過：卡片到期「2027-12」存成 12 月 31 日，或每月 31 號扣款，一到 2 月就溢到 3 月。`PlainYearMonth` 根本沒有日欄位，`overflow` 則把「1 月 31 日加一個月」的行為變成明確的選擇。
%% line-end %%

### 細節（不索引）
- 對手組：時間模型失真
- 支援狀態：Temporal：Limited availability（同上）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：訂閱扣款日、每年的紀念日提醒、帳單月份這類「不完整日期」可以照字面存與比較，月底扣款的規則（夾到月底或拒絕）寫成一個參數。Safari 要 polyfill
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:capture-location-agnostic-data:3" %%
## 時區用 IANA 名稱，不要用固定的 UTC 偏移
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：時區一律用 `America/New_York` 這類 IANA 名稱識別
- 被什麼擋：偏移會隨日光節約與法規改變，「UTC-5」這種標籤一年中有一段時間是錯的（引用："Offsets change with daylight saving time and legislation, so labels like `"UTC-5"` become wrong for part of the year."）
- 戰報：部分改善——IANA 名稱讓日光節約與法規變動自動套用；本指南的 Temporal 在 Safari 需 polyfill（官方宣稱）

經過：把紐約存成 UTC-5，夏天整整差一小時。用地名識別時區，偏移由時區資料庫決定。
%% line-end %%

### 細節（不索引）
- 對手組：時間模型失真
- 支援狀態：Temporal：Limited availability（同上）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

另有 2 個糾錯提醒未拆：不要用 `formatToParts()` 取出年月日；不要從手拼的 ISO 字串建立 `Date`。
