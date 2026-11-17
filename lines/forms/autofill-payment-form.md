---
guide: autofill-payment-form
category: forms
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/forms/autofill-payment-form.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 依最佳做法建立付款表單

%% line-start id="mwg:autofill-payment-form" %%
## 付款欄位給 cc-* autocomplete，帳單地址加 billing 前綴
- 做法：卡號、持卡人、到期日、安全碼分別用 `autocomplete="cc-number"`、`cc-name`、`cc-exp`、`cc-csc`；帳單地址預設同寄送地址，欄位用 `shipping`／`billing` 前綴區分（例如 `billing address-line1`）
- 對手：沒有 autocomplete 時，使用者可能把卡片資料抄在紙上或用不安全的方式存起來（引用："Without autocomplete, users may keep a physical record of payment card details or store them insecurely."）
- 退路：不需要——`autocomplete` 早已 Widely，沒有需要退回去的狀態
- 解鎖：以前付款欄位沒有對應 token，瀏覽器帶不進資料；現在用 `cc-number`、`cc-name` 等 token 讓瀏覽器保管並自動填入，寄送與帳單地址也能用前綴分開

經過：每次結帳都要從錢包掏卡、抄十六位數字，於是有人乾脆把卡號存在記事本裡。帶對 token 後由瀏覽器保管、自動帶入；寄送與帳單兩組地址靠前綴分開，不會互相填錯。
%% line-end %%

### 細節（不索引）
- 對手組：自動填入失效
- 支援狀態：本指南未列 autocomplete 支援資料（autofill-address-form 指南記為 Widely 2015-07-29）；同指南列出 enterkeyhint、Email/telephone/URL input types、inputmode 皆 Widely
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:autofill-payment-form:2" %%
## 姓名盡量用一個欄位，加上 autocomplete="name"
- 做法：除非真的需要分開儲存名、姓、稱謂，否則只放一個姓名欄位，設 `autocomplete="name"`
- 對手：（缺）只列出單一欄位的好處，沒直接說拆欄在哪個時刻出錯（引用："Using a single name input makes forms less complex, enables cut-and-paste, and makes autofill simpler."）
- 退路：不需要——`autocomplete` 已 Widely，欄位怎麼切本來就是自己的選擇
- 解鎖：（缺）

經過：與地址表單指南逐字相同的一段。付款表單裡持卡人姓名另有 `cc-name`，指南的範例同樣用一個欄位收。
%% line-end %%

### 細節（不索引）
- 對手組：表單假設錯的資料格式
- 支援狀態：本指南未列 autocomplete 支援資料（autofill-address-form 指南記為 Widely 2015-07-29）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 缺／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:autofill-payment-form:3" %%
## 驗證姓名時改用 Unicode 字母比對，不要只收拉丁字母
- 做法：驗證用的正規表示式改用 Unicode 字母比對，例如持卡人欄位的 `pattern="[\p{L} \-\.]+"`，並確認後端能安全處理 Unicode
- 對手：只比對拉丁字母的正規表示式，會把名字或地址含非拉丁字元的使用者擋在外面（引用："Latin-only excludes users with names or addresses that include characters that aren't in the Latin alphabet."）
- 退路：不需要——正則的 Unicode 字母比對現代瀏覽器都支援，不必退路
- 解鎖：（缺）

經過：與地址表單指南逐字相同的一段。在付款頁被拒收名字，代價就是一筆沒成交的訂單。
%% line-end %%

### 細節（不索引）
- 對手組：表單假設錯的資料格式
- 支援狀態：不適用（指南只說 "Unicode in regular expressions is well supported by modern browsers."，未給 Baseline 資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:autofill-payment-form:4" %%
## 卡號用文字欄位加數字鍵盤，不用 type="number"
- 做法：卡號用 `type="text"`、`inputmode="numeric"`、`autocomplete="cc-number"`，允許空格並設合理長度與 pattern
- 對手：`type="number"` 會增加增減鈕並去掉開頭的 0，把卡號當成會參與算術的數量（引用："DO NOT use type="number" — it adds increment/decrement controls and strips leading zeros"）
- 退路：不需要——`inputmode` 已 Widely，數字鍵盤沒有退路問題
- 解鎖：以前要有數字鍵盤就得用 `type="number"`，卻多出增減鈕、還會吃掉開頭的 0；現在文字欄位加 `inputmode="numeric"` 就能只借鍵盤、不改值的語意

