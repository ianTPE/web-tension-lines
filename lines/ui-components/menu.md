---
guide: menu
category: ui-components
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-components/menu.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 彈出選單

%% line-start id="mwg:menu" %%
## 用 `focusgroup="menu"` 加 `command="toggle-popover"` 宣告彈出選單
- 做法：觸發鈕設 `commandfor` 與 `command="toggle-popover"`，選單是緊接在後的 `popover="auto"`，裡面巢一層 `<div focusgroup="menu nomemory">`；不寫 `role="menu"`／`menuitem`，由 focusgroup 推斷；子選單是放在父選單 focusgroup 內的另一個 `popover="auto"`
- 對手：指南只要求不要在 focusgroup 裡再做一套 roving tabindex、明寫角色會擋住推斷，沒說手寫版在哪個時刻出錯（引用："Do not add a second roving-tabindex system inside a focusgroup."）
- 退路：保住主要行為——不支援時以腳本補上開合、方向鍵與角色，保留選單行為
- 解鎖：選單可用屬性宣告開合、方向鍵移動與角色，不必全部手寫

經過：選單的開關、點外面關閉、方向鍵移動、角色，以前全是自己的 JS。現在大半是屬性；開子選單預覽、焦點還原仍得自己寫，focusgroup 也只有 Chromium。
%% line-end %%

### 細節（不索引）
- 對手組：手寫焦點管理
- 支援狀態：focusgroup：Limited availability，Supported by: Chrome 150, Edge 150；Unsupported in: Firefox, Safari；Invoker commands：Newly；Popover：Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前一個有子選單的「⋯」選單要幾百行鍵盤處理 → 現在表格列的動作選單、編輯器的匯出子選單可以大半宣告式寫出，點外面關閉與子選單關係由瀏覽器管。focusgroup 目前僅 Chromium
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:menu:2" %%
## 子選單用錨點定位貼在父項目旁，不能退回視窗置中
- 做法：頂層選單 `position-area: block-end span-inline-end`、子選單 `position-area: inline-end span-block-end`，各帶 `position-try-fallbacks` 翻轉；隱式錨點來自 invoker，不寫 `anchor-name`；不支援時用 `@supports not` 加腳本計算位置
- 對手：沒有錨點定位時 popover 退回視窗置中，選單脫離觸發鈕，置中的子選單還蓋住父選單（引用："it detaches the menu from its trigger, and a centered submenu covers its parent."）
- 退路：保住主要行為——不支援錨點定位時改用腳本計算位置，選單仍貼在觸發項旁
- 解鎖：CSS 錨點定位可讓巢狀選單貼在觸發項旁並自動翻邊

經過：「匯出 ›」一展開，子選單跳到畫面正中央，把剛剛的選單整個蓋住。
%% line-end %%

### 細節（不索引）
- 對手組：彈出層脫離觸發點
- 支援狀態：Anchor positioning：記 Newly（核心屬性 2026-01-13 起 Baseline）。指南寫 "Supported by: Safari 27 … Unsupported in: Chrome, Edge, and Firefox"，為群組狀態誤導，見 `lines/ui-components/app-menus.md`；本線未用 `position-visibility`
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前多層選單要定位函式庫逐層算位置 → 現在檔案管理器的右鍵選單、編輯器的巢狀「插入」選單可以純 CSS 逐層展開並自動翻邊
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:menu:3" %%
## 窄螢幕的最後退路 `--below` 要允許子選單縮小
- 做法：`@position-try --below` 放在最後，內含 `min-inline-size: 0` 與 `max-inline-size: calc(100% - 1rem)`
- 對手：放不下的退路會被跳過；若沒有一個放得下，瀏覽器保留基本位置，寬了幾像素的子選單就靜靜蓋住自己的觸發項目（引用："a submenu that is a few pixels too wide silently covers its trigger."）
- 退路：保住主要行為——不支援錨點定位時改用腳本定位，避免子選單蓋住觸發項
- 解鎖：（缺）

經過：手機上點「匯出」，子選單正好疊在「匯出」上面，想收回都找不到按鈕。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：Anchor positioning：記 Newly（群組狀態誤導，見 `lines/ui-components/app-menus.md`）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:menu:4" %%
## 右鍵選單與游標處選單用 `showPopover({ source })` 加零尺寸佔位錨點
- 做法：沒有觸發鈕的選單以 `showPopover({ source })` 開啟，`source` 給被右鍵的卡片或目前聚焦的元素；要開在某一點（游標、`@` 提及的輸入點）時，放一個緊接在選單前、零尺寸、`position: fixed` 的佔位元素，每次開啟時移到該點再當 `source`；選單用 `aria-label` 命名
- 對手：指南只說要用錨點定位、不要用 JS 座標，沒說 JS 座標在哪個時刻出錯（引用："Use CSS anchor positioning, not JavaScript coordinates."）
- 退路：保住主要行為——舊實作改用明確 `anchor-name` 與 `position-anchor` 綁定選單
- 解鎖：零尺寸元素可充當游標或輸入點的錨，讓選單沿用 CSS 定位與翻邊

經過：右鍵選單或 @ 提及清單，以前都是讀滑鼠座標、算視窗邊界再擺上去。改成移一個看不見的點當錨，剩下的翻轉交給同一套 CSS。
%% line-end %%

