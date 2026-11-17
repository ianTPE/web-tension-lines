---
guide: visual-effects
category: visual-design
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/visual-design/visual-effects.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 視覺效果

%% line-start id="mwg:visual-effects" %%
## 漸層與 `color-mix()` 明確寫 `in oklch` 或 `in oklab` 指定插值色彩空間
- 做法：漸層與 `color-mix()` 加上 `in oklch`（保住彩度，但色差大時較容易超出裝置色域）或 `in oklab`（端點在色域內時較容易留在色域內，但對色相時中段可能褪成灰）；除非有特定理由（例如做 sRGB 取色器），不用 `in srgb`
- 對手：缺——指南只說不要用 `in srgb`，沒說 sRGB 插值在哪個時刻出問題
- 退路：不需要——支援狀態不適用，部分舊瀏覽器可搭配條件變數退回預設插值
- 解鎖：用 `in oklch` 或 `in oklab` 指定漸層與 `color-mix()` 插值色彩空間，依需求保彩度或保色域

經過：品牌的藍到橘漸層，要在「中段鮮豔」和「不超出色域」之間取捨。寫明插值空間後，取捨變成一個關鍵字的選擇。
%% line-end %%

### 細節（不索引）
- 對手組：主題配色對不上
- 支援狀態：指南沒有 Baseline 資料，只說部分 2024 年以前的瀏覽器不支援漸層的插值色彩空間；不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前漸層只能接受瀏覽器預設的混色方式 → 現在品牌雙色漸層、資料視覺化的連續色階、`color-mix()` 產生的 hover 色都能指定在哪個色彩空間混，依畫面選保彩度或保色域
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:visual-effects:2" %%
## 用 `@supports` 設定的自訂屬性帶入插值空間，並保留非空的漸層前導
- 做法：`:root` 先把 `--in-oklab`、`--in-oklch` 設成空值，`@supports (linear-gradient(in oklab, white, black))` 成立時才填入 `in oklab`／`in oklch`，用成 `linear-gradient(to bottom var(--in-oklab), …)`；變數之外一定要有方向之類的非空前導；`color-mix()` 不需要這招
- 對手：部分 2024 年以前的瀏覽器不支援漸層插值色彩空間；變數為空時若沒有其他前導，舊瀏覽器直接判為語法錯誤（引用："make sure there is always a non-empty gradient preamble without it, otherwise it will be a syntax error in older browsers."）
- 退路：不需要——支援狀態不適用，不必另設退路
- 解鎖：（缺）

經過：卡片背景寫了 `in oklab`，在舊版瀏覽器整條 `background` 失效、卡片變透明。改成條件填入的變數並保留 `to bottom` 前導後，舊瀏覽器退回一般漸層。
%% line-end %%

### 細節（不索引）
- 對手組：不認得的語法讓整條規則失效
- 支援狀態：指南沒有 Baseline 資料；不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:visual-effects:3" %%
## 條紋、棋盤、圓點、圓餅用 CSS 漸層畫，不用 SVG 或外部圖檔
- 做法：用 `linear-gradient`／`repeating-linear-gradient`／`repeating-conic-gradient`／`radial-gradient` 加硬停點畫圖樣，顏色與尺寸接 CSS 變數與 `em`；第二個停點寫 `0` 讓漸層自動修正；用漸層畫圖表時另附語意資料表
- 對手：SVG 與外部圖檔拿不到周遭的 CSS 變數與長度，圖樣不能跟著主題色或字級變（引用："these can be more flexible and performant than SVGs or external images as they can have access to CSS variables and lengths from the surrounding context."）
- 退路：不需要——支援狀態不適用，不必另設退路
- 解鎖：（缺）

經過：設計系統換了主色，條紋背景的 SVG 還是舊顏色，得重新匯出一份。改成漸層後，圖樣跟著 `--color-1` 一起換。
%% line-end %%

### 細節（不索引）
- 對手組：圖示樣式管不到
- 支援狀態：指南沒有瀏覽器支援資料，不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 4 個糾錯提醒未拆：疊多層陰影做柔和景深；非矩形或透明 PNG 用 `filter: drop-shadow()` 而非 `box-shadow`；混合模式用 `isolation: isolate` 限制範圍；漸層圖表要附語意資料表（無障礙替代內容）
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
