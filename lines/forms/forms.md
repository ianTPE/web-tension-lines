---
guide: forms
category: forms
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/forms/forms.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 表單

%% line-start id="mwg:forms" %%
## 次要按鈕明確寫 type="button"，不讓它預設送出表單
- 做法：表單裡的次要或輔助按鈕（顯示密碼、加一列、清除）明確設 `type="button"`；主要送出鈕維持 `type="submit"`
- 對手：`<form>` 裡的 `<button>` 預設是 `type="submit"`，沒寫 type 的輔助按鈕一按就送出表單（引用："explicitly set `type="button"` on secondary or helper buttons so they don't default to type="submit"."）
- 退路：不需要——`type` 是既有 HTML 行為，沒有退路問題
- 解鎖：（缺）

經過：使用者填到一半，按了「顯示密碼」這類輔助按鈕，整張表單就送出了。原因只是那顆按鈕沒寫 `type`，落回預設的 submit。主要送出鈕則相反，不要寫成 `type="button"`。
%% line-end %%

### 細節（不索引）
- 對手組：表單意外送出
- 支援狀態：不適用（指南全篇沒有瀏覽器支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:forms:2" %%
## 敏感資料用 POST 送，不用 GET
- 做法：送出敏感資料或會改變狀態的表單用 `method="POST"`；只有搜尋這類冪等請求用 `GET`
- 對手：用 `GET` 送敏感資料，資料會出現在瀏覽紀錄與伺服器日誌裡（引用："DON'T use `GET` for sensitive data (it exposes data in history/logs)."）
- 退路：不需要——送出方法是既有 HTML 行為，不涉及瀏覽器功能支援
- 解鎖：（缺）

經過：`GET` 把表單欄位接在網址後面，網址會留在瀏覽紀錄、伺服器與代理的存取日誌。搜尋字串無妨，身分證號、密碼就不行。
%% line-end %%

### 細節（不索引）
- 對手組：敏感資料外露
- 支援狀態：不適用（指南全篇沒有瀏覽器支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:forms:3" %%
## 單一的是／否選項用 checkbox，不用 radio
- 做法：依選項數挑控制項：單一的二元開關用 `<input type="checkbox">`，2–5 個互斥選項用 radio，6 個以上才用 `<select>`，大量或動態清單用 `<datalist>`
- 對手：單一的 radio 一旦選了就取消不掉（引用："Can be checked and unchecked with space unlike a radio button, which gets stuck once checked."）
- 退路：不需要——依選項數挑控制項是既有 HTML 用法
- 解鎖：（缺）

經過：「訂閱電子報」做成單一 radio，使用者點了之後反悔，卻沒有辦法取消。選錯控制項，行為就跟著錯。指南用一張選項數對照表，把每種情境對應到合適的原生元素。
%% line-end %%

### 細節（不索引）
- 對手組：用錯原生控制項
- 支援狀態：不適用（指南全篇沒有瀏覽器支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:forms:4" %%
## 不用 CSS 改變表單的視覺順序
- 做法：表單控制項的畫面順序與 DOM、鍵盤 Tab 順序保持一致，不用 CSS 重排
- 對手：視覺順序被 CSS 改變後，鍵盤仍按 DOM 順序移動，焦點在畫面上亂跳（引用："DON'T use CSS to visually reorder form controls away from their DOM/keyboard `Tab` order."）
- 退路：不需要——版面與 DOM 順序是作者自己的安排
- 解鎖：（缺）

經過：左到右看到的欄位，Tab 卻先跳到另一列，使用者會不知道自己正在填哪一格。
%% line-end %%

### 細節（不索引）
- 對手組：視覺順序與DOM順序脫鉤
- 支援狀態：不適用（指南全篇沒有瀏覽器支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:forms:5" %%
## 改選項不要自動送出表單
- 做法：select、radio、checkbox 改變後仍由使用者明確送出，不在 change 時自動提交
- 對手：使用者只是改一個選項，頁面就送出或切換脈絡，失去檢查與繼續填寫的機會（引用："DON'T auto-submit a form when a user changes `<select>`, radio buttons, or checkbox without an explicit submit action."）
- 退路：不需要——要不要自動送出是腳本自己的決定
- 解鎖：（缺）

