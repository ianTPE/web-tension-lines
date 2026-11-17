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
- 做法：email 欄位用 `autocomplete="username"`、密碼欄位用 `autocomplete="current-password"`；欄位的 `name`／`id` 固定不隨機，放在有送出鈕的 `<form>` 裡
- 對手：沒有 autocomplete 時，使用者比較可能把登入資料抄在紙上，或用不安全的方式存在裝置上；`name`／`id` 每次載入都隨機產生、或不在 `<form>` 裡時，瀏覽器不會把資料存起來（引用："Without autocomplete, users may be more likely to keep a physical record of sign-in details, or store sign-in data insecurely on their device."）
- 退路：不需要——`autocomplete` 早已 Widely，沒有需要退回去的狀態
- 解鎖：以前欄位名稱不固定或沒放進 form，密碼管理員存不進也填不回；現在用 `username`／`current-password` 搭配固定名稱就能存也能填

經過：密碼管理員明明存著帳密，打開登入頁卻沒有跳出建議，原因可能是欄位名稱每次部署都變、或整個表單只是一堆 `<div>`。把角色標清楚、名稱固定下來，存與填才接得上。
%% line-end %%

### 細節（不索引）
- 對手組：自動填入失效
- 支援狀態：本指南未列 autocomplete 支援資料（autofill-address-form 指南記為 Widely 2015-07-29）；同指南列 Email/telephone/URL input types、inputmode 皆 Widely
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:autofill-sign-in-form:2" %%
## 帳號與 email 欄位關掉拼字檢查與自動修正
- 做法：帳號、email 欄位加 `spellcheck="false"`；非 email 的帳號欄位另外關掉 `autocorrect` 與 `autocapitalize`（`type="email"` 已自動關閉）
- 對手：帳號是識別碼不是文章，瀏覽器會把它「改正」成與帳戶對不上的字串（引用："Add `spellcheck="false"` so the browser does not rewrite them into something the account does not match."）
- 退路：保住主要行為——email 欄位本來就被瀏覽器關掉自動修正，少了支援的只是非 email 帳號多一道防護
- 解鎖：以前只能任瀏覽器把帳號改寫成別的字串；現在能對識別碼欄位明確關掉拼字檢查、自動修正與自動大寫

經過：使用者在手機上輸入帳號，拼字檢查、自動修正、自動大寫都是為散文設計的，套在帳號上，送出的字串就和帳戶對不上。對識別碼欄位關掉這些修正；留言、訊息這類自由文字欄位則保留預設。
%% line-end %%

### 細節（不索引）
- 對手組：表單假設錯的資料格式
- 支援狀態：autocorrect：Newly（2026-09-11）；spellcheck、autocapitalize 本指南未給支援資料
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:autofill-sign-in-form:3" %%
## 姓名盡量用一個欄位，加上 autocomplete="name"
- 做法：除非真的需要分開儲存名、姓、稱謂，否則只放一個姓名欄位，設 `autocomplete="name"`
- 對手：（缺）只列出單一欄位的好處，沒直接說拆欄在哪個時刻出錯（引用："Using a single name input makes forms less complex, enables cut-and-paste, and makes autofill simpler."）
- 退路：不需要——`autocomplete` 已 Widely，欄位怎麼切本來就是自己的選擇
- 解鎖：（缺）

經過：與地址、付款表單指南逐字相同的一段。登入表單通常沒有姓名欄位，這段是共用的通則。
%% line-end %%

### 細節（不索引）
- 對手組：表單假設錯的資料格式
- 支援狀態：本指南未列 autocomplete 支援資料（autofill-address-form 指南記為 Widely 2015-07-29）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 缺／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:autofill-sign-in-form:4" %%
## 姓名驗證改用 Unicode 字母，不只收拉丁字母
- 做法：姓名驗證改用 Unicode 字母比對，並確認後端能安全處理 Unicode 輸入與輸出
- 對手：只比對拉丁字母會把名字或地址含其他文字的使用者擋在外面（引用："Latin-only excludes users with names or addresses that include characters that aren't in the Latin alphabet."）
- 退路：不需要——正則的 Unicode 字母比對現代瀏覽器都支援，不必退路
- 解鎖：（缺）

