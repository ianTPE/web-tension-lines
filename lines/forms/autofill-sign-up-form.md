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
- 做法：每個欄位加對應的 `autocomplete`，email 欄位用 `autocomplete="username"`、密碼欄位用 `autocomplete="new-password"`；欄位的 `name`／`id` 固定，放在有送出鈕的 `<form>` 裡
- 對手：沒有 autocomplete 時，使用者比較可能把註冊資料抄在紙上，或用不安全的方式存在裝置上（引用："Without autocomplete, users may be more likely to keep a physical record of sign-up details, or store sign-up data insecurely on their device."）
- 退路：不需要——`autocomplete` 早已 Widely，沒有需要退回去的狀態
- 解鎖：以前註冊欄位沒標角色，瀏覽器存不進新帳密；現在標成 `username`／`new-password` 就能存，也能順帶產生強密碼建議

經過：註冊是瀏覽器記住帳密的那一刻，欄位角色不清楚，之後每次登入都得靠使用者自己記。標成 `new-password`，瀏覽器才會提供產生的強密碼並存起來。
%% line-end %%

### 細節（不索引）
- 對手組：自動填入失效
- 支援狀態：本指南未列 autocomplete 支援資料（autofill-address-form 指南記為 Widely 2015-07-29）；同指南列 Email/telephone/URL input types、inputmode 皆 Widely
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:autofill-sign-up-form:2" %%
## 帳號與 email 欄位關掉拼字檢查與自動修正
- 做法：帳號、email 欄位加 `spellcheck="false"`；非 email 的帳號欄位另外關掉 `autocorrect` 與 `autocapitalize`（`type="email"` 已自動關閉）
- 對手：帳號是識別碼不是文章，瀏覽器會把它「改正」成與帳戶對不上的字串（引用："Add `spellcheck="false"` so the browser does not rewrite them into something the account does not match."）
- 退路：保住主要行為——email 欄位本來就被瀏覽器關掉自動修正，少了支援的只是非 email 帳號多一道防護
- 解鎖：以前只能任瀏覽器把帳號改寫成別的字串；現在能對識別碼欄位明確關掉拼字檢查、自動修正與自動大寫

經過：與登入表單指南逐字相同的一段。拼字檢查、自動修正、自動大寫都是為散文設計的，套在帳號上就會改出一個和使用者本意不同的識別碼。
%% line-end %%

### 細節（不索引）
- 對手組：表單假設錯的資料格式
- 支援狀態：autocorrect：Newly（2026-09-11）；spellcheck、autocapitalize 本指南未給支援資料
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:autofill-sign-up-form:3" %%
## 姓名盡量用一個欄位，加上 autocomplete="name"
- 做法：除非真的需要分開儲存名、姓、稱謂，否則只放一個姓名欄位，設 `autocomplete="name"`
- 對手：（缺）只列出單一欄位的好處，沒直接說拆欄在哪個時刻出錯（引用："Using a single name input makes forms less complex, enables cut-and-paste, and makes autofill simpler."）
- 退路：不需要——`autocomplete` 已 Widely，欄位怎麼切本來就是自己的選擇
- 解鎖：（缺）

經過：與地址、付款、登入表單指南逐字相同的一段。註冊表單常要求姓名，拆成名、姓兩格就預設了名字的結構。
%% line-end %%

### 細節（不索引）
- 對手組：表單假設錯的資料格式
- 支援狀態：本指南未列 autocomplete 支援資料（autofill-address-form 指南記為 Widely 2015-07-29）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 缺／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:autofill-sign-up-form:4" %%
## 姓名驗證改用 Unicode 字母，不只收拉丁字母
- 做法：姓名驗證改用 Unicode 字母比對，並確認後端能安全處理 Unicode 輸入與輸出
- 對手：只比對拉丁字母會把名字或地址含其他文字的使用者擋在外面（引用："Latin-only excludes users with names or addresses that include characters that aren't in the Latin alphabet."）
- 退路：不需要——正則的 Unicode 字母比對現代瀏覽器都支援，不必退路
- 解鎖：（缺）