經過：選到一半頁面突然跳走，尤其鍵盤用方向鍵瀏覽選項時更容易誤觸。
%% line-end %%

### 細節（不索引）
- 對手組：表單意外送出
- 支援狀態：不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:forms:6" %%
## 卡號、郵遞區號、OTP 用文字欄位加 inputmode
- 做法：識別用數字字串用 `type="text"` 與 `inputmode="numeric"`，不用 `type="number"`
- 對手：`type="number"` 帶來捲動與增減鈕問題，還會移除開頭的 0（引用："DON'T use `type="number"` for credit cards, ZIP codes, or one-time passcodes (causes UI scroll issues and removes leading zeros)."）
- 退路：不需要——`inputmode` 早已 Widely，數字鍵盤沒有退路問題
- 解鎖：以前要有數字鍵盤只能用 `type="number"`，卻多出增減鈕、還會吃掉開頭的 0；現在文字欄位加 `inputmode="numeric"` 就能只借鍵盤

經過：郵遞區號與驗證碼是識別碼，不是要做加減的數量。
%% line-end %%

### 細節（不索引）
- 對手組：用錯原生控制項
- 支援狀態：不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:forms:7" %%
## 單一值不要拆成自動跳格的多欄位
- 做法：OTP、電話、卡號用單一文字欄位；分格外觀用 CSS 呈現，不用多個自動跳格 input
- 對手：多格自動跳格妨礙自動填入、貼上與無障礙操作（引用："DON'T split a single value (such as a 6-digit OTP, phone number, or credit card) across multiple `<input>` boxes that auto-advance focus on keypress."）
- 退路：不需要——單一欄位或拆格是表單寫法，不涉及瀏覽器功能支援
- 解鎖：以前把卡號或驗證碼拆成多格，瀏覽器帶不進資料；現在單一欄位就能自動填入與整串貼上

經過：視覺上的六格不代表資料上要有六個控制項。
%% line-end %%

### 細節（不索引）
- 對手組：自動填入失效
- 支援狀態：不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:forms:8" %%
## 驗證欄位不要擋貼上或關 autocomplete
- 做法：密碼、驗證碼與其他身分驗證欄位允許貼上並保留正確 autocomplete token
- 對手：密碼管理員與系統驗證碼建議被擋住，使用者只能手打長秘密（引用："DON'T block copy-and-paste (`paste` events) or disable `autocomplete` on passwords, verification codes, or other authentication fields."）
- 退路：不需要——要不要攔截貼上是表單自己的選擇
- 解鎖：（缺）

經過：安全欄位尤其需要密碼管理員，禁止貼上只會逼使用者改用容易記的弱密碼。
%% line-end %%

### 細節（不索引）
- 對手組：自動填入失效
- 支援狀態：不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:forms:9" %%
## 錯誤樣式用 :user-invalid，不單用 :invalid
- 做法：錯誤樣式由 `:user-invalid` 觸發，原生 required 等限制仍保留
- 對手：只用 `:invalid` 會讓空的必填欄位在使用者互動前就被標成錯（引用："DON'T use the raw `:invalid` CSS pseudo-class alone for error styling to ensure empty required fields are not marked as invalid before the user interacts with the form."）
- 退路：不需要——錯誤樣式用哪個偽類是既有 CSS 用法
- 解鎖：以前只有 `:invalid`，空欄位一開頁就被標成錯；現在能用 `:user-invalid` 在使用者互動後才標記

經過：頁面剛打開就整片紅，會讓還沒填的人以為自己已經做錯。
%% line-end %%

### 細節（不索引）
- 對手組：播報時機或可靠度出錯
- 支援狀態：不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:forms:10" %%
## 不要停用送出鈕來阻止驗證
- 做法：送出鈕保持可按，讓使用者送出後看到錯誤；只有有效送出後才暫停以避免雙重提交
- 對手：停用送出鈕讓使用者無法觸發驗證，也不知道哪些欄位需要修正（引用："DON'T disable submit buttons to block validation; let users submit and highlight errors."）
- 退路：不需要——送出鈕要不要停用是表單自己的行為
- 解鎖：（缺）

