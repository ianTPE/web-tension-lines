---
guide: scoped-component-transitions
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/scoped-component-transitions.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 元件範圍的轉場

%% line-start id="mwg:scoped-component-transitions" %%
## 用 `element.startViewTransition()` 把轉場關在元件裡，不再蓋住整頁
- 做法：在元件根元素上呼叫 `element.startViewTransition()`，子項目用 `view-transition-name: match-element`；重複出現的元件容器加 `view-transition-scope: all`，讓名稱不外洩
- 對手：`document.startViewTransition()` 把 `::view-transition` 疊層掛在 `:root`，轉場期間整頁點不到、不能同時跑兩個轉場，還會蓋住 `position: fixed` 標頭與開著的 popover（引用："blocks pointer events on the rest of the page, prevents concurrent transitions, and obscures `position: fixed` headers or open `[popover]` elements"）
- 退路：保住主要行為——偵測 Element.prototype 無此方法時直接執行 DOM 更新，不阻擋整頁也不播動畫
- 解鎖：把轉場限制在單一元件子樹內，讓多個元件能同時轉場且不遮住固定標頭或阻擋頁面的其餘互動

經過：側欄的清單在重排動畫，同時使用者想點頁首的按鈕卻點不到，打開的選單也被轉場蓋掉。把轉場範圍縮到元件本身，頁面其他地方不受影響；但目前只有 Chromium 做得到。
%% line-end %%

### 細節（不索引）
- 對手組：轉場被跳過或錯亂
- 支援狀態：Element-scoped view transitions：Limited availability，Supported by: Chrome 147, Edge 147；Unsupported in: Firefox, Safari（View transitions 本身為 Newly）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前一個小元件的動畫會凍住整頁 → 現在儀表板上多個卡片可以各自同時做排序、增刪動畫，頁首、浮動工具列照常可按。目前僅 Chromium
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 對手組由「新功能的副作用」改為「轉場被跳過或錯亂」

%% line-start id="mwg:scoped-component-transitions:2" %%
## `match-element` 要搬動既有節點，不能用 `innerHTML` 重建
- 做法：用 `view-transition-name: match-element` 時，重排或刪除都以搬動、移除既有 DOM 節點完成
- 對手：`match-element` 依 DOM 節點身分配對，重建出來的新節點對不上舊節點（引用："Preserve and move existing DOM nodes (rather than recreating them with `innerHTML`) when using `view-transition-name: match-element`, as `match-element` tracks DOM node identity."）
- 退路：保住主要行為——維持搬動既有節點，支援瀏覽器保住變形配對，無元件轉場的退路亦能正確更新清單
- 解鎖：（缺）

經過：排序後重新 render 整串清單，轉場裡的項目找不到前身，只剩淡入淡出。
%% line-end %%

### 細節（不索引）
- 對手組：重建DOM丟狀態
- 支援狀態：Element-scoped view transitions：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:scoped-component-transitions:3" %%
## 同一元件快速重複觸發轉場時，接住 `ready` 的 rejection
- 做法：每次 `element.startViewTransition()` 後加 `transition.ready.catch(() => {})`
- 對手：在同一個元素上再次呼叫會跳過進行中的轉場並讓 `ready` reject，沒接住就變成未處理的 promise 錯誤（引用："Re-triggering startViewTransition() on the same element skips the active transition and rejects `ready`."）
- 退路：保住主要行為——不支援元件轉場時直接跑 DOM 更新回呼不會產生 promise 錯誤，支援時接住即安全
- 解鎖：（缺）

經過：使用者連點「排序」，主控台冒出一串 unhandled rejection。
%% line-end %%

### 細節（不索引）
- 對手組：轉場被跳過或錯亂
- 支援狀態：Element-scoped view transitions：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 對手組由「新功能的副作用」改為「轉場被跳過或錯亂」

%% line-start id="mwg:scoped-component-transitions:4" %%
## 會裁切溢出的範圍元素不要設 `view-transition-name: none`
- 做法：讓範圍元素保留瀏覽器預設的自我參與（`view-transition-name: root`），由 `::view-transition-group-children(root)` 自動套 `overflow: clip`
- 對手：退出自我參與就會關掉自動溢出裁切，轉場中的子項目會溢出元件邊界（引用："opting out of self-participation disables automatic overflow clipping."）
- 退路：保住主要行為——不支援元件轉場時本就無快照疊層，照一般 CSS overflow 規則正常裁切子內容
- 解鎖：（缺）

經過：可捲動的清單卡片在重排時，項目飛出卡片外面，蓋在旁邊的內容上。
%% line-end %%

### 細節（不索引）
- 對手組：轉場被跳過或錯亂
- 支援狀態：Element-scoped view transitions：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 對手組由「新功能的副作用」改為「轉場被跳過或錯亂」

%% line-start id="mwg:scoped-component-transitions:5" %%
## 外層轉場要搬動元件時，包一層有名稱的 wrapper 並把內層設成 `view-transition-scope: all`
- 做法：範圍元素外包一層 wrapper 並給它 `view-transition-name`，範圍元素加 `view-transition-scope: all`；或讓外層捕捉子項目時改用巢狀轉場群組並手動補 `overflow: clip`
- 對手：從父元件或 document 發起的外層轉場，會把範圍元素和裡面所有東西一起捕捉並動畫（引用："the outer transition will capture and animate the scope element and everything inside it."）
- 退路：保住主要行為——不支援元件轉場時直接立即更新 DOM，不存在內外層轉場互搶捕捉的問題
- 解鎖：（缺）

經過：頁面切版的大轉場一開始，卡片內正在跑的小轉場被打斷，裡面的項目被外層抓去亂飛。
%% line-end %%

### 細節（不索引）
- 對手組：轉場被跳過或錯亂
- 支援狀態：Element-scoped view transitions：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 2 個糾錯提醒未拆：用 `prefers-reduced-motion` 關掉轉場動畫；刪除聚焦中的項目時在更新回呼裡把焦點移到相鄰項目
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 對手組由「新功能的副作用」改為「轉場被跳過或錯亂」
