---
guide: typography
category: visual-design
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/visual-design/typography.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 字體排印

%% line-start id="mwg:typography" %%
## 字級用 `rem`，不用 `px`
- 做法：`font-size` 用 `rem`（跟隨根字級），需要依情境縮放時用 `em` 或百分比
- 對手：`px` 字級不理會使用者在瀏覽器設定的字級偏好（引用："Prefer `rem` to honor the user's browser font-size preferences (root font size)"）
- 退路：不需要——支援狀態不適用，不必另設退路
- 解鎖：（缺）

經過：視力不好的使用者把瀏覽器預設字級調大，用 `px` 寫死的網站內文仍是原本的大小。改成 `rem` 後，整站文字照他的設定放大。
%% line-end %%

### 細節（不索引）
- 對手組：忽略使用者設定
- 支援狀態：指南沒有瀏覽器支援資料，不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:typography:2" %%
## 有文字的元件不設固定高度，改用 `min-block-size`
- 做法：按鈕、徽章、分頁、卡片等含文字的元素不設 `height`／`block-size`，讓內容決定高度，需要最小值時用 `min-block-size`
- 對手：使用者加大行高、段距、字距與詞距時，固定高度的元件裡文字溢出或被裁掉（引用："so text doesn't overflow or get clipped when users increase text spacing to a line height of 1.5, spacing after paragraphs of 2em, letter spacing of 0.12em and word spacing of 0.16em"）
- 退路：不需要——支援狀態不適用，不必另設退路
- 解鎖：（缺）

經過：設計稿上的按鈕高 40px，寫成固定高度；使用者用擴充功能加大行距，按鈕文字的下半截就被切掉。改成最小高度後按鈕自己長高。
%% line-end %%

### 細節（不索引）
- 對手組：尺寸不跟內容走
- 支援狀態：指南沒有瀏覽器支援資料，不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:typography:3" %%
## 避免兩端對齊；非用不可時配 `hyphens: auto` 並宣告 `lang`
- 做法：內文用 `text-align: start`（同時支援 LTR 與 RTL）；必須用 `text-align: justify` 時加 `hyphens: auto`，並確認文字有 `lang` 屬性（如 `<html lang="en">`），否則不會斷字
- 對手：兩端對齊在字與字之間撐出過大的空白、讓文字更難讀（引用："Avoid `text-align: justify` as it can make text harder to read. If you must use it, combine it with `hyphens: auto` to avoid excessive whitespace between words."）
- 退路：不需要——支援狀態不適用，不必另設退路
- 解鎖：（缺）

經過：窄欄的英文文章用兩端對齊，長單字一換行，上一行的字就被拉開成一條條白色河流。加上斷字後空白變小，但前提是頁面有寫 `lang`。
%% line-end %%

### 細節（不索引）
- 對手組：版面擠壓破壞可讀性
- 支援狀態：指南沒有瀏覽器支援資料，不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:typography:4" %%
## 長網址用 `overflow-wrap` 斷開，內文不用 `nowrap` 與固定寬度
- 做法：設 `overflow-wrap: break-word`（或 `anywhere`）容納長網址；內文避免 `white-space: nowrap` 與固定寬度，讓文字在 320 CSS px 寬時能重排
- 對手：不換行、固定寬度的內文在窄螢幕或放大時撐出容器，得橫向捲動（引用："let text reflow at a 320 CSS px viewport width without horizontal scrolling (WCAG 1.4.10 Reflow); avoid `white-space: nowrap` and fixed widths on running text."）
- 退路：不需要——支援狀態不適用，不必另設退路
- 解鎖：（缺）

