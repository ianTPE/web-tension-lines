---
guide: interest-triggered-tooltips
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/interest-triggered-tooltips.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 懸停時顯示工具提示

%% line-start id="mwg:interest-triggered-tooltips" %%
## 用 `popover="hint"` 加 `interestfor` 做不會關掉選單的工具提示
- 做法：提示用 `<div popover="hint" id>`，觸發的 `<button>`／`<a>` 寫 `interestfor`；觸發元素自動成為隱式錨點，用 `position-area: block-start` 與 `position-try-fallbacks: flip-block` 定位；toggletip 另加 `popovertarget` 與 `popovertargetaction="show"`
- 對手：用 `auto` popover 做提示時，懸停經過提示就會把已打開的選單關掉（引用："hovering across a toggletip must not close an open menu, which an `auto` popover would"）
- 退路：失去主要好處——退回 popover=auto，開提示仍可能關掉已開選單
- 解鎖：純用 HTML 屬性與 CSS 錨點就能做出不關掉既有選單的工具提示，懸停、聚焦與長按皆可觸發並自動避邊翻轉

經過：提示和選單都是 popover，以前開一個就關另一個。hint 是第三種類型，專給「看一眼就走」的內容，懸停、聚焦、長按都能叫出，不打擾正開著的東西。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：Interest invokers：Limited（Chrome 149, Edge 149）；popover="hint"：Limited（Chrome 151, Edge 151, Firefox 153；Unsupported in: Safari）；Anchor positioning 核心屬性：Newly。指南原寫 "Supported by: Safari 27 (Sep 2026). Unsupported in: Chrome, Edge, and Firefox."，群組狀態誤導，見 `lines/ui-components/app-menus.md`；本線沒用到 `position-visibility`
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前提示要自己接 hover/focus/Esc 還會跟選單搶 → 現在圖示按鈕的說明、術語解釋、連結預覽卡可以幾乎全宣告式做出來，選單開著也能看提示。原生僅 Chromium，其他靠 polyfill
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 交叉核對仲裁：退路改為「失去主要好處」

%% line-start id="mwg:interest-triggered-tooltips:2" %%
## 會自己做事的觸發元素不加 `aria-expanded`
- 做法：觸發元素按下後是導覽或執行動作（連結、有自己動作的按鈕）時，提示設 `role="tooltip"`、觸發元素用 `aria-describedby`，不加 `aria-expanded`；只有按下就開提示的 toggletip 才用 `aria-expanded`，並由 popover 的 `toggle` 事件同步
- 對手：被唸成「已收合」的觸發元素讓人以為按 Enter 會展開，實際上 Enter 是導覽或執行動作（引用："A trigger announced as "collapsed" suggests `Enter` would expand it, but `Enter` navigates or acts."）
- 退路：保住主要行為——在載入 polyfill 前先執行統一的前置 ARIA 腳本，所有瀏覽器都能暴露正確角色與關聯
- 解鎖：（缺）

經過：瀏覽器與讀屏還沒一致地暴露 `interestfor` 的語意，所以要自己補 ARIA；補錯一個 `aria-expanded`，連結就被唸成可展開的東西。
%% line-end %%

### 細節（不索引）
- 對手組：語意結構失真
- 支援狀態：Interest invokers：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:interest-triggered-tooltips:3" %%
## 提示和可及名稱相同時什麼都別加
- 做法：正規化空白後比對提示文字與觸發元素的可及名稱，相同就不加描述；觸發元素沒有名稱時才用 `aria-labelledby` 指向提示
- 對手：例如 `aria-label="Bold"` 的圖示按鈕配上「Bold」提示，描述和名稱一樣會被唸兩次（引用："A description identical to the name would be read twice."）
- 退路：保住主要行為——前置腳本在所有瀏覽器與 polyfill 環境皆先比對名稱，相同時不補 aria-describedby 免重複朗讀
- 解鎖：（缺）

經過：工具提示最常見的內容就是按鈕名稱本身；再接成描述，讀屏就唸「Bold，Bold」。
%% line-end %%