經過：為了數字鍵盤選了 number，卻同時得到不需要的微調按鈕與數值正規化。文字欄位只借用鍵盤，不改變值的語意。
%% line-end %%

### 細節（不索引）
- 對手組：用錯原生控制項
- 支援狀態：inputmode：Widely（2021-12-07）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:autofill-payment-form:5" %%
## 付款格式提示放在欄位上方
- 做法：到期日等格式提示放在可見的欄位上方，用 `aria-describedby` 連結；placeholder 只當額外線索
- 對手：欄位下方的提示會被手機鍵盤或自動填入浮層遮住；只靠 placeholder 時一開始輸入就消失（引用："Hints that sit below an input are easily hidden by the mobile keyboard or by the autofill popover at the moment the user needs them."）
- 退路：不需要——純版面擺放，不涉及瀏覽器功能支援
- 解鎖：（缺）

經過：使用者正要輸入 MM/YY，鍵盤升起、建議浮層跳出，下方的格式說明正好消失。搬到上方就不用記住。
%% line-end %%

### 細節（不索引）
- 對手組：浮層遮住說明
- 支援狀態：不適用（版面擺放，指南未附支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:autofill-payment-form:6" %%
## 安全碼不要遮罩，讓使用者送出前檢查數字
- 做法：卡片安全碼用 `type="text"`、`inputmode="numeric"`、`autocomplete="cc-csc"`，不用 `type="password"`
- 對手：遮住的三四位安全碼無法檢查，打錯一位要等付款被拒才發現；遮罩對印在卡片上的數字也增加不了多少保護（引用："Users can't check a masked three- or four-digit code for typos, so a mistyped digit isn't caught until the payment is declined"）
- 退路：不需要——`inputmode` 已 Widely，要不要遮罩是表單自己的選擇
- 解鎖：（缺）

經過：安全碼只有幾位，使用者看一眼卡片就能確認；遮罩把這個確認機會拿掉，代價是一筆本可避免的被拒交易。
%% line-end %%

### 細節（不索引）
- 對手組：表單假設錯的資料格式
- 支援狀態：inputmode：Widely（2021-12-07）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:autofill-payment-form:7" %%
## 卡號與電話各用一個欄位，不拆成多格
- 做法：卡號、電話號碼各用單一 `<input>`，需要分組外觀時用樣式呈現，不切成多個欄位
- 對手：拆成多格會讓瀏覽器無法自動填入，也增加輸入與驗證的負擔（引用："For payment card and phone numbers use a single input: don't split the number into parts. That makes it easier for users to enter data, makes validation simpler, and enables browsers to autofill."）
- 退路：不需要——單一欄位與拆格的差別是表單寫法，不涉及瀏覽器功能支援
- 解鎖：以前把卡號拆成一格四碼，瀏覽器不知道要把整組數字填到哪裡；現在用單一欄位就能被自動填入

經過：每四碼一格看起來像實體卡片，瀏覽器卻不知道要把完整卡號分到哪裡。保留一個資料入口，外觀另外處理。
%% line-end %%

### 細節（不索引）
- 對手組：自動填入失效
- 支援狀態：不適用（指南未附此做法的支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:autofill-payment-form:8" %%
## 卡號 pattern 允許不同長度與空格
- 做法：驗證卡號接受實際發卡範圍的長度與使用者輸入的空格，後端處理前再移除空格
- 對手：pattern 寫死單一長度會拒絕合法卡片；不允許空格則把實體卡上的分組格式判成錯誤，打斷結帳（引用："Allow users to include spaces when they're entering a new payment card number, since this is how numbers are displayed on physical cards."）
- 退路：不需要——驗證規則是後端與表單自己的事，不涉及瀏覽器功能支援
- 解鎖：（缺）

經過：使用者照卡片輸入「1234 5678…」卻看到格式錯誤，只好重打。指南建議卡號長度保持彈性，安全碼則接受三或四位。
%% line-end %%

### 細節（不索引）
- 對手組：表單假設錯的資料格式
- 支援狀態：不適用（正規表示式驗證，指南未附支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2
