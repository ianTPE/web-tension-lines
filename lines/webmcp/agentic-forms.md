---
guide: agentic-forms
category: webmcp
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/webmcp/agentic-forms.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 給代理用的表單

%% line-start id="mwg:agentic-forms" %%
## 用 `toolname`／`tooldescription` 把一般 `<form>` 變成代理可呼叫的 WebMCP 工具
- 做法：在 `<form>` 加 `toolname` 與 `tooldescription`（說做什麼、何時用，不列欄位）；欄位說明預設取自 `<label>`，需要時用 `toolparamdescription` 補範例值，選項群組放在 `<fieldset>` 上；送出處理器檢查 `event.agentInvoked`，用 `event.respondWith(promise)` 把驗證錯誤或結果直接交回代理、不跳頁；Angular Signal Forms 改用框架提供的整合
- 對手：缺——指南只說瀏覽器會從表單欄位合成 JSON Schema 並處理代理互動，沒說沒有這些屬性時代理在哪個時刻出問題
- 退路：不需要——指南說這組屬性可以安全地用，不支援的瀏覽器會直接忽略 `tool*` 屬性
- 解鎖：以前要讓代理操作網站得另寫一套 API 或頁內腳本；現在一般 `<form>` 加兩個屬性，瀏覽器就把它描述成代理可呼叫的工具

經過：找車網站的搜尋表單已經有完整的標籤與必填設定。加上兩個屬性，瀏覽器就能把它描述成一個帶參數的工具，代理填完送出後直接拿到搜尋結果。
%% line-end %%

### 細節（不索引）
- 對手組：頁面功能對代理不透明
- 支援狀態：Form-associated WebMCP attributes："not natively supported by any major browser yet"（`webmcp` 指南另說 Chromium 146 起可用旗標預覽）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前要讓代理操作網站得另寫一套 API → 現在搜尋、篩選、查庫存這類現成表單加幾個屬性，就成為瀏覽器內代理可呼叫、還能回傳結果的工具。目前沒有瀏覽器原生支援，只有 Chromium 旗標預覽
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:agentic-forms:2" %%
## 不可逆、金流、對外發送與帳號設定的表單不加 `toolautosubmit`
- 做法：只在唯讀查詢（搜尋、篩選、查狀態）與低風險可復原的動作（加入購物車、套用折扣碼、存草稿）加 `toolautosubmit`；刪除、結帳、轉帳、寄信、發布、改密碼或權限的表單省略它
- 對手：有 `toolautosubmit` 時，代理可以不等使用者互動就送出表單（引用："`toolautosubmit`: (Optional) If present, the agent can submit the form without waiting for user interaction."）
- 退路：不需要——不支援的瀏覽器會忽略這些屬性，代理本來就無法代送，無從退路
- 解鎖：（缺）

經過：帳號頁的「刪除帳號」表單被一併加上自動送出，代理理解錯一句話就可能直接按下去。拿掉後，代理只能填好欄位，最後一下留給使用者。
%% line-end %%

### 細節（不索引）
- 對手組：表單意外送出
- 支援狀態：Form-associated WebMCP attributes："not natively supported by any major browser yet"
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:agentic-forms:3" %%
## Angular Signal Forms 用 `experimentalWebMcpTool` 選項，不再加 `toolname`
- 做法：用 `@angular/forms/signals` 的 `form()` 建的表單，不加 `toolname`／`tooldescription`；改在 app providers 加 `provideExperimentalWebMcpForms()`，並把 `experimentalWebMcpTool: { name, description }` 傳給 `form()`，由 Angular 從 signal 模型建 schema 並接上驗證與送出
- 對手：兩種做法同時用，同一張表單被註冊兩次（引用："Using both approaches registers the same form twice."）
- 退路：不需要——不支援的瀏覽器會忽略 `tool*` 屬性與框架整合，Angular 表單本身照常運作
- 解鎖：（缺）

經過：Angular 專案照 HTML 範例在模板上加了 `toolname`，又在 `form()` 開了 WebMCP 選項，代理看到兩個一樣的工具。
%% line-end %%

