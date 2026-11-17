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
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：表單裡的次要或輔助按鈕（顯示密碼、加一列、清除）明確設 `type="button"`；主要送出鈕維持 `type="submit"`
- 被什麼擋：`<form>` 裡的 `<button>` 預設是 `type="submit"`，沒寫 type 的輔助按鈕一按就送出表單（引用："explicitly set `type="button"` on secondary or helper buttons so they don't default to type="submit"."）
- 戰報：勝——明確標成 `button` 後，輔助按鈕只做自己的事，不觸發送出（官方宣稱）

經過：使用者填到一半，按了「顯示密碼」這類輔助按鈕，整張表單就送出了。原因只是那顆按鈕沒寫 `type`，落回預設的 submit。主要送出鈕則相反，不要寫成 `type="button"`。
%% line-end %%

### 細節（不索引）
- 對手組：表單意外送出
- 支援狀態：不適用（指南全篇沒有瀏覽器支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:forms:2" %%
## 敏感資料用 POST 送，不用 GET
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：送出敏感資料或會改變狀態的表單用 `method="POST"`；只有搜尋這類冪等請求用 `GET`
- 被什麼擋：用 `GET` 送敏感資料，資料會出現在瀏覽紀錄與伺服器日誌裡（引用："DON'T use `GET` for sensitive data (it exposes data in history/logs)."）
- 戰報：勝——改用 `POST`，資料放在請求本文，不進網址（官方宣稱）

經過：`GET` 把表單欄位接在網址後面，網址會留在瀏覽紀錄、伺服器與代理的存取日誌。搜尋字串無妨，身分證號、密碼就不行。
%% line-end %%

### 細節（不索引）
- 對手組：敏感資料外露
- 支援狀態：不適用（指南全篇沒有瀏覽器支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:forms:3" %%
## 單一的是／否選項用 checkbox，不用 radio
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：依選項數挑控制項：單一的二元開關用 `<input type="checkbox">`，2–5 個互斥選項用 radio，6 個以上才用 `<select>`，大量或動態清單用 `<datalist>`
- 被什麼擋：單一的 radio 一旦選了就取消不掉（引用："Can be checked and unchecked with space unlike a radio button, which gets stuck once checked."）
- 戰報：勝——checkbox 可以用空白鍵勾選與取消，狀態可逆（官方宣稱）

經過：「訂閱電子報」做成單一 radio，使用者點了之後反悔，卻沒有辦法取消。選錯控制項，行為就跟著錯。指南用一張選項數對照表，把每種情境對應到合適的原生元素。
%% line-end %%

### 細節（不索引）
- 對手組：用錯原生控制項
- 支援狀態：不適用（指南全篇沒有瀏覽器支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:forms:4" %%
## 不用 CSS 改變表單的視覺順序
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：表單控制項的畫面順序與 DOM、鍵盤 Tab 順序保持一致，不用 CSS 重排
- 被什麼擋：視覺順序被 CSS 改變後，鍵盤仍按 DOM 順序移動，焦點在畫面上亂跳（引用："DON'T use CSS to visually reorder form controls away from their DOM/keyboard `Tab` order."）
- 戰報：勝——焦點移動順序與看到的表單順序一致（官方宣稱）

經過：左到右看到的欄位，Tab 卻先跳到另一列，使用者會不知道自己正在填哪一格。
%% line-end %%

### 細節（不索引）
- 對手組：視覺順序與DOM順序脫鉤
- 支援狀態：不適用（指南全篇沒有瀏覽器支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

%% line-start id="mwg:forms:5" %%
## 改選項不要自動送出表單
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：select、radio、checkbox 改變後仍由使用者明確送出，不在 change 時自動提交
- 被什麼擋：使用者只是改一個選項，頁面就送出或切換脈絡，失去檢查與繼續填寫的機會（引用："DON'T auto-submit a form when a user changes `<select>`, radio buttons, or checkbox without an explicit submit action."）
- 戰報：勝——送出行為只由明確動作觸發（官方宣稱）

經過：選到一半頁面突然跳走，尤其鍵盤用方向鍵瀏覽選項時更容易誤觸。
%% line-end %%

