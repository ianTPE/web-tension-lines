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
- 做法：`newParent.moveBefore(element, null)` 取代 `appendChild()`／`insertBefore()`；先用 `'moveBefore' in Element.prototype` 偵測，不支援時退回 `insertBefore()`
- 對手：傳統搬法其實是先移除再插入，會重設許多內部狀態：`<iframe>` 重新載入、CSS 動畫重頭開始、輸入欄位失去焦點（引用："causing `<iframe>` elements to reload, CSS animations to restart, and input fields to lose focus"）
- 退路：失去主要好處——Safari 退回 insertBefore() 雖能完成搬動，但 iframe、動畫與焦點狀態仍會重置
- 解鎖：將已有狀態的 DOM 元素直接搬進新父層，維持 iframe、CSS 動畫與輸入框焦點不斷線重設

經過：把正在播的影片或填到一半的表單換個位置，以前等於重建一次。`moveBefore()` 讓「搬家」真的只是搬家。
%% line-end %%

### 細節（不索引）
- 對手組：重建DOM丟狀態
- 支援狀態：moveBefore()：Limited availability，Supported by: Chrome 133, Edge 133, Firefox 144；Unsupported in: Safari
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前元素一搬就重置 → 現在影片可以從文章內「浮出」到角落小窗再放回來不中斷，嵌入的地圖或聊天 iframe 能在側欄與主區之間切換位置。Safari 仍會重置
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:move-dom-element-without-losing-state:2" %%
## 自訂元素被 `moveBefore()` 搬動時要實作 `connectedMoveCallback()`
- 做法：自訂元素裡依位置更新狀態的邏輯放進 `connectedMoveCallback()`
- 對手：用 `moveBefore()` 搬自訂元素時，`connectedCallback` 與 `disconnectedCallback` 都不會觸發，寫在裡面的邏輯不會跑（引用："their `connectedCallback` and `disconnectedCallback` lifecycle methods will **not** be fired"）
- 退路：保住主要行為——Safari 退回 insertBefore() 時仍觸發既有連接與斷開生命週期回呼，狀態更新照常執行
- 解鎖：（缺）

經過：元件靠「連上 DOM」來偵測父層並初始化，換成原子搬移後這個訊號消失了。
%% line-end %%

### 細節（不索引）
- 對手組：生命週期假設錯
- 支援狀態：moveBefore()：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 3 個糾錯提醒未拆：搬動不能讓焦點掉回 `<body>`；盡量由使用者觸發搬動；依序閱讀的內容搬動會打亂讀屏順序，重要搬動用 live region 確認
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