### 細節（不索引）
- 對手組：彈出層脫離觸發點
- 支援狀態：showPopover() 的 source 參數（隱式錨點）：Baseline Newly available（2026-01-13 起）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前右鍵選單與輸入點選單要自己算座標與碰撞 → 現在看板卡片的右鍵選單、聊天輸入框的 @ 提及與 / 指令清單可以用同一套 CSS 定位並自動避開邊緣
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:menu:5" %%
## 子選單的「安全三角」用 CSS 畫，從游標離開的點延伸到子選單邊緣
- 做法：只在 `(hover: hover)` 時，於子選單觸發項目的 `pointerleave` 把游標位置寫成 `--pointer-x`／`--pointer-y` 並設 `data-bridge`；子選單的 `::before` 用 `clip-path: polygon()` 畫出從該點到子選單近側兩角的三角形（以 `sign()` 判斷左右），游標停下約 300ms、轉向或到達項目時移除
- 對手：靜態的 CSS 橋太窄，只有游標從父選單邊緣出發才有效；斜著移向子選單時會經過兄弟項目，把子選單關掉（引用："A static CSS bridge is too narrow: it only works when the pointer starts near the parent's edge."）
- 退路：保住主要行為——不支援 `sign()` 時改用 `clamp()` 計算三角形邊緣與頂點
- 解鎖：CSS 可畫出從游標離開點到子選單邊緣的安全三角

經過：滑鼠從「匯出」斜斜往右下移到「PDF」，途中掃過「重新命名」，子選單就收掉了。三角形擋在路徑上，兄弟項目收不到那次 hover。
%% line-end %%

### 細節（不索引）
- 對手組：動作被意外觸發
- 支援狀態：abs() 與 sign()：Baseline Newly available（2025-06-26 起）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:menu:6" %%
## 開啟後移焦點要在 `toggle` 事件裡做，不在 `command` 裡
- 做法：鍵盤開啟時在 `toggle` 監聽裡把焦點移到第一個可用項目；`aria-expanded` 也只在 `toggle` 裡設
- 對手：`command` 事件在 `toggle-popover` 打開選單之前觸發，那時焦點移不進去（引用："The `command` event fires before `toggle-popover` opens the menu, so focus cannot move into the menu there."）
- 退路：保住主要行為——不支援 Invoker Commands 時用 click 監聽開合，仍由 toggle 移焦點
- 解鎖：（缺）

經過：按 Enter 開了選單，焦點卻還留在觸發鈕上，按下鍵沒反應。
%% line-end %%

### 細節（不索引）
- 對手組：生命週期假設錯
- 支援狀態：Invoker commands：Baseline Newly available（2025-12-12 起）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:menu:7" %%
## 子選單一次只關一層，焦點自己還給它的觸發項目
- 做法：子選單裡的 Esc 與左鍵呼叫 `stopPropagation()`；關閉時先聚焦觸發項目再 `hidePopover()`
- 對手：HTML 只替堆疊中第一個 `popover="auto"` 還原焦點，巢狀層級得自己還；沒擋下冒泡時，父選單的監聽也會把自己關掉（引用："HTML restores focus only for the first `popover="auto"` in a stack, so nested levels must restore focus to their trigger explicitly. … or the parent's listener closes it too."）
- 退路：保住主要行為——不支援 popover 時載入 polyfill，保留巢狀選單開合
- 解鎖：（缺）

經過：在子選單按 Esc，整串選單一起消失，焦點掉到頁面某處。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：Popover：Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:menu:8" %%
## 勾選項目的勾號選擇器要至少和基本 `::before` 一樣特定
- 做法：`[focusgroup~="menu"] button[aria-checked="true"]::before { content: "✓" }`，特異度不低於保留圖示欄的基本規則
- 對手：特異度不夠時空的 `content` 勝出，勾號永遠不顯示（引用："or the empty content wins and the check mark never shows."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：「顯示格線」明明已開啟，選單裡卻沒有勾。
%% line-end %%

### 細節（不索引）
- 對手組：層疊覆蓋不符意圖
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:menu:9" %%
## 選單列對齊用固定寬的前導欄加 `margin-inline-start: auto`，不用 subgrid
- 做法：項目設 `display: flex`，`::before` 是固定寬度的圖示／勾號欄，快捷鍵或子選單指示放在 `margin-inline-start: auto` 的 `.hint`
- 對手：用 subgrid 時，多出來的行內子元素（例如徽章）會變成自己的格線項目，版面壞掉（引用："any extra inline child (a badge, for example) becomes its own grid item and breaks the layout."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：某一項加了「新」徽章，整個選單的欄位全部錯位。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:menu:10" %%
## 選單開啟動畫要有 `@starting-style`
- 做法：開啟狀態裡寫 `@starting-style { opacity: 0; translate: ... }`；`display`、`overlay` 加入 transition，`transition-behavior: allow-discrete` 另起一行
- 對手：關閉的 popover 是 `display: none`，transition 不會從未渲染的狀態開始，沒有起始值時開啟直接跳出、只有關閉有動畫（引用："Without it the open snaps and only the close animates."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：選單收起時會淡出，打開時卻啪一下出現。
%% line-end %%

### 細節（不索引）
- 對手組：尺寸動畫只能跳變
- 支援狀態：@starting-style：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 5 個糾錯提醒未拆：明寫 `role="menu"`／`menuitem` 會擋住 focusgroup 推斷；選單放在觸發鈕正後方以免出現隱式 `aria-details`；子選單觸發項目不要同時執行指令；指標操作後還原焦點要 `focus({ focusVisible: false })`，否則出現鍵盤焦點框；關閉後觸發鈕只在 `:focus-visible` 時顯示作用中樣式
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