### 細節（不索引）
- 對手組：兩套機制重複作用
- 支援狀態：Form-associated WebMCP attributes："not natively supported by any major browser yet"
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 對手組由「新功能的副作用」改為「兩套機制重複作用」

%% line-start id="mwg:agentic-forms:4" %%
## 欄位互相連動、自訂元件或多步驟的表單不用宣告式 API
- 做法：宣告式 API 只用在自成一體的標準表單；欄位選項或可見性依其他欄位變化、依賴 canvas 或富文字編輯器等不會自動序列化的元件、需要多次送出的精靈流程，改用命令式 API 或一般 DOM 互動
- 對手：合成出來的 schema 表達不了欄位間的相依；自訂元件的值不會自動序列化（引用："The synthesized schema cannot express these dependencies well."）
- 退路：不需要——不支援的瀏覽器忽略 `tool*` 屬性，這些表單本來就走一般 DOM 互動
- 解鎖：（缺）

經過：機票表單選了「單程」才會隱藏回程日期，宣告式 API 產生的 schema 卻把兩個日期都列成獨立參數，代理照填，表單狀態對不上。
%% line-end %%

### 細節（不索引）
- 對手組：表單假設錯的資料格式
- 支援狀態：Form-associated WebMCP attributes："not natively supported by any major browser yet"
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:agentic-forms:5" %%
## `toolactivated`／`toolcancel` 先偵測該掛在 `document.modelContext` 還是 `window`
- 做法：監聽代理開始與取消執行工具的 `toolactivated`、`toolcancel` 事件時，先檢查 `document.modelContext` 上有沒有 `on<type>` 屬性，有就掛在它上面，否則掛在 `window`
- 對手：Chrome 156 起事件改在 `document.modelContext` 上派送，舊版在 `window`，只掛一邊會在另一種版本收不到（引用："Starting in Chrome 156, these events are dispatched on `document.modelContext`. Older versions dispatch them on `window`."）
- 退路：不需要——不支援的瀏覽器不會派送這兩個事件，本來就沒有掛載的問題
- 解鎖：（缺）

經過：照舊範例在 `window` 上聽 `toolactivated`，升級瀏覽器後顯示「代理操作中」的提示再也沒出現過。
%% line-end %%

### 細節（不索引）
- 對手組：功能偵測不可靠
- 支援狀態：Form-associated WebMCP attributes："not natively supported by any major browser yet"
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:agentic-forms:6" %%
## 用 `:tool-form-active`／`:tool-submit-active` 標出代理正在操作的表單與待確認的送出鈕
- 做法：`form:tool-form-active` 標示代理正在使用的表單；`button:tool-submit-active` 標示省略 `toolautosubmit` 時、瀏覽器暫停等使用者檢查的送出按鈕（例如虛線外框加脈動動畫）
- 對手：缺——指南只說用這兩個虛擬類別在代理互動時標亮表單，沒說不標示時在哪個時刻出問題
- 退路：不需要——不支援的瀏覽器不會套用這兩個虛擬類別，樣式放著即可
- 解鎖：以前代理在背景填表單，使用者看不出它動了哪裡；現在可用虛擬類別標出代理正在用的表單與待確認的送出鈕

經過：代理在背景替使用者填訂房表單，使用者只看到欄位一個個自己變了。加上虛擬類別後，表單有框線標示，最後的送出鈕在閃，提醒輪到人確認。
%% line-end %%

### 細節（不索引）
- 對手組：焦點或狀態指示消失
- 支援狀態：Form-associated WebMCP attributes："not natively supported by any major browser yet"
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前代理操作頁面時使用者看不出它動了哪裡 → 現在可以做「代理代填、人來按送出」的交接介面：被代理使用的表單整塊標亮，等待確認的按鈕用動畫提醒。目前沒有瀏覽器原生支援
- 另有 1 個糾錯提醒未拆：`tooldescription` 與 `toolparamdescription` 不重複列出欄位、選項與限制（瀏覽器已從表單控制項產生）
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
