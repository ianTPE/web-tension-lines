---
guide: viewport-aware-dropdowns
category: ui-atoms
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-atoms/viewport-aware-dropdowns.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 會避開視窗邊緣的下拉面板

%% line-start id="mwg:viewport-aware-dropdowns" %%
## 用 `position-area` 加 `position-try-fallbacks` 讓面板碰到視窗邊緣就翻面
- 做法：按鈕用 `popovertarget` 開 `popover="auto"` 的面板（隱式錨點，不必寫 `anchor-name`）；面板設 `position-area: block-end span-inline-end` 與 `inset: auto`，再設 `position-try-fallbacks: flip-block, flip-inline, flip-block flip-inline`；邏輯與實體關鍵字不混用
- 對手：面板在預設位置溢出時會被螢幕邊緣切掉；以前要靠 Popper.js、Floating UI 這類 JS 函式庫計算位置與碰撞（引用："To prevent the panel from being cut off at the edge of the screen, define "try tactics" that the browser should attempt if the default position overflows."）
- 退路：失去主要好處——改用錨點 polyfill 或預設置中，失去原生自動翻邊
- 解鎖：面板可用 CSS 列出多個位置退路，溢出視窗時自動翻邊

經過：列表最後一列的「更多」選單往下開就超出畫面。以前要載一個定位函式庫隨時量位置，現在列出幾種退路，讓瀏覽器自己挑放得下的那個。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：Anchor positioning 核心屬性：Newly（2026-01-13）。指南原寫 "Supported by: Safari 27 (Sep 2026). Unsupported in: Chrome, Edge, and Firefox."，群組狀態誤導，見 `lines/ui-components/app-menus.md`；本線沒用到 `position-visibility`。Popover：Newly（2025-01-27）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前碰撞偵測要載定位函式庫 → 現在表格列尾的「更多動作」、卡片角落的選單、頁尾的語言切換可以在靠近視窗底部或右緣時自動往上或往左開，只用 CSS
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:viewport-aware-dropdowns:2" %%
## 不載 polyfill 時，`inset: auto` 與 `margin: 0` 要包進 `@supports`
- 做法：把 `inset: auto`、`margin: 0` 和定位規則一起放進 `@supports (position-area: block-end)`；需要時在 `@supports not (...)` 裡另給固定在底部的面板
- 對手：無條件設 `inset: auto` 或 `margin: 0`，不支援錨點定位的瀏覽器取消了 popover 的預設置中、`position-area` 又被忽略，popover 卡在 (0, 0) 或蓋住觸發鈕（引用："leaving the popover stranded at `(0, 0)` or overlapping its trigger."）
- 退路：失去主要好處——退回預設置中或固定底條，失去貼附觸發鈕與自動翻邊
- 解鎖：（缺）

經過：重設 inset 是為了讓錨點定位接手，可是在不支援的瀏覽器裡沒有人接手，面板就掉到左上角。
%% line-end %%

### 細節（不索引）
- 對手組：彈出層脫離觸發點
- 支援狀態：同 mwg:viewport-aware-dropdowns，記 Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:viewport-aware-dropdowns:3" %%
## 交給錨點定位 polyfill 的規則不要包在 `@supports` 裡
- 做法：只在 `CSS.supports("anchor-name: --a")` 為 false 時載入 polyfill；交給 polyfill 的規則不包 `@supports`；每組觸發鈕與面板明確設成對的 `anchor-name`／`position-anchor`，需要退路時用 inset 上的 `anchor()` 而非 `position-area`
- 對手：不支援的瀏覽器把 `@supports (position-area: ...)`、`@supports (anchor-name: --a)` 判為 false，在 polyfill 處理之前就把整塊規則丟掉（引用："Browsers without native anchor positioning evaluate `@supports (position-area: ...)` and `@supports (anchor-name: --a)` to `false` and discard the block before the polyfill can process it."）
- 退路：保住主要行為——不支援時載入錨點 polyfill，以明確錨點與 inset 規則定位
- 解鎖：（缺）

經過：`@supports` 本來是保護舊瀏覽器的，遇上 polyfill 反而把它要讀的規則先藏起來了。
%% line-end %%

### 細節（不索引）
- 對手組：功能偵測不可靠
- 支援狀態：同 mwg:viewport-aware-dropdowns，記 Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:viewport-aware-dropdowns:4" %%
## 沒做完鍵盤合約就別加 `role="menu"` 和 `aria-haspopup`
- 做法：把面板當成「popover 裡的按鈕群組」；只有完整實作方向鍵導覽等鍵盤合約時，才加 `role="menu"`／`menuitem` 與 `aria-haspopup`
- 對手：觸發鈕加了 `aria-haspopup`，等於向輔助技術承諾目標具備相對應的角色，而這個模式沒有（引用："its value (`menu`, `listbox`, `tree`, `grid`, or the legacy `true`) is a promise that the target exposes a matching role, which this pattern does not."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：讀屏唸出「選單」，使用者就會按方向鍵，結果什麼都沒動。角色是承諾，做不到就別說。
%% line-end %%

### 細節（不索引）
- 對手組：語意結構失真
- 支援狀態：ARIA：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 2 個糾錯提醒未拆：popover polyfill 載入前不要用 `popover` IDL 屬性；`:popover-open` 要和 polyfill 的 class 合在 `:is()` 裡（與前幾批一致，polyfill 坑不另拆）
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
