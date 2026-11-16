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
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在 `<ul>` 的 `::before` 畫底線，`position: absolute` 加 `position-anchor: --active`；作用中的 `<li>` 設 `anchor-name: --active`；用 inset 屬性加 `anchor()` 定位（`inset-inline-start: anchor(left)` 等），在 `prefers-reduced-motion: no-preference` 時加 `transition: inset .2s`
- 被什麼擋：沒有錨點定位時只能在作用中的分頁畫 `border-bottom`，切換分頁時底線沒有動畫（引用："If anchor positioning is not supported in the browser, use a `border-bottom` to add an underline. It will not be animated."）
- 戰報：部分改善——底線平滑移到新的作用中分頁，連寬度一起變，也不必為裝飾多加 DOM 元素；換分頁會載入新網頁時無效；錨點定位核心屬性為 Newly，更舊的瀏覽器退回不動畫的 `border-bottom`（官方宣稱；支援狀態依已驗證偏差修正）

經過：底線從一個分頁滑到另一個，以前要量兩個分頁的位置和寬度再用 JS 推過去。現在底線只要「跟著帶有那個錨點名稱的元素」，名稱換手，底線就跟過去。
%% line-end %%

### 細節（不索引）
- 對手組：尺寸動畫只能跳變
- 支援狀態：Anchor positioning 核心屬性：Newly（2026-01-13；`position-anchor` 2026-09-14）。指南原寫 "Supported by: Safari 27 (Sep 2026). Unsupported in: Chrome, Edge, and Firefox."，群組狀態誤導，見 `lines/ui-components/app-menus.md`；本線沒用到 `position-visibility`
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前會滑動的作用中指示要用 JS 量位置 → 現在分頁列、分段控制、垂直側欄的指示點可以純 CSS 從舊位置滑到新位置、寬度跟著變；同一招也能做「跟著游標所在列移動的高亮框」
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:anchor-positioning-tab-underline:2" %%
## 要動畫的錨定元素別用 `position-area`
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：底線用 inset 屬性加 `anchor()` 定位，不用 `position-area`
- 被什麼擋：`position-area` 無法過渡（引用："DO NOT use position-area, which can not be transitioned."）
- 戰報：部分改善——inset 屬性可以過渡，底線才滑得過去（官方宣稱）

經過：`position-area` 寫起來最省事，但它是格子裡的區域選擇，不是數值，所以從 A 換到 B 只能瞬移。
%% line-end %%

### 細節（不索引）
- 對手組：尺寸動畫只能跳變
- 支援狀態：同 mwg:anchor-positioning-tab-underline，記 Newly
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:anchor-positioning-tab-underline:3" %%
## 底線用 border 畫，不用背景或陰影
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：底線用 `border-block-end` 畫
- 被什麼擋：用 `background` 或 `box-shadow` 畫底線，強制色彩模式會把兩者都移除，什麼指示都沒有（引用："forced colors mode removes both, leaving no indicator."）
- 戰報：勝——border 在強制色彩模式下保留（官方宣稱）

經過：高對比模式的使用者最需要知道自己在哪個分頁，而他們看到的是一排一模一樣的文字。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：border：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 另有 1 個糾錯提醒未拆：底線只是視覺指示，仍要設 `aria-current="page"` 或 `aria-selected`
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