經過：留言區有人貼了一條很長的追蹤網址，手機上整個頁面被撐寬，每行都要左右滑著讀。讓長字可以斷開後，網址折成幾行，版面回到正常寬度。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：指南沒有瀏覽器支援資料，不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:typography:5" %%
## 流體字級用 `clamp()` 混合 `rem` 與 `vw`，上限不超過下限的 2.5 倍
- 做法：寫成 `font-size: clamp(2rem, 1rem + 5vw, 4rem)` 這類形式，最小與最大值用字型相對單位，最大值不超過最小值的 2.5 倍；不單獨用 `vw` 當字級
- 對手：視窗單位不隨使用者縮放變大，只用 `vw` 的字級在極端螢幕上太小或太大（引用："Viewport units don't grow when users zoom … it can scale text too small or too large on extreme screens."）
- 退路：不需要——支援狀態不適用，不必另設退路
- 解鎖：（缺）

經過：主視覺標題寫成 `6vw`，使用者按了好幾次放大，標題文字紋風不動。改用 `rem` 打底的 `clamp()` 並限制上下限比例後，放大時標題跟著變大。
%% line-end %%

### 細節（不索引）
- 對手組：忽略使用者設定
- 支援狀態：指南沒有瀏覽器支援資料，不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:typography:6" %%
## 標題用 `text-wrap: balance`，長篇內文用 `text-wrap: pretty`
- 做法：標題與類標題內容（例如 `<th>`）設 `text-wrap: balance`；段落、引文等長篇內文設 `text-wrap: pretty`
- 對手：缺——指南只說用來平衡標題、處理長篇內文，沒說預設換行在哪個時刻出問題
- 退路：不需要——支援狀態不適用，不支援時退回一般換行
- 解鎖：用 `text-wrap: balance` 與 `pretty` 讓標題各行均衡、長篇段落自動美化斷行

經過：新聞卡片的兩行標題，第二行常常只剩一個字。交給瀏覽器平衡換行後，兩行長度接近。
%% line-end %%

### 細節（不索引）
- 對手組：版面擠壓破壞可讀性
- 支援狀態：指南沒有瀏覽器支援資料，不適用（`text-wrap` 的支援狀態見 `lines/visual-design/improve-text-layout-and-legibility.md`）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前標題斷行要手插 `<br>` 或依寬度逐一調整 → 現在新聞列表、卡片標題、表格欄位標題在任何寬度都自動斷得整齊，CMS 產生的文字也一樣
- 與 `mwg:improve-text-layout-and-legibility`、`:2` 的對手相同，這裡依本指南原文另拆
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:typography:7" %%
## `balance`／`pretty` 只套在需要的元素，不套在 `*`
- 做法：刻意挑選要平衡或美化換行的元素，不寫 `* { text-wrap: balance; }`
- 對手：這兩種換行有效能成本，全域套用讓整頁都付代價（引用："**DO NOT** apply it on `*` as it does have a performance cost."）
- 退路：不需要——支援狀態不適用，不必另設退路
- 解鎖：（缺）

經過：為了省事把 balance 套到全站，文字多的頁面排版變慢。改成只套在標題後，成本集中在真正需要的幾行。
%% line-end %%

### 細節（不索引）
- 對手組：優化用過頭反傷
- 支援狀態：指南沒有瀏覽器支援資料，不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 與 `mwg:improve-text-layout-and-legibility:3` 對手相同
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:typography:8" %%
## 有背景或邊框的元素不用 `text-wrap: balance`
- 做法：按鈕、標籤、有背景色、邊框或陰影的標題框不加 `balance`
- 對手：`balance` 只改容器內的換行位置，不改容器寬度，可見的盒子尾端留下一塊空白（引用："it does not change the container's width, it only affects how text wraps *within* that width. This can leave empty space at the end of the container"）
- 退路：不需要——支援狀態不適用，不必另設退路
- 解鎖：（缺）

經過：有底色的提示框加了 balance，兩行字變得一樣短，右側卻留下一大塊空著的底色。拿掉後文字填回整個寬度。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：指南沒有瀏覽器支援資料，不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 與 `mwg:improve-text-layout-and-legibility:4` 對手相同
- 另有 5 個糾錯提醒未拆：`line-height` 用無單位數字；段落寬度上限約 80 字元（`max-width: 60ch`）；主要內文不用花體字；不靠全大寫表示強調；強調不要用得到處都是
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
