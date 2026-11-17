---
guide: scroll-entry-exit-effects
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/scroll-entry-exit-effects.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 元素進出捲動視窗的效果

%% line-start id="mwg:scroll-entry-exit-effects" %%
## 用 `view()` 加 `animation-range: entry, exit` 做進場與離場效果
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：進場與離場各寫一組 `@keyframes`（進場 fill `backwards`、離場 `forwards`），用 `animation-timeline: view()` 綁到元素自身的可見度，再以 `animation-range: entry, exit` 限定區段；也可在單一 `@keyframes` 裡用 `entry 0%`、`exit 100%` 這類範圍選擇器
- 被什麼擋：指南沒說舊做法哪裡壞，只說不支援時退路是 IntersectionObserver，而原生實作效能較好（引用："In browsers with built-in support for scroll-driven animations, ALWAYS use the native CSS implementation as those are more performant."）
- 戰報：部分改善——純 CSS 依捲動位置驅動進出場；Scroll-driven animations 為 Newly，裝飾性效果可不給退路（官方宣稱）

經過：卡片滑進畫面時長大、滑出時縮小，以前要每個元素掛觀察器、算交集比例。現在一組 keyframes 綁在 view timeline 上，捲多少動多少。
%% line-end %%

### 細節（不索引）
- 對手組：捲動連動效果靠JS監聽
- 支援狀態：Scroll-driven animations：Baseline Newly available（2026-10-27 起）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前進出場效果要 IntersectionObserver 逐一算比例 → 現在水平相簿、時間軸、商品列可以讓每一項在進出視窗時縮放、淡入淡出，捲動倒退也自動倒帶
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:scroll-entry-exit-effects:2" %%
## `@supports` 要同時檢查 `animation-range: entry`
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：偵測寫成 `@supports ((animation-timeline: view()) and (animation-range: entry))`
- 被什麼擋：只偵測 `animation-timeline` 會放行只有部分支援的瀏覽器（引用："The `(animation-range: entry)` check **MUST** be included here, to filter out browsers with only partial support."）
- 戰報：部分改善——部分支援的瀏覽器被濾掉，走退路或不做效果（官方宣稱）

經過：偵測通過了，效果卻在某些瀏覽器跑在錯的區段。
%% line-end %%

### 細節（不索引）
- 對手組：功能偵測不可靠
- 支援狀態：Scroll-driven animations：Newly
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:scroll-entry-exit-effects:3" %%
## `animation-timeline` 與 `animation-range` 寫在 `animation` 簡寫之後
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：先寫 `animation` 簡寫，再寫 `animation-timeline`、`animation-range`
- 被什麼擋：簡寫寫在後面會把時間軸與區段重設掉（引用："declare `animation-timeline` and `animation-range` *after* it to prevent the shorthand from resetting them."）
- 戰報：部分改善——順序正確時時間軸與區段保留（官方宣稱）

經過：動畫在頁面載入時自己跑完一次，跟捲動毫無關係。
%% line-end %%

### 細節（不索引）
- 對手組：簡寫或屬性連動重設
- 支援狀態：Scroll-driven animations：Newly
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:scroll-entry-exit-effects:4" %%
## 單一 keyframes 寫進出場時，要明寫中段的靜止狀態
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：用 `entry 100%, exit 0%` 一起設定靜止值（例如 `scale: 1`），搭配 `animation-fill-mode: both`
- 被什麼擋：沒寫中段的話，元素會從 `entry 0%` 一路內插到 `exit 100%`（引用："Explicitly set the resting state across the middle (`contain`) phase so the element doesn't interpolate straight from entry 0% to exit 100%"）
- 戰報：部分改善——完整在畫面內時保持原尺寸（官方宣稱）

經過：卡片一進畫面就開始慢慢縮，完全沒有「停在正常大小」的那段。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：Scroll-driven animations：Newly
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 另有 1 個糾錯提醒未拆：不要用 `scroll-timeline-polyfill` 當退路（不完整、已知問題多）
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