### 細節（不索引）
- 對手組：表單意外送出
- 支援狀態：不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

%% line-start id="mwg:forms:6" %%
## 卡號、郵遞區號、OTP 用文字欄位加 inputmode
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：識別用數字字串用 `type="text"` 與 `inputmode="numeric"`，不用 `type="number"`
- 被什麼擋：`type="number"` 帶來捲動與增減鈕問題，還會移除開頭的 0（引用："DON'T use `type="number"` for credit cards, ZIP codes, or one-time passcodes (causes UI scroll issues and removes leading zeros)."）
- 戰報：勝——行動裝置仍有數字鍵盤，原始字串不變（官方宣稱）

經過：郵遞區號與驗證碼是識別碼，不是要做加減的數量。
%% line-end %%

### 細節（不索引）
- 對手組：用錯原生控制項
- 支援狀態：不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

%% line-start id="mwg:forms:7" %%
## 單一值不要拆成自動跳格的多欄位
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：OTP、電話、卡號用單一文字欄位；分格外觀用 CSS 呈現，不用多個自動跳格 input
- 被什麼擋：多格自動跳格妨礙自動填入、貼上與無障礙操作（引用："DON'T split a single value (such as a 6-digit OTP, phone number, or credit card) across multiple `<input>` boxes that auto-advance focus on keypress."）
- 戰報：勝——完整值可在單一欄位貼上、自動填入與驗證（官方宣稱）

經過：視覺上的六格不代表資料上要有六個控制項。
%% line-end %%

### 細節（不索引）
- 對手組：自動填入失效
- 支援狀態：不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

%% line-start id="mwg:forms:8" %%
## 驗證欄位不要擋貼上或關 autocomplete
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：密碼、驗證碼與其他身分驗證欄位允許貼上並保留正確 autocomplete token
- 被什麼擋：密碼管理員與系統驗證碼建議被擋住，使用者只能手打長秘密（引用："DON'T block copy-and-paste (`paste` events) or disable `autocomplete` on passwords, verification codes, or other authentication fields."）
- 戰報：勝——密碼管理員、貼上與自動填入能正常工作（官方宣稱）

經過：安全欄位尤其需要密碼管理員，禁止貼上只會逼使用者改用容易記的弱密碼。
%% line-end %%

### 細節（不索引）
- 對手組：自動填入失效
- 支援狀態：不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

%% line-start id="mwg:forms:9" %%
## 錯誤樣式用 :user-invalid，不單用 :invalid
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：錯誤樣式由 `:user-invalid` 觸發，原生 required 等限制仍保留
- 被什麼擋：只用 `:invalid` 會讓空的必填欄位在使用者互動前就被標成錯（引用："DON'T use the raw `:invalid` CSS pseudo-class alone for error styling to ensure empty required fields are not marked as invalid before the user interacts with the form."）
- 戰報：勝——錯誤等到使用者互動或嘗試送出後才出現（官方宣稱）

經過：頁面剛打開就整片紅，會讓還沒填的人以為自己已經做錯。
%% line-end %%

### 細節（不索引）
- 對手組：播報時機或可靠度出錯
- 支援狀態：不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

%% line-start id="mwg:forms:10" %%
## 不要停用送出鈕來阻止驗證
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：送出鈕保持可按，讓使用者送出後看到錯誤；只有有效送出後才暫停以避免雙重提交
- 被什麼擋：停用送出鈕讓使用者無法觸發驗證，也不知道哪些欄位需要修正（引用："DON'T disable submit buttons to block validation; let users submit and highlight errors."）
- 戰報：勝——按下送出會標出錯誤，有效提交則避免重複（官方宣稱）

經過：灰色按鈕只說不能送，沒說原因；讓原生驗證把問題指出來。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

%% line-start id="mwg:forms:11" %%
## 不要每打一個字就驗證並播報錯誤
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在 submit 或 blur 時驗證；input 時只清除已修正的錯誤，不逐字觸發 aria-live
- 被什麼擋：使用者還在輸入就不斷看到錯誤、聽到播報，形成干擾（引用："DON'T trigger validation errors or `aria-live` error announcements on every keystroke while the user is typing"）
- 戰報：勝——錯誤在適當時機出現，修正時即時消退（官方宣稱）

