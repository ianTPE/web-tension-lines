---
guide: stack-drill-down
category: ui-components
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-components/stack-drill-down.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 堆疊式逐層深入導覽

%% line-start id="mwg:stack-drill-down" %%
## 用捲動吸附做逐層深入的堆疊，`scrollsnapchange` 統一處理所有「換頁」
- 做法：水平 `scroll-snap-type: x mandatory` 容器，每個畫面是一個吸附點（`scroll-snap-stop: always`）；深入時 `pushState`、加入新畫面、捲過去；`scrollsnapchange` 的 `snapTargetInline` 當作「目前畫面變了」的唯一來源，更新 `inert`、焦點、歷史紀錄並修剪畫面；不支援時用 IntersectionObserver（`threshold: 1`）呼叫同一個函式
- 對手：用 JS 驅動 `transform` 動畫時，畫面位置由補間決定、不是手指（引用："the snap mechanism gives the user direct gestural control of the panel's position (their finger drives it, not a tween)"）
- 退路：保住主要行為——不支援 `scrollsnapchange` 時用 IntersectionObserver 呼叫同一處理函式
- 解鎖：原生捲動吸附可做可滑回的堆疊導覽，並以吸附事件統一更新狀態

經過：手機版的設定頁一層層點進去，想用手勢滑回上一層，舊做法放手後播固定動畫、拉到一半無法反悔。改成捲動之後，畫面就在手指底下。
%% line-end %%

### 細節（不索引）
- 對手組：自製控制項丟掉原生行為
- 支援狀態：Scroll snap：Widely（2020-01-15 起）；Scroll snap events：Limited availability，Supported by: Chrome 129, Edge 129；Unsupported in: Firefox, Safari
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前像原生 app 那樣「滑回上一層」要手勢函式庫加路由同步 → 現在郵件串、檔案夾瀏覽、設定子頁、相簿詳情都能用捲動容器做出可滑回、可分享網址、支援系統返回鍵的堆疊導覽。scrollsnapchange 僅 Chromium，其他用 IntersectionObserver 補
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:stack-drill-down:2" %%
## 位移效果套在吸附目標的子元素上，不套在吸附目標本身
- 做法：`.Stack-view` 只負責吸附，視差的 `transform` 套在內層 `.Stack-viewContent`
- 對手：吸附目標上的 transform 會回饋到捲動容器的吸附幾何，手勢途中畫面亂跳（引用："A transform on the snap target feeds back into the scroll container's snap geometry and the scroller will glitch mid-gesture."）
- 退路：不需要——支援狀態為 Widely 或不適用，不必退路
- 解鎖：（缺）

經過：加了視差之後，滑到一半畫面突然跳一下，停在兩層之間。
%% line-end %%

### 細節（不索引）
- 對手組：互動中畫面抖動
- 支援狀態：結構做法，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:stack-drill-down:3" %%
## 除了目前畫面，堆疊裡其他畫面都加 `inert`
- 做法：在 `scrollsnapchange` 處理函式裡，對目前畫面以外的每一層 `toggleAttribute('inert', true)`
- 對手：藏在視差後面的畫面仍可被 Tab 與讀屏走到，明眼人看不出來（引用："Without this, focus and screen-reader navigation leak into views hidden behind the parallax — invisible to sighted users but a severe accessibility failure."）
- 退路：不需要——支援狀態為 Widely 或不適用，不必退路
- 解鎖：（缺）

經過：在第三層按 Tab，焦點跑到被蓋住的第一層清單裡，鍵盤使用者完全不知道自己在哪。
%% line-end %%

### 細節（不索引）
- 對手組：視覺隱藏卻仍可觸及
- 支援狀態：inert：Baseline Widely available（2023-04-11 起）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:stack-drill-down:4" %%
## 讓瀏覽器的返回鍵和畫面同步：滑回時 `history.go()`、深層連結補一個根項目、`popstate` 裡不 `pushState`
- 做法：每次深入 `pushState({depth})`；滑回後若目前畫面的深度與 `currentDepth` 不符，呼叫 `history.go(差值)`；從深層連結進來時，返回鈕改成 `pushState` 一個根項目並在左側插入根畫面；`popstate` 處理函式只捲動、不推新項目
- 對手：滑回後不同步歷史，下一次系統返回會把使用者帶到意料之外的地方；深層連結上直接 `history.back()` 會離開整個 app；在 `popstate` 裡 `pushState` 則讓返回鍵失效（引用："Without this, a subsequent OS Back returns the user somewhere unexpected because the browser's history cursor is out of sync with what's on screen."）
- 退路：不需要——支援狀態為 Widely 或不適用，不必退路
- 解鎖：（缺）

經過：用手勢滑回兩層，再按手機的返回鍵，結果跳回一個早就不在畫面上的頁面；從分享連結進來按返回，直接離開了網站。
%% line-end %%

