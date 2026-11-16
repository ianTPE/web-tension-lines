---
guide: required-field-feedback
category: forms
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/forms/required-field-feedback.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 必填欄位的回饋

%% line-start id="mwg:required-field-feedback" %%
## 用 :user-invalid 標示必填錯誤，頁面一載入不要就標紅
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：欄位加 `required`，錯誤樣式與錯誤文字用 `:user-invalid` 觸發，並附上帶「Error」文字替代的圖示，不只靠顏色
- 被什麼擋：頁面一載入就把必填欄位標成錯誤狀態，會讓使用者困惑；欄位應該在使用者試過並失敗後才顯示無效（引用："Marking required fields with an error state immediately upon page load can be confusing."）
- 戰報：勝——`:user-invalid` 已 Widely，只在使用者互動後離開仍空著、或嘗試送出時才成立，不再需要 `onBlur` 加 `touched` class（官方宣稱）

經過：表單一打開，每個必填欄位都是紅框，使用者還沒動手就被告知做錯了。`:user-invalid` 照瀏覽器的互動時機判斷，錯誤只在該出現的時候出現。ARIA 狀態仍需要一小段腳本同步。
%% line-end %%

### 細節（不索引）
- 對手組：播報時機或可靠度出錯
- 支援狀態：:user-valid／:user-invalid：Widely（2023-11-02）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:required-field-feedback:2" %%
## aria-invalid 依 :user-invalid 同步，不要用 checkValidity()
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：欄位起始設 `aria-invalid="false"`，在 blur 或送出失敗時依 `el.matches(':user-invalid')` 改成 `"true"`
- 被什麼擋：拿 `checkValidity()` 判斷時，使用者只是 Tab 經過沒碰的欄位，它就已經是 false，輔助技術會提早被告知錯誤（引用："deriving it from `:user-invalid`, not `checkValidity()`, which is already false when a user tabs through an untouched field."）
- 戰報：勝——以 `:user-invalid` 為準，讀屏聽到的錯誤時機與畫面一致（官方宣稱）

經過：畫面上的紅框等互動後才出現，但同步 ARIA 的腳本若用 `checkValidity()`，讀屏使用者一路 Tab 就一路聽到「無效」。兩邊要用同一個判準。另外 Firefox 和 Safari 會從載入就把空的必填欄位報成無效，所以起始值要明確設 `"false"`。
%% line-end %%

### 細節（不索引）
- 對手組：播報時機或可靠度出錯
- 支援狀態：:user-valid／:user-invalid：Widely（2023-11-02）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:required-field-feedback:3" %%
## 錯誤訊息只在欄位無效時才掛進 aria-describedby
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：欄位用 `data-error` 指向錯誤訊息的 `id`，由腳本只在欄位無效時把它列進 `aria-describedby`
- 被什麼擋：在標記裡就引用錯誤訊息，隱藏的訊息從頁面載入起就會被讀出來（引用："A reference in the markup would read the hidden message from page load."）
- 戰報：勝——訊息只在欄位無效時和欄位連結，讀屏在聚焦時才一併唸出（官方宣稱）

經過：錯誤訊息元素先寫在頁面上、用 CSS 藏著，描述也先掛好，使用者第一次聚焦就聽到「This field is required.」。改成無效時才掛，聽到的就是當下的狀態。
%% line-end %%

### 細節（不索引）
- 對手組：播報時機或可靠度出錯
- 支援狀態：:user-valid／:user-invalid：Widely（2023-11-02）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

另有 3 條未拆：錯誤改由全頁一個 polite live region 延遲播報，不讓每則錯誤自己當 live region（同 `mwg:accessible-error-announcement:3`）；必填星號要包 `aria-hidden="true"`，因為 `required` 已讓讀屏唸「required」；送出鈕保持可按，不要停用（按下時瀏覽器會觸發 `:user-invalid` 並聚焦第一個錯誤欄位）。
