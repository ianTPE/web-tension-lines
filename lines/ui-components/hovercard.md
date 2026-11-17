---
guide: hovercard
category: ui-components
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-components/hovercard.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 互動式懸停卡片

%% line-start id="mwg:hovercard" %%
## 用 `interestfor` 讓連結在 hover 與聚焦時都叫出預覽卡
- 做法：觸發連結加 `interestfor="卡片 id"`，卡片設 `popover="hint"`；用 `interest-delay` 調整開關延遲，已有卡片開著時以 `:root:has(:interest-source)` 把開啟延遲設成 0
- 對手：指南沒說舊做法哪裡壞，只說這樣能確保卡片在 hover 與聚焦時都出現（引用："This ensures the card appears on both hover and focus."）
- 退路：保住主要行為——不支援時載入 `interestfor` polyfill，保留 hover 與聚焦預覽
- 解鎖：`interestfor` 可讓同一張預覽卡隨 hover 或鍵盤焦點開啟

經過：連結預覽卡以前大多只聽 mouseover，鍵盤使用者看不到。宣告一個屬性，hover 和 Tab 都會叫出同一張卡，延遲也交給 CSS。
%% line-end %%

### 細節（不索引）
- 對手組：只能 hover 才看得到
- 支援狀態：Interest invokers：Limited availability，Supported by: Chrome 149, Edge 149；Unsupported in: Firefox, Safari
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前預覽卡要自己寫 hover、focus、延遲與關閉計時 → 現在維基式的詞條預覽、使用者名片、引用文獻預覽可以宣告式做出，鍵盤一樣叫得出。原生僅 Chromium，其他靠 polyfill
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:hovercard:2" %%
## 預覽卡用 `popover="hint"`，不會把已開的選單關掉
- 做法：卡片容器設 `popover="hint"`
- 對手：用一般 popover 時，叫出預覽卡會關掉其他已開的 popover 選單（引用："Use `hint` to avoid closing unrelated popover menus that may be open."）
- 退路：保住主要行為——不支援 `hint` 時退回 manual，須在失去 interest 時自行關閉
- 解鎖：`popover="hint"` 可開啟預覽卡而不關掉其他選單

經過：選單開著，滑鼠經過某個連結，預覽卡一出來選單就收起來了。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：popover="hint"：Limited availability，Supported by: Chrome 151, Edge 151, Firefox 153；Unsupported in: Safari
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前提示層和選單會互相關掉 → 現在工具列選單開著時也能看各項的說明卡、表格篩選面板開著時也能預覽欄位定義。Safari 尚未支援
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:hovercard:3" %%
## 提示內容和觸發元素名稱相同時，什麼 ARIA 都不加
- 做法：比對正規化後的提示文字與觸發元素的可及名稱，相同就不加描述
- 對手：描述與名稱一樣時會被唸兩次（引用："A description identical to the name would be read twice."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：「粗體，按鈕，粗體」。
%% line-end %%

### 細節（不索引）
- 對手組：播報過量
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:hovercard:4" %%
## 會導覽或執行動作的觸發元素不加 `aria-expanded`
- 做法：觸發連結或有自己動作的按鈕，提示卡設 `role="tooltip"`、觸發元素用 `aria-describedby`；只有「按下就是打開提示」的按鈕才用 `aria-expanded`
- 對手：觸發元素被唸成「已收合」會暗示按 Enter 會展開，但 Enter 其實是導覽或執行動作（引用："A trigger announced as "collapsed" suggests `Enter` would expand it, but `Enter` navigates or acts."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：讀屏使用者以為按 Enter 會展開預覽，結果直接跳到別頁。
%% line-end %%

### 細節（不索引）
- 對手組：語意結構失真
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:hovercard:5" %%
## 當作描述暴露的提示，只能放錯過也沒關係的內容
- 做法：懸停卡只放可從其他地方取得的補充資訊；使用者需要的內容放在 toggletip 或直接寫在頁面上
- 對手：不是每個讀屏都會在瀏覽時唸描述，NVDA 的瀏覽模式就刻意略過（引用："Not every screen reader reads descriptions when moving through the page (NVDA skips them in browse mode by design)"）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：重要的限制條件只寫在懸停卡裡，NVDA 使用者完全沒聽到。
%% line-end %%

### 細節（不索引）
- 對手組：播報時機或可靠度出錯
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:hovercard:6" %%
## ARIA 屬性在 DOM 解析完就一次接好，不要等 focus、interest 或 polyfill
- 做法：寫一小段腳本，在每個瀏覽器、載入 `interestfor` polyfill 之前、DOM 解析完就掃過所有 `[interestfor]` 觸發元素補上 ARIA，並提供給後來插入的內容重跑的函式
- 對手：讀屏的瀏覽模式在任何互動之前就要讀到這些屬性，等到 focus 或 interest 才接已經太晚；polyfill 又要到 `load` 才接，也不替純文字提示加 `role="tooltip"`（引用："wiring them lazily on `focus` or `interest` is too late, and so is waiting for the polyfill"）
- 退路：保住主要行為——不支援時載入 polyfill，ARIA 仍在 DOM 解析後立即接好
- 解鎖：（缺）

經過：讀屏使用者用方向鍵讀過整頁，所有連結都沒有任何描述，因為那些屬性要等滑鼠移過去才加上。
%% line-end %%