### 細節（不索引）
- 對手組：平台慣用操作沒有作用
- 支援狀態：History API：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:stack-drill-down:5" %%
## 在捲動吸附容器裡還原焦點一律加 `preventScroll: true`
- 做法：還原到原本點擊的連結、或聚焦新畫面的返回鈕時，呼叫 `.focus({ preventScroll: true })`
- 對手：預設會把焦點目標捲進畫面，和吸附容器打架，使用者停在兩層之間（引用："The default `preventScroll: false` makes the browser scroll the focus target into view, which fights the snap container and can land the user mid-snap."）
- 退路：不需要——支援狀態為 Widely 或不適用，不必退路
- 解鎖：（缺）

經過：滑回上一層後焦點還原到原本的連結，畫面卻又被拉動半格，卡在兩個畫面中間。
%% line-end %%

### 細節（不索引）
- 對手組：互動中畫面抖動
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:stack-drill-down:6" %%
## 每次換畫面都確保焦點落在新畫面裡，沒有目標就聚焦內容容器
- 做法：優先還原到使用者點過的連結，其次是返回鈕；回到根畫面又沒有可還原的連結時，聚焦設了 `tabindex="-1"` 的 `.Stack-viewContent`；只在焦點原本就在堆疊裡時才移動
- 對手：焦點留在被移除或 `inert` 的畫面裡，會掉回 `<body>`，鍵盤與讀屏使用者從頁首重來（引用："Focus left in a removed or `inert` view falls to `<body>`."）
- 退路：不需要——支援狀態為 Widely 或不適用，不必退路
- 解鎖：（缺）

經過：從深層連結按返回回到首頁，下一個 Tab 卻從網站最上方的 logo 開始。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:stack-drill-down:7" %%
## 每層都更新 `document.title`，返回鈕以要回去的那層命名
- 做法：換畫面時把標題設成「目前畫面 | 應用名」，根畫面只用應用名；返回鈕的 `aria-label` 設成「Back to 上一層標題」
- 對手：每次深入都多一筆歷史，標題不變時歷史清單、分頁與讀屏分不出這些項目；只寫「Back」又讓讀屏使用者不知道自己在哪（引用："Each drill-down adds a history entry, and the title is what the browser's history list, the tab and screen readers use to tell those entries apart."）
- 退路：不需要——支援狀態為 Widely 或不適用，不必退路
- 解鎖：（缺）

經過：長按瀏覽器的返回鍵，跳出五筆一模一樣的「Mail」，不知道該選哪一筆。
%% line-end %%

### 細節（不索引）
- 對手組：語意結構失真
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:stack-drill-down:8" %%
## 多步跳轉與往前的 `popstate` 用 `behavior: 'instant'`
- 做法：`popstate` 時比較目標位置與目前位置；跨越超過一層或向右（前進）時用 `'instant'`，單步返回才用 `'auto'`
- 對手：多步跳轉若平滑捲動，每經過一個吸附點都觸發 `scrollsnapchange`，做 N 輪 inert／焦點／歷史處理；iOS Safari 又會把邊緣滑動誤當成前進，播出使用者沒要求的深入動畫（引用："Multi-step jumps would otherwise fire `scrollsnapchange` at every intermediate snap and do N rounds of inert/focus/history work."）
- 退路：不需要——支援狀態為 Widely 或不適用，不必退路
- 解鎖：（缺）

經過：在歷史清單裡直接跳回三層前，畫面一層層滑過去，焦點也跟著亂跳了三次。
%% line-end %%

### 細節（不索引）
- 對手組：工作花在看不到的地方
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:stack-drill-down:9" %%
## 平滑捲動交給 CSS 的 `scroll-behavior`，JS 一律傳 `behavior: 'auto'`
- 做法：`scroll-behavior: smooth` 只寫在 `@media (prefers-reduced-motion: no-preference)` 裡，`scrollTo`／`scrollBy` 傳 `'auto'` 讓它照 CSS 走
- 對手：在 JS 寫死 `behavior: 'smooth'` 會繞過使用者的減少動態設定（引用："Hard-coding `behavior: 'smooth'` bypasses the user's setting."）
- 退路：不需要——支援狀態為 Widely 或不適用，不必退路
- 解鎖：（缺）

經過：開了減少動態的使用者每點一層，畫面照樣整頁滑過去。
%% line-end %%

### 細節（不索引）
- 對手組：忽略使用者設定
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:stack-drill-down:10" %%
## 深入的觸發點用真的 `<a href>`，並放行修飾鍵點擊
- 做法：畫面裡用 `<a href>` 指向各層網址；點擊攔截時遇到 meta／ctrl／shift 或非左鍵就不攔，讓瀏覽器開新分頁
- 對手：用 `<button onclick>` 或 `<div>` 會失去懸停預覽網址、分享、中鍵開新分頁、讀屏角色與 SEO（引用："Real anchors get URL preview on hover, shareability, middle-click, screen-reader role, and SEO for free."）
- 退路：不需要——支援狀態為 Widely 或不適用，不必退路
- 解鎖：（缺）

經過：想把某封信用中鍵開在新分頁，結果什麼也沒發生，也沒辦法複製連結傳給同事。
%% line-end %%

