---
guide: anchor-positioning-tab-underline
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/anchor-positioning-tab-underline.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 以錨點定位做分頁底線

%% line-start id="mwg:anchor-positioning-tab-underline" %%
## 用錨點定位讓分頁底線滑到新的作用中分頁
- 做法：在 `<ul>` 的 `::before` 畫底線，`position: absolute` 加 `position-anchor: --active`；作用中的 `<li>` 設 `anchor-name: --active`；用邏輯 inset 屬性加 `anchor(self-start)`／`anchor(self-end)` 定位，在 `prefers-reduced-motion: no-preference` 時加 `transition: inset .2s`
- 對手：沒有錨點定位時只能在作用中的分頁畫一條靜態的 `border-block-end`，切換分頁時底線不會滑動（引用："hide the pseudo-element and draw a static `border-block-end` on the active tab."）
- 退路：保住主要行為——退回靜態 `border-block-end`，或讓底線直接跳到新分頁，失去滑動動畫
- 解鎖：用錨點定位讓純 CSS 底線跟著作用中分頁平滑移動並配合寬度變化，不必新增 DOM

經過：底線從一個分頁滑到另一個，以前要量兩個分頁的位置和寬度再用 JS 推過去。現在底線只要「跟著帶有那個錨點名稱的元素」，名稱換手，底線就跟過去。Firefox 能定位但還不能過渡 `anchor()` 的值，底線會直接跳到新分頁。
%% line-end %%

### 細節（不索引）
- 對手組：尺寸動畫只能跳變
- 支援狀態：Anchor positioning animations and transitions：Limited availability，Supported by: Chrome 125, Edge 125, Safari 26；Unsupported in: Firefox。css.types.anchor：Newly（2026-01-13），Supported by: Chrome 125, Edge 125, Firefox 147, Safari 26
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前會滑動的作用中指示要用 JS 量位置 → 現在分頁列、分段控制、垂直側欄的指示點可以純 CSS 從舊位置滑到新位置、寬度跟著變；同一招也能做「跟著游標所在列移動的高亮框」。Firefox 目前只會跳、不會滑
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-25（v1.0.2）上游把支援資料拆成錨點定位（Newly）與錨點動畫（Limited，Firefox 不支援），支援狀態由 Newly 改為 Limited；原對手引文被改寫，改引新句；做法改用 `anchor(self-start)`／`anchor(self-end)`；退路分類與戰報不變

%% line-start id="mwg:anchor-positioning-tab-underline:2" %%
## 要動畫的錨定元素別用 `position-area`
- 做法：底線用 inset 屬性加 `anchor()` 定位，不用 `position-area`
- 對手：`position-area` 無法過渡（引用："DO NOT use position-area, which can not be transitioned."）
- 退路：保住主要行為——不能過渡 `anchor()` 時保留錨定的底線，直接跳到新分頁，失去動畫
- 解鎖：（缺）

經過：`position-area` 寫起來最省事，但它是格子裡的區域選擇，不是數值，所以從 A 換到 B 只能瞬移。
%% line-end %%

### 細節（不索引）
- 對手組：尺寸動畫只能跳變
- 支援狀態：同 mwg:anchor-positioning-tab-underline，錨點動畫記 Limited（Firefox 不支援）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-25（v1.0.2）支援狀態由 Newly 改為 Limited，退路句改為「不能過渡時直接跳到新分頁」；退路分類與戰報不變

%% line-start id="mwg:anchor-positioning-tab-underline:3" %%
## 底線用 border 畫，不用背景或陰影
- 做法：底線用 `border-block-end` 畫
- 對手：用 `background` 或 `box-shadow` 畫底線，強制色彩模式會把兩者都移除，什麼指示都沒有（引用："forced colors mode removes both, leaving no indicator."）
- 退路：不需要——支援狀態不適用，不必另設退路
- 解鎖：（缺）

經過：高對比模式的使用者最需要知道自己在哪個分頁，而他們看到的是一排一模一樣的文字。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：border：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 2 個糾錯提醒未拆：底線只是視覺指示，仍要設 `aria-current="page"` 或 `aria-selected`；RTL 分頁列放在 LTR 頁面裡時用 `anchor(self-start)`／`anchor(self-end)`，錨邊才會和邏輯 inset 一致（v1.0.2 新增）
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
