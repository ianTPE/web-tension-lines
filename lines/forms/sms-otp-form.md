---
guide: sms-otp-form
category: forms
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/forms/sms-otp-form.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 簡訊一次性密碼（OTP）表單驗證

%% line-start id="mwg:sms-otp-form" %%
## 用 WebOTP 與綁網域的簡訊格式自動帶入驗證碼，擋掉切 app 抄碼
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：單一 `<input autocomplete="one-time-code" inputmode="numeric">`，簡訊最後一行寫 `@網域 #驗證碼`，支援時用 `navigator.credentials.get({ otp: { transport: ['sms'] } })` 取碼並 `requestSubmit()`，以 `AbortController` 管理每個離開路徑
- 被什麼擋：使用者要在瀏覽器和簡訊 app 之間切換、記住或複製多位數驗證碼，增加摩擦與流失，還容易在仿冒網域上被釣魚（引用："Switching between a browser and an SMS messaging app to memorize or copy-paste a multi-digit code introduces user friction, increases drop-off rates, and leaves users vulnerable to phishing on spoofed domains."）
- 戰報：部分改善——支援 WebOTP 的瀏覽器先核對網域再帶入驗證碼，一次點擊完成；不支援時退回鍵盤列建議（Safari 等）或手動輸入數字鍵盤，網域綁定仍在但少了自動送出（官方宣稱）

經過：收到簡訊、切出去、記下六位數、切回來、打錯一位重來，流程在這裡掉人；仿冒網站也一樣能叫人抄碼。網域綁定的簡訊格式讓瀏覽器與系統只在網域相符時才提供驗證碼，WebOTP 再把「貼上並送出」變成一下點擊。Firefox 沒有 WebOTP，只剩手動輸入。
%% line-end %%

### 細節（不索引）
- 對手組：自動填入失效
- 支援狀態：WebOTP：Limited availability。Supported by: Chrome 93, Edge 93, Safari 27；Unsupported in: Firefox
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：手機號碼驗證、付款確認這類步驟可以做到「簡訊一到就自動帶入並送出」，而且驗證碼綁網域，釣魚頁拿不到自動帶入。跨來源 iframe（3-D Secure）也能用，但目前 Permissions-Policy 委派僅 Chromium
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:sms-otp-form:2" %%
## 驗證碼用 type="text" 加 inputmode="numeric"，不要用 type="number"
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：OTP 欄位用 `type="text"` 配 `inputmode="numeric"`、`pattern="\d{6}"`，不用 `type="number"` 也不用 `type="tel"`
- 被什麼擋：驗證碼是識別字串不是數量，`type="number"` 會多出增減按鈕、可能吃掉開頭的 0，還會被滾輪意外改值（引用："Using `type="number"` adds increment/decrement spinner buttons, can strip leading zeros, and allows accidental scroll-wheel value changes."）
- 戰報：勝——`inputmode` 已 Widely，行動裝置照樣出數字鍵盤，值保持原樣的字串（官方宣稱）

經過：為了在手機上叫出數字鍵盤而用 `type="number"`，結果 `012345` 變成 `12345`，捲動頁面時滑鼠滾過欄位還會把碼改掉。改用文字欄位加 `inputmode`，鍵盤一樣，值不會被當成數字處理。
%% line-end %%

### 細節（不索引）
- 對手組：用錯原生控制項
- 支援狀態：inputmode：Widely（2021-12-07）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:sms-otp-form:3" %%
## 驗證碼用單一欄位，不要拆成六個格子
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：只用一個 `<input>`，要分格的外觀就用等寬字型加 `letter-spacing`
- 被什麼擋：六個 `maxlength="1"` 的分格輸入，在許多瀏覽器會讓 `autocomplete="one-time-code"` 自動帶入失效，也妨礙貼上、讓讀屏導覽變複雜（引用："Multi-box OTP patterns (six separate `maxlength="1"` inputs) break native `autocomplete="one-time-code"` autofill in many browsers, hinder copy-pasting, and complicate screen reader navigation."）
- 戰報：勝——單一欄位能吃到系統的驗證碼建議與整段貼上，外觀仍可做成分格（官方宣稱）

經過：設計稿畫了六個方格，實作成六個輸入框，系統跳出的驗證碼建議卻填不進去，貼上也只進第一格。換成一個欄位加字距，看起來一樣，自動帶入和貼上都恢復。
%% line-end %%

### 細節（不索引）
- 對手組：自動填入失效
- 支援狀態：inputmode：Widely（2021-12-07）；指南未附 `autocomplete="one-time-code"` 的支援資料
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:sms-otp-form:4" %%
## 自動取碼後用 requestSubmit()，不要用 form.submit()
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：WebOTP 取到碼、填進欄位後呼叫 `form.requestSubmit()`（或直接呼叫自己的驗證函式）
- 被什麼擋：`form.submit()` 會繞過 submit 事件監聽（`preventDefault()`／`fetch()` 處理）並跳過原生約束驗證（引用："`form.submit()` bypasses `submit` event listeners (`event.preventDefault()` / `fetch()` handlers) and skips native constraint validation."）
- 戰報：勝——`requestSubmit()` 走和使用者按送出一樣的路徑，監聽器與驗證都會執行（官方宣稱）

經過：自動取碼後順手 `form.submit()`，頁面直接以原生 POST 跳走，原本寫在 submit 事件裡的 fetch 送出、中止監聽、格式驗證全被略過。改成 `requestSubmit()` 就和手動按下送出鈕一致。
%% line-end %%

### 細節（不索引）
- 對手組：表單意外送出
- 支援狀態：不適用（指南未附 requestSubmit() 的支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:sms-otp-form:5" %%
## 格式提示放在欄位上方，擋掉被自動填入浮層和鍵盤蓋住
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：可見 `<label>` 之外，格式說明（以 `aria-describedby` 連結）放在 `<input>` 的視覺上方
- 被什麼擋：提示放在欄位下方時，自動填入的浮層和行動裝置的虛擬鍵盤會把它蓋住（引用："place any format instructions (linked via `aria-describedby`) visually **above** the `<input>` so autofill popovers and mobile virtual keyboards never cover the instructions."）
- 戰報：勝——提示在上方，聚焦輸入時仍看得到（官方宣稱）

經過：「請輸入寄到手機的 6 位數驗證碼」放在欄位下面，一點欄位鍵盤升起、驗證碼建議跳出，說明正好被蓋掉。挪到上方就一直看得到。
%% line-end %%

### 細節（不索引）
- 對手組：浮層遮住說明
- 支援狀態：不適用（版面擺放，指南未附支援資料）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

另有 1 條未拆：跨來源 iframe 取碼（簡訊列出兩個網域、`Permissions-Policy: otp-credentials`、`<iframe allow>`），指南只說預設受限，沒說舊做法哪裡壞；可視為 `mwg:sms-otp-form` 的延伸。
