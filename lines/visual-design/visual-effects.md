---
guide: visual-effects
category: visual-design
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/visual-design/visual-effects.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 視覺效果

%% line-start id="mwg:visual-effects" %%
## 漸層與 `color-mix()` 明確指定插值色彩空間，預設 `in oklab`，混中性色不用 `in oklch`
- 做法：漸層與 `color-mix()` 加上插值空間；`color-mix()` 預設用 `in oklab`，尤其是混中性色；`in oklch` 只用在兩個飽和色相之間的漸層（保住彩度，但色差大時較容易超出色域）；除非有特定理由（例如做 sRGB 取色器），不用 `in srgb`
- 對手：用 `in oklch` 混中性色時，Chromium 的 bug 讓低彩度顏色的色相解成 `0deg`，混出不該有的偏紅／粉紅色（引用："low chroma oklch colors have powerless hue angles (`none`), which resolve to `0deg` (magenta-red) and cause an unintended reddish/pink tint shift when rendered."）
- 退路：不需要——支援狀態不適用，部分舊瀏覽器可搭配條件變數退回預設插值
- 解鎖：用 `in oklch` 或 `in oklab` 指定漸層與 `color-mix()` 插值色彩空間，依需求保彩度或保色域

經過：把品牌色和白或灰混成淡色時寫了 `in oklch`，在 Chromium 上中性色意外帶了一層粉紅。`in oklab` 用直角座標往 (0, 0) 縮，不必算色相角，色相保持不變。兩個飽和色相之間的漸層才值得用 oklch 換中段鮮豔。
%% line-end %%

### 細節（不索引）
- 對手組：瀏覽器實作有缺陷
- 支援狀態：指南沒有 Baseline 資料，只說部分 2024 年以前的瀏覽器不支援漸層的插值色彩空間；不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前漸層只能接受瀏覽器預設的混色方式 → 現在品牌雙色漸層、資料視覺化的連續色階、`color-mix()` 產生的 hover 色都能指定在哪個色彩空間混，依畫面選保彩度或保色域
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18（v1.0.1）上游補上具體對手（`in oklch` 混中性色在 Chromium 偏紅），對手由缺改為有，對手組由「主題配色對不上」改為「新功能的副作用」，做法改為預設 `in oklab`；同版 color 指南也加了同一提醒；2026-11-18 對手組由「新功能的副作用」改為「瀏覽器實作有缺陷」

%% line-start id="mwg:visual-effects:2" %%
## 用 `@supports` 設定的自訂屬性帶入插值空間，並保留非空的漸層前導
- 做法：`:root` 先把 `--in-oklab`、`--in-oklch` 設成空值，`@supports (background: linear-gradient(in oklab, white, black))` 成立時才填入 `in oklab`／`in oklch`，用成 `linear-gradient(to bottom var(--in-oklab), …)`；變數之外一定要有方向之類的非空前導；`color-mix()` 不需要這招
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
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18（v1.0.1）上游把 `@supports (linear-gradient(...))` 更正為 `@supports (background: linear-gradient(...))`，做法句跟著改；對手與戰報不變

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