### 細節（不索引）
- 對手組：自製控制項丟掉原生行為
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:stack-drill-down:11" %%
## 捲動驅動的視差整塊包在 `@supports (animation-timeline: view())`
- 做法：`animation-timeline: view(inline)`、`animation-range` 與 `@keyframes` 都放在 `@supports` 區塊內
- 對手：不支援的瀏覽器仍會解析 keyframes，把 `to` 狀態當成靜態樣式套用，每個畫面都永遠處於位移狀態（引用："Browsers without scroll-driven animations still parse the @keyframes and would apply the `to` state as a static style, leaving every view permanently transformed."）
- 退路：保住主要行為——不支援時以 `@supports` 停用視差，畫面直接切換到吸附點
- 解鎖：（缺）

經過：在舊版瀏覽器打開，每個畫面都偏了四分之三、整片變暗。
%% line-end %%

### 細節（不索引）
- 對手組：沒防護不支援的瀏覽器
- 支援狀態：Scroll-driven animations：Baseline Newly available（2026-10-27 起）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 對手組由「新功能的副作用」改為「沒防護不支援的瀏覽器」

%% line-start id="mwg:stack-drill-down:12" %%
## 視差、變暗與陰影用 `view(inline)` 時間軸跟著手指走，不用 `scroll` 監聽
- 做法：`.Stack-viewContent` 設 `animation-timeline: view(inline)`，離場階段（`exit 0% exit 100%`）播視差＋變暗，深入的畫面另加左緣陰影
- 對手：JS 的 `scroll` 監聽跑在主執行緒，手勢中會明顯掉幀（引用："a JS scroll listener runs on the main thread and will visibly drop frames during the gesture."）
- 退路：保住主要行為——不支援時停用視差與變暗，只保留直接切換吸附畫面
- 解鎖：視差、變暗與陰影可直接綁在 `view()` 時間軸，跟著手勢進度變化

經過：滑回上一層時，底下那層應該從左邊緩緩推出、慢慢變亮；用 scroll 監聽做的版本在低階手機上一卡一卡。
%% line-end %%

### 細節（不索引）
- 對手組：捲動連動效果靠JS監聽
- 支援狀態：Scroll-driven animations：Baseline Newly available（2026-10-27 起），Supported by: Chrome 115, Edge 115, Firefox 159, Safari 26
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前「卡片疊上來、底層退後變暗」要逐幀計算 → 現在任何水平分頁（設定子頁、商品詳情、聊天串）都能讓轉場效果直接綁在拖動進度上，拖一半停住效果也停在一半
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:stack-drill-down:13" %%
## 滑回後把後面已經離開的畫面從 DOM 移除，只留網址以便重建
- 做法：`scrollsnapchange` 時移除目前畫面右邊的所有畫面，`entriesByDepth` 只保留它們的網址路徑，前進時再重建
- 對手：長時間來回深入會累積幾十個脫離的子樹（引用："A long drill-down session can otherwise accumulate dozens of detached subtrees."）
- 退路：不需要——支援狀態為 Widely 或不適用，不必退路
- 解鎖：（缺）

經過：在檔案夾裡進進出出一個小時，頁面越來越慢，DOM 裡塞滿看不到的舊畫面。
%% line-end %%

### 細節（不索引）
- 對手組：工作花在看不到的地方
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:stack-drill-down:14" %%
## 堆疊容器設 `overscroll-behavior-x: none`，滑回手勢不要連到瀏覽器的上一頁
- 做法：`.Stack { overscroll-behavior-x: none; }`
- 對手：滑回手勢到底後會串到瀏覽器自己的返回手勢（iOS、部分 Android）或頁面的垂直捲動（引用："Prevent the swipe-back gesture from chaining into the browser's own history-back gesture (iOS, some Android) or the page's vertical scroll."）
- 退路：不需要——支援狀態為 Widely 或不適用，不必退路
- 解鎖：（缺）

經過：在根畫面多滑了一下，整個網站退回上一個瀏覽的網頁。
%% line-end %%

### 細節（不索引）
- 對手組：動作被意外觸發
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:stack-drill-down:15" %%
## 堆疊高度用 `100dvh`
- 做法：`.Stack { height: 100dvh; }`，跟著行動裝置網址列顯示或隱藏變化
- 對手：`svh` 在網址列動畫時會裁切，`vh` 會滲到網址列底下（引用："svh would clip during the address bar animation; vh leaks under it."）
- 退路：不需要——支援狀態為 Widely 或不適用，不必退路
- 解鎖：（缺）

經過：手機上捲到底，最下方的按鈕藏在網址列後面點不到。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：dvh：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 註：與 `mwg:navigation-drawer:6`（抽屜用 `svh`，避免滑動中高度跳動）方向相反；兩份指南針對的元件不同，各照原文
- 另有 3 個糾錯提醒未拆：偵測 `onscrollsnapchange` 要查 `HTMLElement.prototype` 而非 `window`；IntersectionObserver 退路要過濾 `intersectionRatio === 1` 的進場項目；初始化時用 `'instant'` 捲動避免首次繪製播視差
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
