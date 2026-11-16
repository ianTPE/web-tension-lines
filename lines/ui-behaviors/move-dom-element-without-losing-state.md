---
guide: move-dom-element-without-losing-state
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/move-dom-element-without-losing-state.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 搬動 DOM 元素而不丟狀態

%% line-start id="mwg:move-dom-element-without-losing-state" %%
## 用 `moveBefore()` 搬元素，iframe 不重載、焦點不丟
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`newParent.moveBefore(element, null)` 取代 `appendChild()`／`insertBefore()`；先用 `'moveBefore' in Element.prototype` 偵測，不支援時退回 `insertBefore()`
- 被什麼擋：傳統搬法其實是先移除再插入，會重設許多內部狀態：`<iframe>` 重新載入、CSS 動畫重頭開始、輸入欄位失去焦點（引用："causing `<iframe>` elements to reload, CSS animations to restart, and input fields to lose focus"）
- 戰報：部分改善——原子性的搬移，跳過移除與插入步驟，狀態全部保住；`moveBefore()` 為 Limited，Safari 退回傳統搬法，狀態照樣被重設（官方宣稱）

經過：把正在播的影片或填到一半的表單換個位置，以前等於重建一次。`moveBefore()` 讓「搬家」真的只是搬家。
%% line-end %%

### 細節（不索引）
- 對手組：重建DOM丟狀態
- 支援狀態：moveBefore()：Limited availability，Supported by: Chrome 133, Edge 133, Firefox 144；Unsupported in: Safari
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前元素一搬就重置 → 現在影片可以從文章內「浮出」到角落小窗再放回來不中斷，嵌入的地圖或聊天 iframe 能在側欄與主區之間切換位置。Safari 仍會重置
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:move-dom-element-without-losing-state:2" %%
## 自訂元素被 `moveBefore()` 搬動時要實作 `connectedMoveCallback()`
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：自訂元素裡依位置更新狀態的邏輯放進 `connectedMoveCallback()`
- 被什麼擋：用 `moveBefore()` 搬自訂元素時，`connectedCallback` 與 `disconnectedCallback` 都不會觸發，寫在裡面的邏輯不會跑（引用："their `connectedCallback` and `disconnectedCallback` lifecycle methods will **not** be fired"）
- 戰報：部分改善——搬動時有專屬回呼可以更新與新位置相關的狀態（官方宣稱）

經過：元件靠「連上 DOM」來偵測父層並初始化，換成原子搬移後這個訊號消失了。
%% line-end %%

### 細節（不索引）
- 對手組：生命週期假設錯
- 支援狀態：moveBefore()：Limited
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 另有 3 個糾錯提醒未拆：搬動不能讓焦點掉回 `<body>`；盡量由使用者觸發搬動；依序閱讀的內容搬動會打亂讀屏順序，重要搬動用 live region 確認
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