### 細節（不索引）
- 對手組：播報時機或可靠度出錯
- 支援狀態：Interest invokers：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:hovercard:7" %%
## 同步 `aria-expanded` 要在 document 上以捕獲階段聽 `toggle`
- 做法：在 `document` 上掛一個 `capture: true` 的 `toggle` 監聽，依 popover 狀態更新所有指向它、由腳本管理的觸發元素；不從 `interest`／`loseinterest` 同步
- 對手：`toggle` 不冒泡，掛在 document 的一般監聽永遠不會觸發；而 popover 也可能被 Esc、點外面或別的觸發元素關掉（引用："`toggle` does not bubble. A bubbling listener on `document` never fires"）
- 退路：保住主要行為——不支援 popover 時載入 polyfill，仍以捕獲階段的 toggle 同步狀態
- 解鎖：（缺）

經過：提示卡已經關了，讀屏還說「已展開」。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：Popover：Baseline Newly available（2025-01-27 起）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:hovercard:8" %%
## 用錨點定位把預覽卡貼在連結下方，溢出時自動翻轉
- 做法：`interestfor` 讓觸發元素成為隱式錨點；卡片設 `position-area: block-end span-inline-end` 與 `position-try-fallbacks: flip-block, flip-inline`
- 對手：沒有錨點定位時，popover 退回瀏覽器預設的視窗置中，和觸發點分離（引用："tethered elements such as `[popover]` overlays fall back to their default user-agent placement (centered in the viewport for popovers)."）
- 退路：保住主要行為——不支援時載入錨點定位 polyfill，改用明確錨點保持貼附
- 解鎖：CSS 錨點定位可讓預覽卡貼在觸發連結旁，溢出時自動翻邊

經過：預覽卡出現在螢幕正中央，看不出是哪個連結的。錨點定位讓它長在連結底下，靠近邊緣就翻到另一側。
%% line-end %%

### 細節（不索引）
- 對手組：彈出層脫離觸發點
- 支援狀態：Anchor positioning：記 Newly（核心屬性 2026-01-13 起 Baseline）。指南寫 "Supported by: Safari 27 … Unsupported in: Chrome, Edge, and Firefox"，為群組狀態誤導，見 `lines/ui-components/app-menus.md`；本線未用 `position-visibility`
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前預覽卡要用 Floating UI 算位置 → 現在連結預覽、人名卡、註腳彈窗只寫兩行 CSS 就黏在觸發點旁並自動避開邊緣
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:hovercard:9" %%
## 不用 polyfill 時，`inset: auto` 與 `margin: 0` 要包在 `@supports` 裡
- 做法：把 `inset: auto`、`margin: 0` 與 `position-area` 一起放進 `@supports (position-area: block-end)`，必要時寫 `@supports not (...)` 的固定底部條
- 對手：不支援的瀏覽器忽略 `position-area`，但 `inset: auto` 照樣蓋掉預設置中，popover 卡在 `(0, 0)` 或疊在觸發點上（引用："leaving the popover stranded at `(0, 0)` or overlapping its trigger."）
- 退路：失去主要好處——不用 polyfill 時退回預設置中或固定底條，失去貼附觸發點
- 解鎖：（缺）

經過：在舊瀏覽器裡，所有預覽卡都擠在畫面左上角。
%% line-end %%

### 細節（不索引）
- 對手組：彈出層脫離觸發點
- 支援狀態：Anchor positioning：記 Newly（群組狀態誤導，見 `lines/ui-components/app-menus.md`）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:hovercard:10" %%
## `transition-behavior: allow-discrete` 獨立宣告在 `transition` 之後
- 做法：`transition` 列出 `opacity, transform, display, overlay`，再另起一行 `transition-behavior: allow-discrete`；進場值寫在 `@starting-style`，全部包在 `prefers-reduced-motion: no-preference` 裡
- 對手：把 `allow-discrete` 寫進簡寫，舊瀏覽器會忽略整條 transition（引用："Declare `transition-behavior: allow-discrete` as a separate property after `transition` rather than inside the `transition` shorthand so older browsers do not ignore the entire `transition` declaration."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：新瀏覽器裡卡片優雅滑出，舊瀏覽器裡連最基本的淡入都沒了。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：transition-behavior：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:hovercard:11" %%
## 預覽卡點下去後，用跨文件轉場把卡片變形成目的頁
- 做法：兩頁都 `@view-transition { navigation: auto; }`；只在 `[popover]:popover-open` 內給卡片、標題、圖片 `view-transition-name`，目的頁對應元素用同名；目的頁以 `<link rel="expect" href="#main-content" blocking="render">` 等關鍵內容解析完才渲染
- 對手：目的頁不等內容就渲染時轉場會不穩、閃爍（引用："To ensure the transition is stable and doesn't flicker, the destination page should use `blocking="render"` and `<link rel="expect">`"）
- 退路：失去主要好處——不支援時退回一般換頁，失去卡片變形成目的頁的動畫
- 解鎖：預覽卡與目的頁的同名元素可做跨文件變形轉場

經過：預覽卡上已經看到文章標題和主圖，點下去整頁一白再重新出現。名稱只掛在開著的那張卡上，不會撞名，目的頁等主內容到了才拍快照。
%% line-end %%

### 細節（不索引）
- 對手組：生命週期假設錯
- 支援狀態：Cross-document view transitions：Limited availability，Supported by: Chrome 126, Edge 126, Safari 18.2；Unsupported in: Firefox
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前「預覽」和「打開」是兩個斷開的畫面 → 現在多頁網站的文章預覽卡、商品快看卡可以點下去直接長成完整頁面，不必改成 SPA。Firefox 退回一般換頁
- 另有 1 個糾錯提醒未拆：interestfor polyfill 下 `:interest-source`、`:interest-target` 要用 `:is()` 合併類別，`interest-delay` 要透過 CSS 變數
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
