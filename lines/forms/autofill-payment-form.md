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
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：卡號、持卡人、到期日、安全碼分別用 `autocomplete="cc-number"`、`cc-name`、`cc-exp`、`cc-csc`；帳單地址預設同寄送地址，欄位用 `shipping`／`billing` 前綴區分（例如 `billing address-line1`）
- 被什麼擋：沒有 autocomplete 時，使用者可能把卡片資料抄在紙上或用不安全的方式存起來（引用："Without autocomplete, users may keep a physical record of payment card details or store them insecurely."）
- 戰報：勝——欄位帶對 token，瀏覽器能安全地存取並自動填入卡片與地址；不支援時使用者手動輸入，型別與驗證照常運作（官方宣稱）

經過：每次結帳都要從錢包掏卡、抄十六位數字，於是有人乾脆把卡號存在記事本裡。帶對 token 後由瀏覽器保管、自動帶入；寄送與帳單兩組地址靠前綴分開，不會互相填錯。
%% line-end %%

### 細節（不索引）
- 對手組：自動填入失效
- 支援狀態：本指南未列 autocomplete 支援資料（autofill-address-form 指南記為 Widely 2015-07-29）；同指南列出 enterkeyhint、Email/telephone/URL input types、inputmode 皆 Widely
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:autofill-payment-form:2" %%
## 姓名盡量用一個欄位，加上 autocomplete="name"
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：除非真的需要分開儲存名、姓、稱謂，否則只放一個姓名欄位，設 `autocomplete="name"`
- 被什麼擋：（缺）只列出單一欄位的好處，沒直接說拆欄在哪個時刻出錯（引用："Using a single name input makes forms less complex, enables cut-and-paste, and makes autofill simpler."）
- 戰報：勝——單一欄位可整段貼上、自動填入（官方宣稱）

經過：與地址表單指南逐字相同的一段。付款表單裡持卡人姓名另有 `cc-name`，指南的範例同樣用一個欄位收。
%% line-end %%

### 細節（不索引）
- 對手組：表單假設錯的資料格式
- 支援狀態：本指南未列 autocomplete 支援資料（autofill-address-form 指南記為 Widely 2015-07-29）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:autofill-payment-form:3" %%
## 驗證姓名時改用 Unicode 字母比對，不要只收拉丁字母
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：驗證用的正規表示式改用 Unicode 字母比對，例如持卡人欄位的 `pattern="[\p{L} \-\.]+"`，並確認後端能安全處理 Unicode
- 被什麼擋：只比對拉丁字母的正規表示式，會把名字或地址含非拉丁字元的使用者擋在外面（引用："Latin-only excludes users with names or addresses that include characters that aren't in the Latin alphabet."）
- 戰報：勝——改用 Unicode 比對後，這些使用者的輸入能通過驗證（官方宣稱）

經過：與地址表單指南逐字相同的一段。在付款頁被拒收名字，代價就是一筆沒成交的訂單。
%% line-end %%

### 細節（不索引）
- 對手組：表單假設錯的資料格式
- 支援狀態：不適用（指南只說 "Unicode in regular expressions is well supported by modern browsers."，未給 Baseline 資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

另有 5 條未拆：卡號用 `type="number"` 會加上增減鈕、去掉開頭的 0；格式提示放在欄位下方，會被手機鍵盤或自動填入彈窗遮住；安全碼用 `type="password"` 遮罩，打錯一位要到付款被拒才發現；卡號、電話拆成多個欄位，自動填入無法運作；卡號長度的 pattern 寫太死、不允許空格。