### 細節（不索引）
- 對手組：播報過量
- 支援狀態：Interest invokers：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:interest-triggered-tooltips:4" %%
## 當描述用的提示只能放錯過也無妨的內容
- 做法：接成描述的提示只放連結預覽、動作說明這類可錯過的內容；使用者需要的資訊放 toggletip 或直接寫在頁面上
- 對手：不是每個讀屏在瀏覽時都會唸描述，NVDA 在瀏覽模式下刻意跳過（引用："Not every screen reader reads descriptions when moving through the page (NVDA skips them in browse mode by design)"）
- 退路：保住主要行為——關鍵資訊本就改放 toggletip 或內文並搭配 polyfill，所有瀏覽器與讀屏都能取得
- 解鎖：（缺）

經過：把「為什麼這欄必填」塞進懸停提示，看得到的人偶爾會看到，NVDA 使用者則根本不會聽到。
%% line-end %%

### 細節（不索引）
- 對手組：播報時機或可靠度出錯
- 支援狀態：Interest invokers：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:interest-triggered-tooltips:5" %%
## `toggle` 不冒泡，同步 `aria-expanded` 要用捕獲
- 做法：在 `document` 用單一捕獲監聽器接 popover 的 `toggle` 事件，同步所有指向該提示的觸發元素；以 popover 為準，不從 `interest`／`loseinterest` 同步
- 對手：`toggle` 不冒泡，掛在 `document` 的一般監聽器永遠不會觸發；popover 也可能被 Esc、點外面或其他觸發元素關掉（引用："A bubbling listener on `document` never fires; use the capture phase (or a listener per popover)."）
- 退路：保住主要行為——在 document 用捕獲監聽同步 aria-expanded，原生與 polyfill 環境都能準確反映開關狀態
- 解鎖：（缺）

經過：以為從興趣事件同步就好，提示被 Esc 關掉後觸發元素卻還唸「已展開」。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：Popover：Newly；Interest invokers：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:interest-triggered-tooltips:6" %%
## 不支援 `hint` 時，toggletip 要在 `beforetoggle` 改成 `auto`
- 做法：用探針元素設 `popover = "hint"` 再讀回判斷支援；不支援時在捕獲階段的 `beforetoggle` 裡，把要開啟的 toggletip 改成 `popover = "auto"`
- 對手：不支援 `hint` 的瀏覽器把它當成 `manual`：鍵盤聚焦開的提示，在指標懸停開另一個時可能還開著；用點擊開的 toggletip 沒有興趣可失去，永遠不會關（引用："so a `manual` fallback would never close"）
- 退路：保住主要行為——於捕獲階段 beforetoggle 將缺 hint 的 toggletip 轉成 auto，Safari 點擊後也能正常輕觸關閉
- 解鎖：（缺）

經過：無效的屬性值會靜默變成 `manual`，看起來能開、卻關不掉。類型要在 `beforetoggle` 改，開著再改會直接把它關掉。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：popover="hint"：Limited（Unsupported in: Safari）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:interest-triggered-tooltips:7" %%
## 不用錨點定位 polyfill 時，`inset: auto` 要包進 `@supports`
- 做法：不載 polyfill 時，`inset: auto`、`margin: 0` 與 `position-area` 一起包進 `@supports (position-area: block-end)`，或另給 `@supports not` 的底部固定列；用 polyfill 時每對觸發元素與提示要明確設 `anchor-name`／`position-anchor`，因為 polyfill 不支援隱式錨點
- 對手：無條件設 `inset: auto` 會蓋掉 popover 的預設置中，而 `position-area` 又被忽略，提示卡在左上角或蓋住觸發元素（引用："leaving the popover stranded at `(0, 0)` or overlapping its trigger"）
- 退路：保住主要行為——以 `@supports` 包住讓不支援者維持置中或底部列，或改載含明確錨點的 polyfill 照樣定位
- 解鎖：（缺）

經過：為了讓提示貼著按鈕而重設的 inset，在不懂錨點的瀏覽器裡只剩「重設」那一半。
%% line-end %%

### 細節（不索引）
- 對手組：彈出層脫離觸發點
- 支援狀態：Anchor positioning 核心屬性：Newly（群組狀態誤導，見 `lines/ui-components/app-menus.md`；本線沒用到 `position-visibility`）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 3 個糾錯提醒未拆：不在 `interest` 時把焦點移進提示（WCAG 3.2.1）；提示需符合 WCAG 1.4.13（可關閉、可懸停、持續顯示）；popover polyfill 與 interest polyfill 的注意事項與 mwg:declarative-dialog-popover-control:4、mwg:interest-triggered-action-previews 相同，未重複拆
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
