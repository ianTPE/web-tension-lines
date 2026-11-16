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
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：按鈕用 `popovertarget` 開 `popover="auto"` 的面板（隱式錨點，不必寫 `anchor-name`）；面板設 `position-area: block-end span-inline-end` 與 `inset: auto`，再設 `position-try-fallbacks: flip-block, flip-inline, flip-block flip-inline`；邏輯與實體關鍵字不混用
- 被什麼擋：面板在預設位置溢出時會被螢幕邊緣切掉；以前要靠 Popper.js、Floating UI 這類 JS 函式庫計算位置與碰撞（引用："To prevent the panel from being cut off at the edge of the screen, define "try tactics" that the browser should attempt if the default position overflows."）
- 戰報：部分改善——瀏覽器依序嘗試翻轉，面板留在視窗內又黏著觸發鈕；錨點定位核心屬性為 Newly，更舊的瀏覽器要條件載入 `@oddbird/css-anchor-positioning`，或用 `@supports` 守門保留預設置中（官方宣稱；支援狀態依已驗證偏差修正）

經過：列表最後一列的「更多」選單往下開就超出畫面。以前要載一個定位函式庫隨時量位置，現在列出幾種退路，讓瀏覽器自己挑放得下的那個。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：Anchor positioning 核心屬性：Newly（2026-01-13）。指南原寫 "Supported by: Safari 27 (Sep 2026). Unsupported in: Chrome, Edge, and Firefox."，群組狀態誤導，見 `lines/ui-components/app-menus.md`；本線沒用到 `position-visibility`。Popover：Newly（2025-01-27）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前碰撞偵測要載定位函式庫 → 現在表格列尾的「更多動作」、卡片角落的選單、頁尾的語言切換可以在靠近視窗底部或右緣時自動往上或往左開，只用 CSS
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:viewport-aware-dropdowns:2" %%
## 不載 polyfill 時，`inset: auto` 與 `margin: 0` 要包進 `@supports`
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：把 `inset: auto`、`margin: 0` 和定位規則一起放進 `@supports (position-area: block-end)`；需要時在 `@supports not (...)` 裡另給固定在底部的面板
- 被什麼擋：無條件設 `inset: auto` 或 `margin: 0`，不支援錨點定位的瀏覽器取消了 popover 的預設置中、`position-area` 又被忽略，popover 卡在 (0, 0) 或蓋住觸發鈕（引用："leaving the popover stranded at `(0, 0)` or overlapping its trigger."）
- 戰報：部分改善——不支援時保留預設置中（或底部面板），不會卡在左上角（官方宣稱）

經過：重設 inset 是為了讓錨點定位接手，可是在不支援的瀏覽器裡沒有人接手，面板就掉到左上角。
%% line-end %%

### 細節（不索引）
- 對手組：彈出層脫離觸發點
- 支援狀態：同 mwg:viewport-aware-dropdowns，記 Newly
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:viewport-aware-dropdowns:3" %%
## 交給錨點定位 polyfill 的規則不要包在 `@supports` 裡
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：只在 `CSS.supports("anchor-name: --a")` 為 false 時載入 polyfill；交給 polyfill 的規則不包 `@supports`；每組觸發鈕與面板明確設成對的 `anchor-name`／`position-anchor`，需要退路時用 inset 上的 `anchor()` 而非 `position-area`
- 被什麼擋：不支援的瀏覽器把 `@supports (position-area: ...)`、`@supports (anchor-name: --a)` 判為 false，在 polyfill 處理之前就把整塊規則丟掉（引用："Browsers without native anchor positioning evaluate `@supports (position-area: ...)` and `@supports (anchor-name: --a)` to `false` and discard the block before the polyfill can process it."）
- 戰報：部分改善——規則留在樣式表裡讓 polyfill 讀到；但 polyfill 不支援隱式錨點，也不支援 `position-area` 搭配退路，寫法要遷就它（官方宣稱）

經過：`@supports` 本來是保護舊瀏覽器的，遇上 polyfill 反而把它要讀的規則先藏起來了。
%% line-end %%

### 細節（不索引）
- 對手組：功能偵測不可靠
- 支援狀態：同 mwg:viewport-aware-dropdowns，記 Newly
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:viewport-aware-dropdowns:4" %%
## 沒做完鍵盤合約就別加 `role="menu"` 和 `aria-haspopup`
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：把面板當成「popover 裡的按鈕群組」；只有完整實作方向鍵導覽等鍵盤合約時，才加 `role="menu"`／`menuitem` 與 `aria-haspopup`
- 被什麼擋：觸發鈕加了 `aria-haspopup`，等於向輔助技術承諾目標具備相對應的角色，而這個模式沒有（引用："its value (`menu`, `listbox`, `tree`, `grid`, or the legacy `true`) is a promise that the target exposes a matching role, which this pattern does not."）
- 戰報：勝——宣告的角色與實際行為一致，讀屏使用者不會期待一個不存在的選單操作方式（官方宣稱）

經過：讀屏唸出「選單」，使用者就會按方向鍵，結果什麼都沒動。角色是承諾，做不到就別說。
%% line-end %%

### 細節（不索引）
- 對手組：語意結構失真
- 支援狀態：ARIA：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 另有 2 個糾錯提醒未拆：popover polyfill 載入前不要用 `popover` IDL 屬性；`:popover-open` 要和 polyfill 的 class 合在 `:is()` 裡（與前幾批一致，polyfill 坑不另拆）
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
