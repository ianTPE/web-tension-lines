---
guide: form-associated-custom-elements
category: html
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/html/form-associated-custom-elements.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 表單關聯自訂元素

%% line-start id="mwg:form-associated-custom-elements" %%
## 用 formAssociated 與 ElementInternals 讓自訂控制項自己送值，不要藏一個 input
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：類別加 `static formAssociated = true`，用 `setFormValue()` 送值、`setValidity()` 接上原生驗證，並實作 `formResetCallback`、`formDisabledCallback`、`formStateRestoreCallback`
- 被什麼擋：缺——指南只說不要退回隱藏的 `<input>`，列出 FACE 的好處（自己送值、參與驗證、反映表單狀態），沒說隱藏 input 在哪個時刻出錯
- 戰報：勝——FACE 已 Widely；元素自己送出值，無效時表單不會送出，`:invalid`／`:valid` 生效，reset、`fieldset[disabled]`、上一頁還原都像原生控制項（官方宣稱）

經過：自訂的評分元件要參與表單，傳統做法是旁邊藏一個 input 同步值。FACE 讓元素本身就是表單控制項，送值、驗證、重設、停用都走瀏覽器的路。指南也提醒，`:user-invalid` 在 FACE 上各瀏覽器還沒一致接好。
%% line-end %%

### 細節（不索引）
- 對手組：自製控制項丟掉原生行為
- 支援狀態：Form-associated custom elements：Widely（2023-03-27）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:form-associated-custom-elements:2" %%
## formDisabledCallback 只停用內部控制項，不要設宿主的 disabled
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在 `formDisabledCallback(disabled)` 裡停用 shadow 內的按鈕（或移出 Tab 順序並忽略輸入），宿主本身不碰
- 被什麼擋：在回呼裡替宿主加上 `disabled` 屬性，祖先 `<fieldset>` 重新啟用時宿主仍卡著自己的 `disabled`，永遠停用（引用："Do NOT toggle `disabled` on `this`, or a `<fieldset disabled>` toggle will leave the host permanently stuck with its own `disabled` attribute."）
- 戰報：勝——只停用內部控制項，fieldset 切換時能正常恢復，宿主也會自動符合 `:disabled`（官方宣稱）

經過：整個 fieldset 停用再啟用後，其他欄位都恢復了，只有自訂元件還是灰的、點不動。因為回呼把 disabled 寫到宿主上，那個屬性沒有人會拿掉。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：Form-associated custom elements：Widely（2023-03-27）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:form-associated-custom-elements:3" %%
## 不要用 ElementInternals 直接給可及名稱
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：處理互動或作為群組的自訂元素用 `ElementInternals` 設角色（例如 `role = 'group'`）與狀態，但除非元素自帶可見標籤，不透過它設可及名稱
- 被什麼擋：用 `ElementInternals` 設名稱，可能蓋掉使用端給的名稱，例如用 `<label for>` 標示的名稱（引用："this would likely override any accessible name set when using the custom element, such as by labelling the element using a HTML label's `for` attribute."）
- 戰報：勝——不預設名稱，使用端的 `<label>` 就是讀屏聽到的名稱（官方宣稱）

經過：元件內建一個「Rating」名稱，頁面上明明用 `<label for>` 標成「這次服務的滿意度」，讀屏卻唸出元件預設的那個。名稱留給使用端給。
%% line-end %%

### 細節（不索引）
- 對手組：可及名稱蓋掉可見文字
- 支援狀態：Form-associated custom elements：Widely（2023-03-27）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

另有 1 個糾錯提醒未拆：優先派送內建的 `input` 與 `change` 事件，不自創事件名。
