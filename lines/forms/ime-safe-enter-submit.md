---
guide: ime-safe-enter-submit
category: forms
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/forms/ime-safe-enter-submit.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 不打斷輸入法的 Enter 送出

%% line-start id="mwg:ime-safe-enter-submit" %%
## Enter 送出前先檢查 isComposing（加 keyCode 229），不在輸入法選字時送出
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在自訂的 Enter 送出 `keydown` 處理裡，`event.isComposing` 或 `event.keyCode === 229` 成立時直接 return，不呼叫 `form.requestSubmit()`；適用 `<textarea>` 與有自訂 Enter 處理的單行 `<input>`
- 被什麼擋：用輸入法打中文、日文、韓文時，Enter 是用來確認選字的；script 一收到 Enter 就送出，訊息在還沒選完字時就送出去（引用："the user's message is sent while they are still converting characters, resulting in incomplete, fragmented, or incorrect messages."）
- 戰報：部分改善——`isComposing` 為 Limited（Safari 不支援，且曾因事件順序問題讓它在 keydown 時已變回 false）；加上 `keyCode === 229` 的 fallback 可以可靠地擋住（官方宣稱）

經過：聊天室裡打「你好」，按 Enter 確認選字，訊息卻送出了一半的注音或假名。原生表單從 `<input>` 隱式送出時瀏覽器會自己避開，壞的是自訂的 keydown 處理。指南也提醒：把舊的 `keyCode === 13` 改寫成 `key === 'Enter'` 卻沒加這兩個檢查，反而會引入這個問題。
%% line-end %%

### 細節（不索引）
- 對手組：表單意外送出
- 支援狀態：api.KeyboardEvent.isComposing：Limited（Supported by: Chrome 56 (Jan 2017), Edge 79 (Jan 2020), and Firefox 31 (Jul 2014). Unsupported in: Safari.）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:ime-safe-enter-submit:2" %%
## 自訂 Enter 送出時呼叫 preventDefault()，避免送出兩次
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在 Enter 的 `keydown` 處理裡先呼叫 `event.preventDefault()`，再自行 `requestSubmit()`
- 被什麼擋：Enter 的預設動作在 `<textarea>` 會插入換行，在 `<form>` 裡的 `<input>` 會觸發瀏覽器的隱式送出，加上自己的送出就送了兩次（引用："in an `<input>` inside a `<form>` it triggers the browser's implicit submission, which would submit a second time."）
- 戰報：勝——擋掉預設動作後，送出只由自己的處理觸發一次（官方宣稱）

經過：搜尋列、行內改名欄位、指令面板常自己接 Enter，忘了擋預設動作，表單就被瀏覽器再送一次。`preventDefault()` 也讓 textarea 不會在送出前多插一行空白。
%% line-end %%

### 細節（不索引）
- 對手組：表單意外送出
- 支援狀態：不適用（指南未給 `preventDefault()` 支援資料；全篇唯一的支援資料是 isComposing）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

未拆：「一定要有 `<button type="submit">`，快捷鍵不能取代原生送出路徑」沒有說明缺了會怎樣。
