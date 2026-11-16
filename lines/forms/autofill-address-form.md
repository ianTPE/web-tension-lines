---
guide: autofill-address-form
category: forms
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/forms/autofill-address-form.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 依最佳做法建立地址表單

%% line-start id="mwg:autofill-address-form" %%
## 每個欄位都給 autocomplete，地址拆行時用 address-line1／2 token
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：每個 `<input>`、`<select>`、`<textarea>` 加上對應的 `autocomplete`；街道地址優先用一個 `autocomplete="street-address"` 的 `<textarea>`，資料模型需要分行時改用 `address-line1`、`address-line2` token，只有第一行必填
- 被什麼擋：沒有 token 的欄位，瀏覽器不會自動填入，使用者得重打一次；把街道地址拆到沒有這些 token 的多個欄位，自動填入就失效（引用："Don't split the street address across inputs that lack these tokens"）
- 戰報：勝——`autocomplete` 已 Widely，欄位帶對 token 後自動填入照常運作；不支援自動填入的瀏覽器使用者手動輸入即可（官方宣稱）

經過：地址表單是最常被自動填入的表單之一，卻常拆成「地址 1」「地址 2」「門牌」等自訂欄位，瀏覽器認不出來就整段留白。給每一欄正確的 token，或乾脆用一個多行欄位，存好的地址一次帶入。
%% line-end %%

### 細節（不索引）
- 對手組：自動填入失效
- 支援狀態：html.elements.input.autocomplete：Widely（2015-07-29）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:autofill-address-form:2" %%
## 姓名盡量用一個欄位，加上 autocomplete="name"
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：除非真的需要分開儲存名、姓、稱謂，否則只放一個姓名欄位，設 `autocomplete="name"`
- 被什麼擋：（缺）只列出單一欄位的好處（較簡單、可以貼上、自動填入較簡單），沒直接說拆欄在哪個時刻出錯（引用："Using a single name input makes forms less complex, enables cut-and-paste, and makes autofill simpler."）
- 戰報：勝——`autocomplete` 已 Widely，單一欄位可整段貼上、自動填入（官方宣稱）

經過：「名」「姓」分兩格，預設了每個人的名字都能這樣切。指南建議沒有理由就別切，貼上與自動填入都只要對付一個欄位。
%% line-end %%

### 細節（不索引）
- 對手組：表單假設錯的資料格式
- 支援狀態：html.elements.input.autocomplete：Widely（2015-07-29）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:autofill-address-form:3" %%
## 驗證姓名與地址時改用 Unicode 字母比對，不要只收拉丁字母
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：驗證用的正規表示式改用 Unicode 字母比對（例如 `\p{L}`），並確認後端能安全處理 Unicode 的輸入與輸出
- 被什麼擋：只比對拉丁字母的正規表示式，會把名字或地址含非拉丁字元的使用者擋在外面（引用："Latin-only excludes users with names or addresses that include characters that aren't in the Latin alphabet."）
- 戰報：勝——改用 Unicode 比對後，這些使用者的輸入能通過驗證（官方宣稱）

經過：`[A-Za-z]+` 看起來是合理的姓名檢查，但「王小明」「Олег」都過不了，表單直接拒收真實的名字。換成 Unicode 字母類別，同一條規則就能涵蓋各種文字。
%% line-end %%

### 細節（不索引）
- 對手組：表單假設錯的資料格式
- 支援狀態：不適用（指南只說 "Unicode in regular expressions is well supported by modern browsers."，未給 Baseline 資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

未拆：`<label>`、`<button>`、`type="email"`／`type="tel"`、送出鈕寫「Proceed to Payment」等段落只說做法的好處，沒有指出舊做法的可觀察後果。
