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

另有十餘條未拆（清單式指南），例如：卡號、郵遞區號、OTP 用 `type="number"`，會有捲動問題並去掉開頭的 0；把一個值拆成多格自動跳格的輸入框；阻擋貼上或關掉密碼、驗證碼欄位的 autocomplete；只用 `:invalid` 讓空的必填欄位在互動前就被標成錯；停用送出鈕擋驗證；每打一個字就驗證、播報錯誤；表單控制項字級小於 `1rem` 觸發 iOS 縮放；用 `display: none` 隱藏輸入讓它離開無障礙樹；非作用中的精靈步驟留在 Tab 順序裡。
