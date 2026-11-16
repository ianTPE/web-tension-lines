---
guide: sort-high-precision-timestamps
category: js
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/js/sort-high-precision-timestamps.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 用 Temporal.Instant 排序高精度時間戳

%% line-start id="mwg:sort-high-precision-timestamps" %%
## 用 Temporal.Instant 解析奈秒時間戳，擋掉同一毫秒內的事件排序錯亂
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：伺服器或日誌給的 ISO 8601 時間戳用 `Temporal.Instant.from()` 解析，`Temporal.Instant.compare()` 當排序比較函式，`.since()` 算間隔、`.equals()` 判斷相同
- 被什麼擋：`Date` 只存毫秒，`new Date()`／`Date.parse()` 會默默截掉毫秒以下的位數，同一毫秒內的不同事件撞在一起、排序不穩定（引用："parsing those strings with `new Date()` or `Date.parse()` silently truncates sub-millisecond digits, causing distinct events within the same millisecond to collide and sort in an unstable order."）
- 戰報：部分改善——`Instant` 保留完整奈秒值，排序確定、間隔精確；Safari 需 polyfill。瀏覽器自己的 `Temporal.Now.instant()` 仍被刻意降低解析度（官方宣稱）

經過：分散式追蹤的三筆事件都在 12:00:00.000 這一毫秒內，用 `Date` 解析後時間完全相同，畫出來的順序每次都可能不一樣。`Instant` 保住後面的六位數，request.start、db.query、request.end 永遠按真實順序排。
%% line-end %%

### 細節（不索引）
- 對手組：時間模型失真
- 支援狀態：Temporal：Limited availability。Supported by: Chrome 144, Edge 144, Firefox 139；Unsupported in: Safari
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：在瀏覽器裡做的日誌檢視器、追蹤時間軸、遙測面板可以照伺服器記錄的奈秒精度排序並顯示「3μs 456ns」這種間隔，不用把時間戳當字串比。Safari 要 polyfill
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:sort-high-precision-timestamps:2" %%
## 間隔保持 Temporal.Duration 再格式化，不要轉成奈秒數字
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：間隔維持 `Temporal.Duration`，用 `toLocaleString()` 顯示；不用 `duration.total('nanoseconds')` 轉成單一數字
- 被什麼擋：`total('nanoseconds')` 回傳 `Number`，超過約 104 天的間隔就超出 `Number.MAX_SAFE_INTEGER`，默默失去精度（引用："`duration.total('nanoseconds')` returns a `Number`, which exceeds `Number.MAX_SAFE_INTEGER` for spans longer than ~104 days and silently loses precision."）
- 戰報：部分改善——保持 Duration 型別，精度與單位結構都在；Safari 需 polyfill（官方宣稱）

經過：奈秒時間戳費心保住了，最後為了顯示轉成一個大數字，長區間的尾數就悄悄錯了。相減 `epochNanoseconds`（BigInt）雖然精確，卻丟了單位結構，直接格式化 Duration 最省事。
%% line-end %%

### 細節（不索引）
- 對手組：時間模型失真
- 支援狀態：Temporal：Limited availability（同上）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

另有 1 個糾錯提醒未拆：判斷相等用 `.equals()`，不要比 `compare() === 0` 或 `toString()`。
