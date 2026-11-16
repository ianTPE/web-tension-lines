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

%% line-start id="mwg:required-field-feedback:4" %%
## 錯誤用全頁一個 polite live region 延遲播報
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：欄位離開或改變時，把錯誤送進全頁共用的 polite live region，延遲到下一個欄位播報完；失敗送出後聚焦第一個無效欄位
- 被什麼擋：每則錯誤各自當 live region，只是被顯示而不是文字改變時，讀屏不一定會播；同時播報又會蓋過下一個欄位（引用："a live region that is shown, rather than changed, isn't announced reliably."）
- 戰報：勝——共用區域的文字確實改變，延遲後錯誤能被聽到，也不和焦點欄位搶話（官方宣稱）

經過：與 `mwg:accessible-error-announcement:3` 同一個對手。錯誤區域要在頁面載入時就存在，更新文字才可靠，不是把隱藏元素切換成可見。
%% line-end %%

### 細節（不索引）
- 對手組：播報時機或可靠度出錯
- 支援狀態：:user-valid／:user-invalid：Widely（2023-11-02）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

%% line-start id="mwg:required-field-feedback:5" %%
## 必填星號加 aria-hidden，避免重複播報
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：視覺必填標記用 `<span aria-hidden="true">*</span>`，在表單前解釋一次星號意義，欄位本身保留 `required`
- 被什麼擋：`required` 已讓讀屏播報必填，星號再進無障礙樹會多出無意義的「星號」或重複狀態（引用："wrap it in `<span aria-hidden="true">*</span>`, because the `required` attribute already makes screen readers announce "required"."）
- 戰報：勝——視覺使用者看得到星號，讀屏只播報一次 required（官方宣稱）

經過：星號是給眼睛看的額外提示，程式狀態已經由 `required` 表達，不必讓輔助技術再讀一遍符號。
%% line-end %%

### 細節（不索引）
- 對手組：播報過量
- 支援狀態：:user-valid／:user-invalid：Widely；`required`／`aria-hidden` 本指南未另列支援資料
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏

%% line-start id="mwg:required-field-feedback:6" %%
## 送出鈕保持可按，讓瀏覽器揭示所有必填錯誤
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：表單尚未有效時也保持送出鈕啟用；按下後由瀏覽器對空的必填欄位觸發 `:user-invalid` 並聚焦第一個錯誤
- 被什麼擋：停用送出鈕會讓使用者無法主動要求驗證，也看不到按下後應出現的錯誤與焦點導引（引用："Unlike `disabled` buttons, keep your submit button enabled. If the user clicks it, the browser will automatically trigger `:user-invalid` on all empty required fields and focus the first one."）
- 戰報：勝——使用者按送出就知道哪裡未完成，第一個錯誤欄位直接取得焦點（官方宣稱）

經過：灰色送出鈕只告訴人「還不能送」，沒說缺什麼。讓按鈕可按，瀏覽器才能執行內建的錯誤揭露流程。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：:user-valid／:user-invalid：Widely（2023-11-02）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏
