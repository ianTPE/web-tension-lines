---
guide: autofill-sign-up-form
category: forms
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/forms/autofill-sign-up-form.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 依最佳做法建立註冊表單

%% line-start id="mwg:autofill-sign-up-form" %%
## 註冊欄位用 username／new-password，讓瀏覽器存下新帳密
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：每個欄位加對應的 `autocomplete`，email 欄位用 `autocomplete="username"`、密碼欄位用 `autocomplete="new-password"`；欄位的 `name`／`id` 固定，放在有送出鈕的 `<form>` 裡
- 被什麼擋：沒有 autocomplete 時，使用者比較可能把註冊資料抄在紙上，或用不安全的方式存在裝置上（引用："Without autocomplete, users may be more likely to keep a physical record of sign-up details, or store sign-up data insecurely on their device."）
- 戰報：勝——瀏覽器能辨識這是新密碼，安全地儲存、之後自動填入，也能提供強密碼建議；不支援時使用者手動輸入（官方宣稱）

經過：註冊是瀏覽器記住帳密的那一刻，欄位角色不清楚，之後每次登入都得靠使用者自己記。標成 `new-password`，瀏覽器才會提供產生的強密碼並存起來。
%% line-end %%

### 細節（不索引）
- 對手組：自動填入失效
- 支援狀態：本指南未列 autocomplete 支援資料（autofill-address-form 指南記為 Widely 2015-07-29）；同指南列 Email/telephone/URL input types、inputmode 皆 Widely
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:autofill-sign-up-form:2" %%
## 帳號與 email 欄位關掉拼字檢查與自動修正
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：帳號、email 欄位加 `spellcheck="false"`；非 email 的帳號欄位另外關掉 `autocorrect` 與 `autocapitalize`（`type="email"` 已自動關閉）
- 被什麼擋：帳號是識別碼不是文章，瀏覽器會把它「改正」成與帳戶對不上的字串（引用："Add `spellcheck="false"` so the browser does not rewrite them into something the account does not match."）
- 戰報：部分改善——`autocorrect` 為 Newly（2026-09-11），關掉後瀏覽器不再改寫識別碼（官方宣稱）

經過：與登入表單指南逐字相同的一段。拼字檢查、自動修正、自動大寫都是為散文設計的，套在帳號上就會改出一個和使用者本意不同的識別碼。
%% line-end %%

### 細節（不索引）
- 對手組：表單假設錯的資料格式
- 支援狀態：autocorrect：Newly（2026-09-11）；spellcheck、autocapitalize 本指南未給支援資料
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:autofill-sign-up-form:3" %%
## 姓名盡量用一個欄位，加上 autocomplete="name"
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：除非真的需要分開儲存名、姓、稱謂，否則只放一個姓名欄位，設 `autocomplete="name"`
- 被什麼擋：（缺）只列出單一欄位的好處，沒直接說拆欄在哪個時刻出錯（引用："Using a single name input makes forms less complex, enables cut-and-paste, and makes autofill simpler."）
- 戰報：勝——單一欄位可整段貼上、自動填入（官方宣稱）

經過：與地址、付款、登入表單指南逐字相同的一段。註冊表單常要求姓名，拆成名、姓兩格就預設了名字的結構。
%% line-end %%

### 細節（不索引）
- 對手組：表單假設錯的資料格式
- 支援狀態：本指南未列 autocomplete 支援資料（autofill-address-form 指南記為 Widely 2015-07-29）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

另有 6 條未拆：姓名驗證只收拉丁字母（同 `mwg:autofill-address-form:3`）；不用 `<form>`、只用 `<div>` 加 JavaScript 送出；要求輸入兩次 email 或密碼；手機鍵盤蓋住註冊鈕；沒有 `new-password` 時密碼管理員可能把既有密碼填進註冊欄位；禁止貼上密碼。