經過：註冊是使用者第一次留下姓名的地方，一開始就只接受拉丁字母，後續帳戶資料也只能保存錯誤形式。
%% line-end %%

### 細節（不索引）
- 對手組：表單假設錯的資料格式
- 支援狀態：不適用（指南只說現代瀏覽器支援 Unicode 正規表示式，未給 Baseline 資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:autofill-sign-up-form:5" %%
## 註冊資料放在真正的 form 裡，不靠 div 加 JS 才能送
- 做法：註冊欄位放進帶送出鈕的 `<form>`，保留原生送出能力，再依需要增強成 JavaScript 流程
- 對手：只用 `<div>` 並完全靠 JavaScript 送出時，JS 失敗就無法註冊，也失去內建的輔助技術與舊瀏覽器行為（引用："can still work even if JavaScript fails."）
- 退路：不需要——原生 form 一直是既有能力，不涉及瀏覽器功能支援
- 解鎖：（缺）

經過：帳號建立不能只剩一條 JavaScript 路徑。原生表單先確保腳本失敗時仍能完成基本流程。
%% line-end %%

### 細節（不索引）
- 對手組：自製控制項丟掉原生行為
- 支援狀態：不適用（指南未附 form 的支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:autofill-sign-up-form:6" %%
## 註冊不要求輸入兩次 email 或密碼
- 做法：帳密各輸入一次，提供顯示密碼、email 確認與重設密碼管道，不另加確認欄位
- 對手：重複輸入對所有人都增加工作並提高放棄率，對能自動填入或使用強密碼建議的人尤其沒有意義（引用："causes extra work for all users, and increases abandonment rates."）
- 退路：不需要——要不要重複輸入是流程設計，不涉及瀏覽器功能支援
- 解鎖：（缺）

經過：確認欄位擋不住所有錯誤，卻確定讓每個人多做一次工。用可檢查、可修正的機制取代重打。
%% line-end %%

### 細節（不索引）
- 對手組：表單假設錯的資料格式
- 支援狀態：不適用（流程設計，指南未附支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:autofill-sign-up-form:7" %%
## 註冊欄位與送出鈕放在手機鍵盤遮不到的位置
- 做法：註冊頁上方只放 email／電話、密碼與註冊鈕，其他內容移到下方
- 對手：手機鍵盤可能蓋住表單或部分遮住註冊鈕，使用者還沒弄清狀況就放棄（引用："mobile keyboards may cover your form or, worse, partially obstruct the Sign up button. Users may give up before realizing what has happened."）
- 退路：不需要——版面配置是表單自己的安排，不涉及瀏覽器功能支援
- 解鎖：（缺）

經過：註冊鈕被鍵盤蓋住時，使用者可能以為頁面沒有下一步。把核心流程放在鍵盤之上的區域。
%% line-end %%

### 細節（不索引）
- 對手組：浮層遮住說明
- 支援狀態：不適用（版面配置，指南未附支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:autofill-sign-up-form:8" %%
## 密碼欄位允許貼上
- 做法：不攔截密碼欄位的 paste 事件，配合 `new-password`、密碼管理員與顯示密碼功能
- 對手：禁止貼上會促使使用者選好記、可能更容易被破的密碼；使用者要貼上時才發現被擋，也避不開剪貼簿風險（引用："Disallowing password pasting annoys users, encourages passwords that are memorable (and therefore may be easier to compromise)"）
- 退路：不需要——要不要攔截貼上是表單自己的選擇，不涉及瀏覽器功能支援
- 解鎖：（缺）

經過：第一條的 `new-password` 已涵蓋避免密碼管理員誤填既有密碼；這條處理另一個相反問題：頁面主動阻止安全密碼進場。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：不適用（指南未附支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2
