---
guide: position-aware-tooltips
category: ui-atoms
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-atoms/position-aware-tooltips.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 知道自己位置的 tooltip

%% line-start id="mwg:position-aware-tooltips" %%
## 用 anchored container queries 讓箭頭跟著翻轉
- 做法：tooltip 用 popover 加 `popovertarget`（自動建立隱式錨點），設 `position-try-fallbacks: flip-block` 與 `container-type: anchored`；在 `@container anchored(fallback: flip-block)` 裡改內層元素 `::before` 箭頭的方向與位置；要改外框本身的圓角、間距時多包一層內層元素
- 對手：tooltip 預設在錨點上方、箭頭朝下；捲動後翻到下方時，箭頭指錯方向，也在錯的一側（引用："If the user scrolls and the tooltip flips to appear *below* the anchor, the arrow is now pointing the wrong way and is on the wrong side of the tooltip."）
- 退路：保住主要行為——不支援 anchored 查詢時隱藏箭頭，tooltip 仍可翻邊
- 解鎖：CSS 可查詢實際套用的錨點退路，讓箭頭方向跟著翻轉

經過：錨點定位讓 tooltip 碰到邊緣會自己翻面，但翻面這件事以前只有瀏覽器知道，箭頭不知道。新的查詢讓樣式能問「我現在在哪一邊」。
%% line-end %%

### 細節（不索引）
- 對手組：彈出層脫離觸發點
- 支援狀態：Anchor position container queries：Limited availability。Supported by: Chrome 143, Edge 143。Unsupported in: Firefox, Safari。Popover：Newly（2025-01-27）。本指南未給 anchor positioning 群組狀態
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前 tooltip 翻面後箭頭還指著反方向，只好拿掉箭頭或寫 JS 偵測 → 現在說明氣泡、導覽教學框、圖表標註可以讓箭頭永遠指向觸發點，純 CSS。目前僅 Chromium
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:position-aware-tooltips:2" %%
## tooltip 不要蓋住剛取得焦點的控制項
- 做法：tooltip 可能遮住下一個聚焦元素時，調整它的位置，或在它不再相關時關閉
- 對手：鍵盤導覽不會關閉 `popover=auto` 的 tooltip，它可能蓋住剛取得焦點的控制項，不符 WCAG 2.4.11 Focus Not Obscured（引用："Keyboard navigation does not close a `popover=auto` tooltip, so ensure that tooltips do not obscure interactive elements as they receive focus via keyboard."）
- 退路：保住主要行為——不支援 popover 時載入 polyfill，保留提示開關行為
- 解鎖：（缺）

經過：滑鼠使用者移開就看不到 tooltip，鍵盤使用者卻會帶著它一路 Tab 下去，下一個按鈕剛好被它蓋住。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：Popover：Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 2 個糾錯提醒未拆：popover polyfill 載入前不要用 `popover` IDL 屬性；`:popover-open` 要和 polyfill 的 class 合在 `:is()` 裡，否則整條規則被丟掉（與前幾批一致，polyfill 坑不另拆）
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
