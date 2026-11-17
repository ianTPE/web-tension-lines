---
guide: custom-elements
category: html
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/html/custom-elements.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 自訂元素

%% line-start id="mwg:custom-elements" %%
## 用 connectedMoveCallback 接住 moveBefore() 的搬移，擋掉搬一次就重來
- 做法：自訂元素定義 `connectedMoveCallback`，元素被 `Node.moveBefore()` 搬動時改跑這個回呼，不跑 disconnect／connect
- 對手：一般搬動會先 `disconnectedCallback` 再 `connectedCallback`，昂貴或看得出來的 setup／teardown 整套重跑；`connectedMoveCallback` 存在的理由就是讓狀態、焦點、iframe／媒體播放撐過搬移（引用："this callback fires *instead of* `disconnectedCallback` → `connectedCallback`, so state, focus, and iframe/media playback survive the move."）
- 退路：沒說——指南未交代不支援 `moveBefore()` 時怎麼辦
- 解鎖：自訂元素可在搬移時保留狀態、焦點與 iframe／媒體播放

經過：元件裡有影片或 iframe，拖到別的欄位就整個重新初始化，播放中斷、焦點掉了。`moveBefore()` 加上 `connectedMoveCallback` 讓搬移成為一件獨立的事，元件可以只更新位置相關的東西。
%% line-end %%

### 細節（不索引）
- 對手組：重建DOM丟狀態
- 支援狀態：不適用（本指南未附支援資料；`moveBefore()` 在 `mwg:drag-and-drop` 記為 Limited）
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：包著播放器、地圖、編輯器的自訂元素可以在版面間自由搬動（拖到側欄、彈出成浮動視窗再放回）而不重新載入，可重排的工作區元件真正可行。支援度依 moveBefore()，見 mwg:drag-and-drop
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:custom-elements:2" %%
## connectedCallback 要能重跑，teardown 寫在 disconnectedCallback
- 做法：`connectedCallback` 的 setup 寫成冪等；全域監聽、計時器、observer 在 `disconnectedCallback` 移除，但不當成永久銷毀
- 對手：`connectedCallback` 每次插入都會觸發，搬動元素就再跑一次；不在 disconnect 時清掉全域監聽與計時器就會洩漏（引用："It fires on every insertion, so moving the element re-runs it."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：把 `connectedCallback` 當成「只跑一次的初始化」，元素一被移動就再掛一次監聽，事件觸發兩遍；拿掉時沒清計時器，背景持續跑。指南把它當成「每次接上都會跑」來設計。
%% line-end %%

### 細節（不索引）
- 對手組：生命週期假設錯
- 支援狀態：不適用（本指南未附支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:custom-elements:3" %%
## 生命週期回呼與 observedAttributes 要在 define() 之前就寫好
- 做法：`static observedAttributes` 與所有生命週期方法在呼叫 `customElements.define()` 前就放在類別上
- 對手：`define()` 只在註冊時讀一次這些設定，之後才加上的回呼或屬性清單會被默默忽略，`attributeChangedCallback` 永遠不觸發（引用："`attributeChangedCallback` never fires unless `observedAttributes` was already present at `define()` time."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：先 `define()`，之後才在類別上補 `observedAttributes` 或掛回呼，改屬性時元件毫無反應，也沒有錯誤可查。註冊是一次快照，要在那之前定型。
%% line-end %%

### 細節（不索引）
- 對手組：生命週期假設錯
- 支援狀態：不適用（本指南未附支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:custom-elements:4" %%
## 升級時屬性可能已在、子節點可能還沒到，用 slotchange 與 attributeChangedCallback 補
- 做法：constructor 先呼叫 `super()`；在 `connectedCallback` 讀既有屬性同步初始狀態；用 `slotchange` 監看子節點、`attributeChangedCallback` 監看屬性，不忽略之後的觸發
- 對手：元素可能在類別註冊前就已在 DOM 裡，升級時屬性和子節點早就存在；反過來，長清單的子節點在 `connectedCallback` 時可能還沒解析完（引用："the HTML parser can yield mid-parse of long child lists, so the callback sometimes runs before every child is attached."）；在 `super()` 之前碰 `this` 會丟 `ReferenceError`
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：伺服器輸出的元素在腳本晚載時才升級，元件假設自己是空的、把既有內容蓋掉；或在 `connectedCallback` 數子節點，偶爾只數到一半。改成「升級時讀現況、之後靠事件補」就不受時序影響。
%% line-end %%

### 細節（不索引）
- 對手組：生命週期假設錯
- 支援狀態：不適用（本指南未附支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:custom-elements:5" %%
## 用延遲的 opacity 動畫隱藏未定義元素，不要用 visibility: hidden 硬藏
- 做法：`my-element:not(:defined)` 設 `opacity: 0` 並加一個 2 秒後轉為不透明的動畫；只對需要的元素或子樹（`:has(:not(:defined))`）設，不對整個 `body`
- 對手：硬藏未升級的元素時，腳本一旦沒載入或載得慢，內容就永遠看不到；把守衛設在整個 `body`，一個不重要的小工具就會拖住整頁繪製（引用："so a failed or slow script never hides content for good."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：為了避免元件升級前的閃爍，在 `:not(:defined)` 寫 `visibility: hidden`，結果分享按鈕的腳本被擋掉時整塊內容永遠空白。改成延遲淡入，最壞情況只是晚兩秒出現。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：不適用（本指南未附支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

另有 3 個糾錯提醒未拆：只用於樣式的內部狀態改用 custom states（`:state()`）而非反射合成屬性（指南沒說合成屬性在哪個時刻出錯）；不要用自己的屬性遮蔽 `style`、`id`、`slot` 等全域屬性；setter 寫屬性會重入 `attributeChangedCallback`，要比對新舊值。