經過：灰色按鈕只說不能送，沒說原因；讓原生驗證把問題指出來。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:forms:11" %%
## 不要每打一個字就驗證並播報錯誤
- 做法：在 submit 或 blur 時驗證；input 時只清除已修正的錯誤，不逐字觸發 aria-live
- 對手：使用者還在輸入就不斷看到錯誤、聽到播報，形成干擾（引用："DON'T trigger validation errors or `aria-live` error announcements on every keystroke while the user is typing"）
- 退路：不需要——驗證時機由腳本決定
- 解鎖：（缺）

經過：email 還沒打完一定是無效格式，逐字檢查只是在懲罰正常輸入過程。
%% line-end %%

### 細節（不索引）
- 對手組：播報過量
- 支援狀態：不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:forms:12" %%
## 表單字級至少 1rem，避免 iOS 自動放大
- 做法：控制項設 `font: inherit` 與 `font-size: max(1rem, 1em)`，保持至少 16px
- 對手：欄位字級太小會觸發 iOS 聚焦時自動縮放，打斷表單版面（引用："staying at least `1rem`(16px) to prevent iOS zoom."）
- 退路：不需要——字級設定是既有 CSS，不涉及瀏覽器功能支援
- 解鎖：（缺）

經過：手機上點一個小字輸入框，整頁突然放大，送出鈕與其他欄位因此跑出畫面。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:forms:13" %%
## 視覺隱藏控制項不用 display: none
- 做法：自訂 checkbox／radio 的原生輸入用 1px、`clip-path: inset(50%)` 的 visually-hidden 配方，不用 `display: none`
- 對手：`display: none` 會把輸入移出無障礙樹，讀屏找不到真正的控制項（引用："NOT `display: none`, which removes them from the accessibility tree."）
- 退路：不需要——視覺隱藏原生意法是既有 CSS 配方
- 解鎖：（缺）

經過：畫面上是自訂方框，鍵盤與讀屏仍操作背後的原生 input。
%% line-end %%

### 細節（不索引）
- 對手組：視覺隱藏卻仍可觸及
- 支援狀態：不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:forms:14" %%
## AJAX 表單保留 JS 失敗時的伺服器退路
- 做法：原生 form 先能送往伺服器，再用 `preventDefault()` 與 fetch 增強；JS 失敗時仍接受一般提交
- 對手：唯一提交路徑依賴 JS 時，腳本失敗會讓整張表單不能送（引用："DON'T block page submission if JS fails; ensure server-side fallback."）
- 退路：不需要——原生送出路徑是既有能力
- 解鎖：（缺）

經過：漸進增強不是保留兩套功能，而是先讓原生路徑可用，再加上較好的體驗。
%% line-end %%

### 細節（不索引）
- 對手組：自製控制項丟掉原生行為
- 支援狀態：不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:forms:15" %%
## 非作用中的精靈步驟移出 Tab 與無障礙樹
- 做法：非目前步驟用 `hidden`、`display: none` 或 `inert` 隱藏；切換時把焦點移到新步驟標題或第一欄
- 對手：舊步驟仍在 Tab 順序與無障礙樹裡，使用者會走進看不到或不該操作的欄位（引用："DON'T leave inactive wizard steps in the keyboard `Tab` order or accessibility tree"）
- 退路：不需要——隱藏步驟可用既有的 `hidden`、`display: none` 或 `inert`
- 解鎖：現在能用 `inert` 一次把非作用中的步驟移出 Tab 順序與無障礙樹

經過：畫面已是付款步驟，Tab 卻回到隱藏的帳號欄位，使用者無法判斷自己身在何處。
%% line-end %%

### 細節（不索引）
- 對手組：視覺隱藏卻仍可觸及
- 支援狀態：不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:forms:16" %%
## 多步驟表單避免手機鍵盤遮住欄位與按鈕
- 做法：聚焦欄位與主要按鈕安排在視窗上半部，或用 `scroll-padding` 保留鍵盤空間
- 對手：虛擬鍵盤升起後遮住正在輸入的欄位或下一步按鈕（引用："design layouts so that the mobile keyboard does not obscure inputs or buttons"）
- 退路：不需要——版面配置是作者自己的安排
- 解鎖：（缺）

經過：填完一欄找不到下一步，使用者只能關掉鍵盤或盲目捲動。
%% line-end %%

### 細節（不索引）
- 對手組：浮層遮住說明
- 支援狀態：不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2
