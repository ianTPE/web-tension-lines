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
- 做法：在自訂的 Enter 送出 `keydown` 處理裡，`event.isComposing` 或 `event.keyCode === 229` 成立時直接 return，不呼叫 `form.requestSubmit()`；適用 `<textarea>` 與有自訂 Enter 處理的單行 `<input>`
- 對手：用輸入法打中文、日文、韓文時，Enter 是用來確認選字的；script 一收到 Enter 就送出，訊息在還沒選完字時就送出去（引用："the user's message is sent while they are still converting characters, resulting in incomplete, fragmented, or incorrect messages."）
- 退路：保住主要行為——Safari 上 `isComposing` 會提早重置，改用 `keyCode === 229` 或時間戳視窗仍擋得住選字時的送出
- 解鎖：以前無法知道使用者正在用輸入法選字，Enter 一到就送出；現在能用 `isComposing` 或 `keyCode === 229` 判斷並等選字完成

經過：聊天室裡打「你好」，按 Enter 確認選字，訊息卻送出了一半的注音或假名。原生表單從 `<input>` 隱式送出時瀏覽器會自己避開，壞的是自訂的 keydown 處理。指南也提醒：把舊的 `keyCode === 13` 改寫成 `key === 'Enter'` 卻沒加這兩個檢查，反而會引入這個問題。
%% line-end %%

### 細節（不索引）
- 對手組：表單意外送出
- 支援狀態：api.KeyboardEvent.isComposing：Limited（Supported by: Chrome 56 (Jan 2017), Edge 79 (Jan 2020), and Firefox 31 (Jul 2014). Unsupported in: Safari.）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:ime-safe-enter-submit:2" %%
## 自訂 Enter 送出時呼叫 preventDefault()，避免送出兩次
- 做法：在 Enter 的 `keydown` 處理裡先呼叫 `event.preventDefault()`，再自行 `requestSubmit()`
- 對手：Enter 的預設動作在 `<textarea>` 會插入換行，在 `<form>` 裡的 `<input>` 會觸發瀏覽器的隱式送出，加上自己的送出就送了兩次（引用："in an `<input>` inside a `<form>` it triggers the browser's implicit submission, which would submit a second time."）
- 退路：不需要——`preventDefault()` 是既有 DOM 行為，不涉及瀏覽器功能支援
- 解鎖：（缺）

經過：搜尋列、行內改名欄位、指令面板常自己接 Enter，忘了擋預設動作，表單就被瀏覽器再送一次。`preventDefault()` 也讓 textarea 不會在送出前多插一行空白。
%% line-end %%

### 細節（不索引）
- 對手組：表單意外送出
- 支援狀態：不適用（指南未給 `preventDefault()` 支援資料；全篇唯一的支援資料是 isComposing）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

未拆：「一定要有 `<button type="submit">`，快捷鍵不能取代原生送出路徑」沒有說明缺了會怎樣。