經過：email 還沒打完一定是無效格式，逐字檢查只是在懲罰正常輸入過程。
%% line-end %%

### 細節（不索引）
- 對手組：播報過量
- 支援狀態：不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

%% line-start id="mwg:forms:12" %%
## 表單字級至少 1rem，避免 iOS 自動放大
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：控制項設 `font: inherit` 與 `font-size: max(1rem, 1em)`，保持至少 16px
- 被什麼擋：欄位字級太小會觸發 iOS 聚焦時自動縮放，打斷表單版面（引用："staying at least `1rem`(16px) to prevent iOS zoom."）
- 戰報：勝——聚焦欄位不再被系統突然放大，文字也跟著容器縮放（官方宣稱）

經過：手機上點一個小字輸入框，整頁突然放大，送出鈕與其他欄位因此跑出畫面。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

%% line-start id="mwg:forms:13" %%
## 視覺隱藏控制項不用 display: none
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：自訂 checkbox／radio 的原生輸入用 1px、`clip-path: inset(50%)` 的 visually-hidden 配方，不用 `display: none`
- 被什麼擋：`display: none` 會把輸入移出無障礙樹，讀屏找不到真正的控制項（引用："NOT `display: none`, which removes them from the accessibility tree."）
- 戰報：勝——控制項視覺上消失，語意、焦點與標籤仍保留（官方宣稱）

經過：畫面上是自訂方框，鍵盤與讀屏仍操作背後的原生 input。
%% line-end %%

### 細節（不索引）
- 對手組：視覺隱藏卻仍可觸及
- 支援狀態：不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

%% line-start id="mwg:forms:14" %%
## AJAX 表單保留 JS 失敗時的伺服器退路
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：原生 form 先能送往伺服器，再用 `preventDefault()` 與 fetch 增強；JS 失敗時仍接受一般提交
- 被什麼擋：唯一提交路徑依賴 JS 時，腳本失敗會讓整張表單不能送（引用："DON'T block page submission if JS fails; ensure server-side fallback."）
- 戰報：勝——有 JS 時走 AJAX，沒有 JS 時仍能完成表單（官方宣稱）

經過：漸進增強不是保留兩套功能，而是先讓原生路徑可用，再加上較好的體驗。
%% line-end %%

### 細節（不索引）
- 對手組：自製控制項丟掉原生行為
- 支援狀態：不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

%% line-start id="mwg:forms:15" %%
## 非作用中的精靈步驟移出 Tab 與無障礙樹
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：非目前步驟用 `hidden`、`display: none` 或 `inert` 隱藏；切換時把焦點移到新步驟標題或第一欄
- 被什麼擋：舊步驟仍在 Tab 順序與無障礙樹裡，使用者會走進看不到或不該操作的欄位（引用："DON'T leave inactive wizard steps in the keyboard `Tab` order or accessibility tree"）
- 戰報：勝——鍵盤與讀屏只接觸目前步驟，焦點也跟著新內容（官方宣稱）

經過：畫面已是付款步驟，Tab 卻回到隱藏的帳號欄位，使用者無法判斷自己身在何處。
%% line-end %%

### 細節（不索引）
- 對手組：視覺隱藏卻仍可觸及
- 支援狀態：不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

%% line-start id="mwg:forms:16" %%
## 多步驟表單避免手機鍵盤遮住欄位與按鈕
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：聚焦欄位與主要按鈕安排在視窗上半部，或用 `scroll-padding` 保留鍵盤空間
- 被什麼擋：虛擬鍵盤升起後遮住正在輸入的欄位或下一步按鈕（引用："design layouts so that the mobile keyboard does not obscure inputs or buttons"）
- 戰報：勝——輸入與前進動作在鍵盤出現時仍看得到（官方宣稱）

經過：填完一欄找不到下一步，使用者只能關掉鍵盤或盲目捲動。
%% line-end %%

### 細節（不索引）
- 對手組：浮層遮住說明
- 支援狀態：不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏
