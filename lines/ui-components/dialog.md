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
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：阻斷式的確認、表單、登入用 `<dialog>` 以 `command="show-modal"` 或 `showModal()` 開啟；不加 `role="dialog"`、`aria-modal`、焦點陷阱、`inert` 切換或 Esc 處理
- 被什麼擋：指南只說自製浮層得手工重建這些行為，沒說重建版在哪個時刻出錯（引用："It provides the accessibility semantics, focus handling, top-layer rendering and `Esc` handling that custom overlays have to rebuild by hand."）
- 戰報：勝——瀏覽器提供背景 inert、焦點圍堵、頂層、`::backdrop`、Esc 與返回手勢關閉、關閉後焦點還給觸發者（官方宣稱）

經過：每個專案都有一份自己的 modal 元件，各自漏掉不同的東西。原生 dialog 把這一整包交給瀏覽器。
%% line-end %%

### 細節（不索引）
- 對手組：手寫焦點管理
- 支援狀態：<dialog> 本身：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:dialog:2" %%
## 模態框的背景捲動用 `overscroll-behavior` 擋，不鎖 `<body>`
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`dialog:modal` 設 `overscroll-behavior: contain`；`dialog::backdrop` 設 `overflow: hidden` 加 `overscroll-behavior: contain`（細節見 `mwg:prevent-page-scroll-under-modal-dialog`）
- 被什麼擋：沒有這兩條，在背景上或對話框內捲動會捲到後面的頁面；用 `overflow: hidden` 或 `position: fixed` 鎖根元素則會拿掉捲軸、讓版面橫移（引用："without them, scrolling over the backdrop or inside the dialog scrolls the page behind it"）
- 戰報：部分改善——支援的瀏覽器完全擋住背景捲動；Safari 只在對話框內容溢出時擋得住，且這個行為無法偵測（官方宣稱）

經過：確認刪除的框開著，手指一滑，後面的列表捲走了。
%% line-end %%

### 細節（不索引）
- 對手組：原生捲動手勢不合用途
- 支援狀態：overscroll-behavior：Limited availability，Supported by: Chrome 144, Edge 144, Firefox 150；Unsupported in: Safari
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：同 `mwg:prevent-page-scroll-under-modal-dialog`：所有模態框（燈箱、確認、表單）都能純 CSS 鎖背景捲動，不再有版面跳動
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:dialog:3" %%
## 讓使用者邊開邊用頁面的面板用 `<dialog popover>`，不用 `showModal()`
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：尋找列、檢視器、調色盤、撰寫窗格這類「開著也要繼續操作頁面」的對話框，用 `<dialog popover>`（`auto` 會點外面關閉、`manual` 不會），並放一顆可見的關閉鈕；選單、提示、懸停卡則用帶 `popover` 的語意元素，不用 `<dialog>`
- 被什麼擋：用 `showModal()` 開這類面板會擋住整個頁面（引用："**DON'T** use `showModal()`, which blocks the page."）
- 戰報：部分改善——面板在頂層、頁面保持可操作且不被 inert；Popover 為 Newly（官方宣稱）

經過：開了「尋找」想邊找邊點結果，結果頁面全被鎖住，只能先關掉對話框。
%% line-end %%

### 細節（不索引）
- 對手組：用錯原生控制項
- 支援狀態：Popover：Baseline Newly available（2025-01-27 起）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:dialog:4" %%
## 讀完 `returnValue` 就重設成空字串
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在 `close` 監聽裡讀 `dialog.returnValue` 判斷按了哪顆，讀完設 `dialog.returnValue = ''`，把空字串當成「沒選就關」
- 被什麼擋：Esc 與其他關閉要求不設值，瀏覽器對是否清掉上一次的值又不一致，舊值會漏到這一次（引用："browsers differ on whether they clear the previous one, so without the reset a stale value can leak."）
- 戰報：勝——每次關閉都只看到這一次的選擇（官方宣稱）

經過：上次按了「刪除」，這次按 Esc 關掉，程式卻又刪了一筆。
%% line-end %%

### 細節（不索引）
- 對手組：生命週期假設錯
- 支援狀態：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:dialog:5" %%
## 攔下關閉時，要讓使用者知道對話框為什麼還開著
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`cancel` 被 `preventDefault()` 時顯示一段可見訊息，並由接到焦點的控制項（例如「捨棄」）用 `aria-describedby` 指向它
- 被什麼擋：沒有這段描述時，焦點移到新按鈕只會唸出按鈕名稱（引用："Without it, focus moving to a new button announces only that button's name."）
- 戰報：勝——讀屏在焦點移過去時一併唸出原因（官方宣稱）

經過：按 Esc 沒關掉，讀屏只說「捨棄，按鈕」，使用者不懂發生了什麼。
%% line-end %%

### 細節（不索引）
- 對手組：播報時機或可靠度出錯
- 支援狀態：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:dialog:6" %%
## 出現確認訊息時，不要讓按鈕移到游標底下
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：訊息空間預先保留（用 `visibility` 隱藏，不用 `display` 或 `hidden`）；破壞性按鈕加在現有按鈕不會移動的位置
- 被什麼擋：版面一變，第二下點在同一個位置就會按到「捨棄」，丟掉使用者的修改（引用："so a second click at the same spot cannot discard the user's changes."）
- 戰報：勝——按鈕不位移，重複點擊不會誤按破壞性動作（官方宣稱）

經過：連點兩下「取消」，第二下剛好落在新冒出來的「捨棄變更」上。
%% line-end %%

### 細節（不索引）
- 對手組：動作被意外觸發
- 支援狀態：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:dialog:7" %%
## 不要無條件在 `dialog` 上設 `display`
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：版面用的 `display` 寫在 `dialog[open]` 上
- 被什麼擋：直接設在 `dialog` 會蓋掉關閉狀態（引用："It overrides the closed state. Scope it with `dialog[open]`."）
- 戰報：勝——關閉的對話框保持隱藏（官方宣稱）

經過：為了排版寫了 `dialog { display: flex }`，對話框從頁面載入起就一直開著。
%% line-end %%

### 細節（不索引）
- 對手組：層疊覆蓋不符意圖
- 支援狀態：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:dialog:8" %%
## 未存修改的保護寫在 `cancel` 裡，不能只靠 `closedby="none"`
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：表單有未存修改時設 `closedby="none"`，同時在 `cancel` 監聽裡擋下並顯示確認；取消鈕用 `command="request-close"` 或 `requestClose()`
- 被什麼擋：不支援 `closedby` 的瀏覽器會忽略 `closedby="none"`，按 Esc 照樣觸發 `cancel` 並關閉對話框（引用："`closedby="none"` is ignored the same way: `Esc` fires `cancel` and then closes the dialog."）
- 戰報：部分改善——`cancel` 裡的保護在所有瀏覽器都有效；`closedby` 為 Limited（官方宣稱）

經過：在 Safari 填了一半的長表單，順手按了 Esc，全部消失。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：<dialog closedby>：Limited availability，Supported by: Chrome 134, Edge 134, Firefox 141；Unsupported in: Safari
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 另有 3 個糾錯提醒未拆：不要依賴 `preventDefault()` 擋下沒有使用者啟用的連續 Esc；popover polyfill 的 `:popover-open` 要用 `:is()` 合併（同 `mwg:declarative-dialog-popover-control:4`）；Invoker Commands polyfill 只在偵測不到時載入
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
