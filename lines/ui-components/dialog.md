---
guide: dialog
category: ui-components
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-components/dialog.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 對話框

%% line-start id="mwg:dialog" %%
## 用原生 `<dialog>` 的 `showModal()`，不手寫焦點陷阱、inert 與 Esc
- 做法：阻斷式的確認、表單、登入用 `<dialog>` 以 `command="show-modal"` 或 `showModal()` 開啟；不加 `role="dialog"`、`aria-modal`、焦點陷阱、`inert` 切換或 Esc 處理
- 對手：指南只說自製浮層得手工重建這些行為，沒說重建版在哪個時刻出錯（引用："It provides the accessibility semantics, focus handling, top-layer rendering and `Esc` handling that custom overlays have to rebuild by hand."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：每個專案都有一份自己的 modal 元件，各自漏掉不同的東西。原生 dialog 把這一整包交給瀏覽器。
%% line-end %%

### 細節（不索引）
- 對手組：手寫焦點管理
- 支援狀態：<dialog> 本身：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 交叉核對仲裁：解鎖改為缺

%% line-start id="mwg:dialog:2" %%
## 模態框的背景捲動用 `overscroll-behavior` 擋，不鎖 `<body>`
- 做法：`dialog:modal` 設 `overscroll-behavior: contain`；`dialog::backdrop` 設 `overflow: hidden` 加 `overscroll-behavior: contain`（細節見 `mwg:prevent-page-scroll-under-modal-dialog`）
- 對手：沒有這兩條，在背景上或對話框內捲動會捲到後面的頁面；用 `overflow: hidden` 或 `position: fixed` 鎖根元素則會拿掉捲軸、讓版面橫移（引用："without them, scrolling over the backdrop or inside the dialog scrolls the page behind it"）
- 退路：失去主要好處——不支援時背景仍會捲動，失去捲動 containment
- 解鎖：模態對話框可用純 CSS 阻止背景捲動，不必鎖根元素

經過：確認刪除的框開著，手指一滑，後面的列表捲走了。
%% line-end %%

### 細節（不索引）
- 對手組：原生捲動手勢不合用途
- 支援狀態：overscroll-behavior：Limited availability，Supported by: Chrome 144, Edge 144, Firefox 150；Unsupported in: Safari
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：同 `mwg:prevent-page-scroll-under-modal-dialog`：所有模態框（燈箱、確認、表單）都能純 CSS 鎖背景捲動，不再有版面跳動
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:dialog:3" %%
## 讓使用者邊開邊用頁面的面板用 `<dialog popover>`，不用 `showModal()`
- 做法：尋找列、檢視器、調色盤、撰寫窗格這類「開著也要繼續操作頁面」的對話框，用 `<dialog popover>`（`auto` 會點外面關閉、`manual` 不會），並放一顆可見的關閉鈕；選單、提示、懸停卡則用帶 `popover` 的語意元素，不用 `<dialog>`
- 對手：用 `showModal()` 開這類面板會擋住整個頁面（引用："**DON'T** use `showModal()`, which blocks the page."）
- 退路：保住主要行為——不支援 popover 時載入 polyfill，保留非模態頂層面板
- 解鎖：（缺）

經過：開了「尋找」想邊找邊點結果，結果頁面全被鎖住，只能先關掉對話框。
%% line-end %%

### 細節（不索引）
- 對手組：用錯原生控制項
- 支援狀態：Popover：Baseline Newly available（2025-01-27 起）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 交叉核對仲裁：解鎖改為缺

%% line-start id="mwg:dialog:4" %%
## 讀完 `returnValue` 就重設成空字串
- 做法：在 `close` 監聽裡讀 `dialog.returnValue` 判斷按了哪顆，讀完設 `dialog.returnValue = ''`，把空字串當成「沒選就關」
- 對手：Esc 與其他關閉要求不設值，瀏覽器對是否清掉上一次的值又不一致，舊值會漏到這一次（引用："browsers differ on whether they clear the previous one, so without the reset a stale value can leak."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：上次按了「刪除」，這次按 Esc 關掉，程式卻又刪了一筆。
%% line-end %%

### 細節（不索引）
- 對手組：生命週期假設錯
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:dialog:5" %%
## 攔下關閉時，要讓使用者知道對話框為什麼還開著
- 做法：`cancel` 被 `preventDefault()` 時顯示一段可見訊息，並由接到焦點的控制項（例如「捨棄」）用 `aria-describedby` 指向它
- 對手：沒有這段描述時，焦點移到新按鈕只會唸出按鈕名稱（引用："Without it, focus moving to a new button announces only that button's name."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：按 Esc 沒關掉，讀屏只說「捨棄，按鈕」，使用者不懂發生了什麼。
%% line-end %%

### 細節（不索引）
- 對手組：播報時機或可靠度出錯
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:dialog:6" %%
## 出現確認訊息時，不要讓按鈕移到游標底下
- 做法：訊息空間預先保留（用 `visibility` 隱藏，不用 `display` 或 `hidden`）；破壞性按鈕加在現有按鈕不會移動的位置
- 對手：版面一變，第二下點在同一個位置就會按到「捨棄」，丟掉使用者的修改（引用："so a second click at the same spot cannot discard the user's changes."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：連點兩下「取消」，第二下剛好落在新冒出來的「捨棄變更」上。
%% line-end %%

### 細節（不索引）
- 對手組：動作被意外觸發
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:dialog:7" %%
## 不要無條件在 `dialog` 上設 `display`
- 做法：版面用的 `display` 寫在 `dialog[open]` 上
- 對手：直接設在 `dialog` 會蓋掉關閉狀態（引用："It overrides the closed state. Scope it with `dialog[open]`."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：為了排版寫了 `dialog { display: flex }`，對話框從頁面載入起就一直開著。
%% line-end %%

### 細節（不索引）
- 對手組：層疊覆蓋不符意圖
- 支援狀態：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:dialog:8" %%
## 未存修改的保護寫在 `cancel` 裡，不能只靠 `closedby="none"`
- 做法：表單有未存修改時設 `closedby="none"`，同時在 `cancel` 監聽裡擋下並顯示確認；取消鈕用 `command="request-close"` 或 `requestClose()`
- 對手：不支援 `closedby` 的瀏覽器會忽略 `closedby="none"`，按 Esc 照樣觸發 `cancel` 並關閉對話框（引用："`closedby="none"` is ignored the same way: `Esc` fires `cancel` and then closes the dialog."）
- 退路：保住主要行為——不支援 `closedby` 時由 `cancel` 監聽攔下關閉，仍保護未存修改
- 解鎖：（缺）

經過：在 Safari 填了一半的長表單，順手按了 Esc，全部消失。
%% line-end %%

### 細節（不索引）
- 對手組：沒防護不支援的瀏覽器
- 支援狀態：<dialog closedby>：Limited availability，Supported by: Chrome 134, Edge 134, Firefox 141；Unsupported in: Safari
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 3 個糾錯提醒未拆：不要依賴 `preventDefault()` 擋下沒有使用者啟用的連續 Esc；popover polyfill 的 `:popover-open` 要用 `:is()` 合併（同 `mwg:declarative-dialog-popover-control:4`）；Invoker Commands polyfill 只在偵測不到時載入
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 交叉核對仲裁：解鎖改為缺；2026-11-18 對手組由「新功能的副作用」改為「沒防護不支援的瀏覽器」
