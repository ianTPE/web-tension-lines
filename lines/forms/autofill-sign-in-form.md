---
guide: autofill-sign-in-form
category: forms
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/forms/autofill-sign-in-form.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 依最佳做法建立登入表單

%% line-start id="mwg:autofill-sign-in-form" %%
## 登入欄位用 username／current-password，讓密碼管理員存得下也填得回
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：email 欄位用 `autocomplete="username"`、密碼欄位用 `autocomplete="current-password"`；欄位的 `name`／`id` 固定不隨機，放在有送出鈕的 `<form>` 裡
- 被什麼擋：沒有 autocomplete 時，使用者比較可能把登入資料抄在紙上，或用不安全的方式存在裝置上；`name`／`id` 每次載入都隨機產生、或不在 `<form>` 裡時，瀏覽器不會把資料存起來（引用："Without autocomplete, users may be more likely to keep a physical record of sign-in details, or store sign-in data insecurely on their device."）
- 戰報：勝——瀏覽器能辨識欄位角色，安全地儲存並自動填入帳密；不支援時使用者手動輸入（官方宣稱）

經過：密碼管理員明明存著帳密，打開登入頁卻沒有跳出建議，原因可能是欄位名稱每次部署都變、或整個表單只是一堆 `<div>`。把角色標清楚、名稱固定下來，存與填才接得上。
%% line-end %%

### 細節（不索引）
- 對手組：自動填入失效
- 支援狀態：本指南未列 autocomplete 支援資料（autofill-address-form 指南記為 Widely 2015-07-29）；同指南列 Email/telephone/URL input types、inputmode 皆 Widely
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:autofill-sign-in-form:2" %%
## 帳號與 email 欄位關掉拼字檢查與自動修正
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：帳號、email 欄位加 `spellcheck="false"`；非 email 的帳號欄位另外關掉 `autocorrect` 與 `autocapitalize`（`type="email"` 已自動關閉）
- 被什麼擋：帳號是識別碼不是文章，瀏覽器會把它「改正」成與帳戶對不上的字串（引用："Add `spellcheck="false"` so the browser does not rewrite them into something the account does not match."）
- 戰報：部分改善——`autocorrect` 為 Newly（2026-09-11），關掉後瀏覽器不再改寫識別碼（官方宣稱）

經過：使用者在手機上輸入帳號，拼字檢查、自動修正、自動大寫都是為散文設計的，套在帳號上，送出的字串就和帳戶對不上。對識別碼欄位關掉這些修正；留言、訊息這類自由文字欄位則保留預設。
%% line-end %%

### 細節（不索引）
- 對手組：表單假設錯的資料格式
- 支援狀態：autocorrect：Newly（2026-09-11）；spellcheck、autocapitalize 本指南未給支援資料
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:autofill-sign-in-form:3" %%
## 姓名盡量用一個欄位，加上 autocomplete="name"
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：除非真的需要分開儲存名、姓、稱謂，否則只放一個姓名欄位，設 `autocomplete="name"`
- 被什麼擋：（缺）只列出單一欄位的好處，沒直接說拆欄在哪個時刻出錯（引用："Using a single name input makes forms less complex, enables cut-and-paste, and makes autofill simpler."）
- 戰報：勝——單一欄位可整段貼上、自動填入（官方宣稱）

經過：與地址、付款表單指南逐字相同的一段。登入表單通常沒有姓名欄位，這段是共用的通則。
%% line-end %%

### 細節（不索引）
- 對手組：表單假設錯的資料格式
- 支援狀態：本指南未列 autocomplete 支援資料（autofill-address-form 指南記為 Widely 2015-07-29）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

另有 5 條未拆：姓名驗證只收拉丁字母（同 `mwg:autofill-address-form:3`）；不用 `<form>`、只用 `<div>` 加 JavaScript 送出，JS 失敗就無法登入；要求輸入兩次 email 或密碼，增加放棄率；手機鍵盤蓋住登入鈕，使用者還沒發現就放棄；禁止貼上密碼，反而讓使用者選好記、易破的密碼。
