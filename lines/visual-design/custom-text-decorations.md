---
guide: custom-text-decorations
category: visual-design
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/visual-design/custom-text-decorations.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 自訂文字裝飾線

%% line-start id="mwg:custom-text-decorations" %%
## 底線、上線、刪除線用原生 `text-decoration`，不用邊框、背景漸層或偽元素假造
- 做法：`:where(.decorated)` 裡用 `text-decoration` 簡寫設線型、樣式、顏色與 `max(1px, 0.08em)` 的粗細，`text-underline-offset: 0.2em` 調距離；懸停時換 `text-decoration-color` 與粗細
- 對手：用邊框、背景漸層或偽元素假造的線，不會跟著文字換行、不會隨字型度量調整、不會避開下伸部、也不會繼承到巢狀元素（引用："A native decoration follows the text across wrapped lines, tracks the font's metrics, skips glyph descenders, and inherits through nested elements, so none of that needs to be reimplemented."）
- 退路：不需要——支援狀態不適用，不必另設退路
- 解鎖：（缺）

經過：用 `border-bottom` 做的連結底線，連結一換行就只剩最後一行有線，而且直接穿過 g、y 的尾巴。
%% line-end %%

### 細節（不索引）
- 對手組：手工重現瀏覽器渲染
- 支援狀態：text-decoration 系列：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:custom-text-decorations:2" %%
## 有裝飾線的連結用真的 `<a href>`，不用 `javascript:void(0)`
- 做法：連結指向實際目的地，開新分頁加 `target="_blank" rel="noopener"`；不是連結的底線文字要做得不像連結
- 對手：`href="javascript:void(0)"` 加腳本處理會失去中鍵、複製連結與讀屏行為（引用："A real link keeps middle-click, copy-link, and screen reader behavior."）
- 退路：不需要——支援狀態不適用，不必另設退路
- 解鎖：（缺）

經過：右鍵「複製連結」得到的是 `javascript:void(0)`，貼給別人完全沒用。
%% line-end %%

### 細節（不索引）
- 對手組：自製控制項丟掉原生行為
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:custom-text-decorations:3" %%
## 中文、日文的底線用 `text-decoration-skip-ink: all` 避開筆畫
- 做法：底線靠近基線、會碰到表意文字時，或混合文字需要一致外觀時，設 `text-decoration-skip-ink: all`；拉丁文維持預設 `auto` 不寫；很粗或刻意裝飾的線用 `none`
- 對手：預設的 `auto` 只在多數文字系統避開筆畫，日文、中文這類不在其中，底線直接壓過字（引用："all: also skip ink in scripts where auto does not, such as Japanese or Chinese."）
- 退路：失去主要好處——退回預設 `auto` 仍保留底線與拉丁文避讓，但中日文筆畫仍會被壓過
- 解鎖：加上 `text-decoration-skip-ink: all` 讓中日文等表意文字的貼近基線底線也能自動避開筆畫

經過：中文文章的連結底線緊貼著字，「這」「還」的走之底被線切過去，一整行看起來像刪除線。
%% line-end %%

### 細節（不索引）
- 對手組：版面擠壓破壞可讀性
- 支援狀態：text-decoration-skip-ink: all：Baseline Newly available（2026-05-07 起），Supported by: Chrome 148, Edge 148, Firefox 75, Safari 15.4
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前中日文的底線只能拉遠避免壓字，或乾脆不用底線 → 現在中文部落格、日文文件、中英混排的介面可以用貼近文字的細底線，筆畫處自動斷開，連結辨識度和美觀兼顧
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:custom-text-decorations:4" %%
## 用 `text-decoration-inset` 做懸停時長出來的底線
- 做法：`text-decoration-inset: 0 100%` 把底線尾端內縮到長度為零，懸停與 `:focus-visible` 時過渡回 `0 0`；只在 `prefers-reduced-motion: no-preference` 裡隱藏與動畫，其他情況底線一直顯示；也可用正負值縮短或延長線段兩端
- 對手：以往這種效果靠邊框或背景漸層假造，失去原生裝飾線跟著換行、避開筆畫等行為（引用："To reveal an underline on hover without a border or background gradient, trim the end by 100% and transition it back to 0"）
- 退路：不需要——支援狀態不適用（未支援時保留正常底線、僅無懸停展開動畫）
- 解鎖：用 `text-decoration-inset` 調整起訖縮排，不必假造邊框就能做出原生底線的懸停展開動畫

經過：導覽列想做「滑過時底線從左邊畫出來」，以前得用偽元素加 `scaleX` 假造。現在底線就是那條原生底線，只是長度會動。
%% line-end %%

### 細節（不索引）
- 對手組：手工重現瀏覽器渲染
- 支援狀態：text-decoration-inset：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前懸停底線動畫都要額外偽元素 → 現在導覽列、文章內連結、標籤頁的作用中指示都能讓真正的底線伸縮，多行連結也照樣正確
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:custom-text-decorations:5" %%
## 波浪線、箭頭標籤這類形狀用 `border-shape`，只改角落用 `corner-shape`
- 做法：偽元素加 `border-shape: shape(…)` 畫出波浪底線，再用 `clip-path` 過渡做「畫出來」的動畫；標籤的尖角外框用 `border-shape: polygon(…)`；只要斜角、內凹、缺角時用 `corner-shape` 配 `border-radius`
- 對手：不支援時要用 `evenodd` 的 `clip-path` 在偽元素上切出外框環，斜邊的筆畫會變細；而 `clip-path` 也會切掉焦點外框與陰影（引用："`clip-path` also clips focus rings and `box-shadow`."）
- 退路：失去主要好處——退回 `clip-path` 偽元素或直線，斜邊筆畫變細、切掉焦點框且失去曲線描邊
- 解鎖：用 `border-shape` 或 `corner-shape` 直接沿形狀描邊，不會像裁切一樣切掉焦點外框與陰影

經過：做一個尖頭的價格標籤，用 clip-path 切出來後鍵盤聚焦時看不到焦點框，斜邊的線也比直邊細。
%% line-end %%

### 細節（不索引）
- 對手組：裁切切掉不該切的
- 支援狀態：border-shape：Limited availability，Supported by: Chrome 147, Edge 147；Unsupported in: Firefox, Safari。corner-shape：本篇未給支援資料（`mwg:breadcrumbs:2` 記 Limited）
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前非矩形的外框要切 clip-path 或畫 SVG → 現在價格標籤、對話氣泡、手繪感的波浪底線都能用一個 CSS 屬性描邊，焦點框和背景照常。目前僅 Chromium
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:custom-text-decorations:6" %%
## 漸層外框、中間透明，用 `background-clip: border-area`
- 做法：透明邊框配 `linear-gradient(…) border-box` 背景，再設 `background-clip: border-area` 讓背景只畫在邊框範圍；放在 `@supports` 裡
- 對手：不支援時宣告被忽略，背景畫滿整個邊框盒，填滿了文字底下而不只是外框（引用："the background paints under the whole border box, filling the text instead of only its outline."）
- 退路：保住主要行為——退回 `padding-box` 遮罩或雙層漸層仍保中空漸層外框，僅失去單一屬性簡潔性
- 解鎖：只設 `background-clip: border-area` 就能畫出真正中空透出背景的漸層外框，不必另寫遮罩偽元素

經過：想做一顆漸層描邊、透明底的按鈕，以前要嘛假設底色疊一層實色，要嘛用 mask-composite 挖洞。現在背景直接只畫在邊框上。
%% line-end %%

### 細節（不索引）
- 對手組：裁切切掉不該切的
- 支援狀態：background-clip: border-area：Limited availability，Supported by: Chrome 150, Edge 150, Safari 18.2；Unsupported in: Firefox
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前漸層描邊只能在已知底色上假造 → 現在浮在照片或影片上的漸層外框按鈕、標籤、頭像圈可以真正中空透出背景。Firefox 仍需遮罩退路
- 另有 2 個糾錯提醒未拆：`text-decoration-skip-spaces` 只在要裝飾空白或逐字斷開時才寫；畫線動畫要尊重減少動態，預設保持完整線條
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