經過：與地址、付款、註冊表單共用同一段通則。姓名是國際化資料，不該被套用英文識別碼的限制。
%% line-end %%

### 細節（不索引）
- 對手組：表單假設錯的資料格式
- 支援狀態：不適用（指南只說現代瀏覽器支援 Unicode 正規表示式，未給 Baseline 資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:autofill-sign-in-form:5" %%
## 登入資料放在真正的 form 裡，不靠 div 加 JS 才能送
- 做法：帳號密碼放進帶送出鈕的 `<form>`，保留原生送出能力，再依需要增強成 JavaScript 流程
- 對手：只用 `<div>` 並完全靠 JavaScript 送出時，JS 失敗就無法登入，也失去內建的輔助技術與舊瀏覽器行為（引用："can still work even if JavaScript fails."）
- 退路：不需要——原生 form 一直是既有能力，不涉及瀏覽器功能支援
- 解鎖：（缺）

經過：腳本載入失敗時，畫面上的欄位仍在，使用者卻怎麼按都沒反應。真正的表單先保住最基本的路。
%% line-end %%

### 細節（不索引）
- 對手組：自製控制項丟掉原生行為
- 支援狀態：不適用（指南未附 form 的支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:autofill-sign-in-form:6" %%
## 登入不要求輸入兩次 email 或密碼
- 做法：帳密各輸入一次，提供顯示密碼與重設密碼管道，不另加確認欄位
- 對手：重複輸入對所有人都增加工作並提高放棄率，對能自動填入或使用強密碼建議的人尤其沒有意義（引用："causes extra work for all users, and increases abandonment rates."）
- 退路：不需要——要不要重複輸入是流程設計，不涉及瀏覽器功能支援
- 解鎖：（缺）

經過：密碼管理員已經帶入正確帳密，確認欄位卻要求使用者再手打一次，原本自動化的流程反而被迫退回去。
%% line-end %%

### 細節（不索引）
- 對手組：表單假設錯的資料格式
- 支援狀態：不適用（流程設計，指南未附支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:autofill-sign-in-form:7" %%
## 登入欄位與送出鈕放在手機鍵盤遮不到的位置
- 做法：登入頁上方只放 email／電話、密碼與登入鈕，其他內容移到下方
- 對手：手機鍵盤可能蓋住表單或部分遮住登入鈕，使用者還沒弄清狀況就放棄（引用："mobile keyboards may cover your form or, worse, partially obstruct the Sign in button. Users may give up before realizing what has happened."）
- 退路：不需要——版面配置是表單自己的安排，不涉及瀏覽器功能支援
- 解鎖：（缺）

經過：使用者輸入完密碼，畫面上只剩鍵盤，登入鈕被蓋在後面。精簡首屏配置比事後補捲動更直接。
%% line-end %%

### 細節（不索引）
- 對手組：浮層遮住說明
- 支援狀態：不適用（版面配置，指南未附支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:autofill-sign-in-form:8" %%
## 密碼欄位允許貼上
- 做法：不攔截密碼欄位的 paste 事件，配合密碼管理員與顯示密碼功能
- 對手：禁止貼上會促使使用者選好記、可能更容易被破的密碼；使用者要貼上時才發現被擋，也避不開剪貼簿風險（引用："Disallowing password pasting annoys users, encourages passwords that are memorable (and therefore may be easier to compromise)"）
- 退路：不需要——要不要攔截貼上是表單自己的選擇，不涉及瀏覽器功能支援
- 解鎖：（缺）

經過：禁止貼上看似資安措施，實際是在懲罰使用密碼管理員的人。安全風險沒有消失，只是多了一層摩擦。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：不適用（指南未附支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2
