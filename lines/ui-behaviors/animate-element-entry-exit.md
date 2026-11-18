---
guide: animate-element-entry-exit
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/animate-element-entry-exit.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 元素進場與離場動畫

%% line-start id="mwg:animate-element-entry-exit" %%
## 用 `@starting-style` 與 `allow-discrete` 讓元素出現與 `display: none` 都能過渡
- 做法：基礎樣式寫最終值；`@starting-style` 寫進場的起點；`transition` 列入 `display`，另寫一條 `transition-behavior: allow-discrete`；`[hidden]` 寫離場的終點；用 `appendChild()` 插入的元素一樣靠 `@starting-style` 進場
- 對手：CSS transition 以前無法對剛加入 DOM、或 `display` 從 `none` 變化的元素做動畫：瀏覽器跳過元素的第一次樣式更新（引用："Browsers skip transitions on an element's first style update (initial render or `display: none` change) unless this is provided."）
- 退路：保住主要行為——Firefox 離場退回 `data-closing` 搭 `getAnimations()`，仍保住進離場動畫但須靠 JS
- 解鎖：用 `@starting-style` 與 `allow-discrete` 讓 `display: none` 切換與新插入元素都能宣告式過渡

經過：切 `hidden` 屬性，元素就瞬間出現或消失，transition 寫了也沒用。現在進場有起點、離場可以把 `display` 留到動畫結束，只是 Firefox 的離場還得靠腳本。
%% line-end %%

### 細節（不索引）
- 對手組：尺寸動畫只能跳變
- 支援狀態：@starting-style：Newly（2024-08-06）；transition-behavior：Newly（2024-08-06）；transitionable display：Limited availability，Supported by: Chrome 117, Edge 117, Safari 18，Unsupported in: Firefox
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前切 `hidden` 只能瞬間出現消失，要動畫就得 JS 先改 class、等一個影格再加動畫 class → 現在通知、展開的說明、篩選結果的卡片可以只切 `hidden` 屬性就淡入淡出。Firefox 的離場仍需 JS 退路
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:animate-element-entry-exit:2" %%
## 不要只靠 `CSS.supports()` 判斷能不能過渡 `display`
- 做法：建一個暫時的探針元素，設好 `transition: display 1s allow-discrete` 後改成 `display: none`，讀計算值是否仍為 `block` 來判斷；不支援時走 `data-closing` 退路
- 對手：Firefox 129+ 認得 `transition-behavior: allow-discrete`（`CSS.supports()` 回傳 true），實際上卻不過渡 `display`，元素離場時立刻消失（引用："Firefox 129+ parses `transition-behavior: allow-discrete` (`CSS.supports('transition-behavior', 'allow-discrete')` returns `true`) without actually transitioning the `display` property"）
- 退路：保住主要行為——改以暫時探針實測 `display` 計算值，讓 Firefox 正確分流走 `data-closing` 離場退路
- 解鎖：（缺）

經過：功能偵測說「支援」，使用者看到的卻是元素直接消失。這次瀏覽器認得語法，但沒有做到語法承諾的事。
%% line-end %%

### 細節（不索引）
- 對手組：功能偵測不可靠
- 支援狀態：transitionable display：Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:animate-element-entry-exit:3" %%
## `allow-discrete` 不要寫進 `transition` 簡寫
- 做法：另寫一條 `transition-behavior: allow-discrete`，放在 `transition` 之後
- 對手：把 `allow-discrete` 寫進 `transition` 簡寫，舊瀏覽器會忽略整條 `transition` 宣告（引用："it will make older browsers ignore the entire `transition` declaration."）
- 退路：保住主要行為——拆開宣告後，舊瀏覽器仍保留透明度等一般屬性過渡而不整條丟棄
- 解鎖：（缺）

經過：為了一個新關鍵字，舊瀏覽器連透明度的淡入都一起丟掉。
%% line-end %%

### 細節（不索引）
- 對手組：不認得的語法讓整條規則失效
- 支援狀態：transition-behavior：Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 對手組由「新功能的副作用」改為「不認得的語法讓整條規則失效」

%% line-start id="mwg:animate-element-entry-exit:4" %%
## 移除節點前先觸發離場，等動畫結束再 `remove()`
- 做法：先設 `element.hidden = true` 觸發離場，再用 `Promise.race` 等 `Promise.allSettled(getAnimations().map(a => a.finished))` 與 2 秒保險逾時，最後才 `element.remove()`
- 對手：`element.remove()` 立即生效，不會觸發 CSS 過渡（引用："Since `element.remove()` is instantaneous and doesn't trigger a CSS transition on its own"）
- 退路：保住主要行為——不支援 `display` 離場過渡的瀏覽器結合 `data-closing` 退路仍可等動畫結束再移除
- 解鎖：（缺）

經過：刪掉一則通知時寫好的淡出從來沒出現過，因為節點在動畫開始前就不在了。
%% line-end %%

### 細節（不索引）
- 對手組：尺寸動畫只能跳變
- 支援狀態：@starting-style、transition-behavior：Newly（本指南未給 `getAnimations()` 支援資料）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 2 個糾錯提醒未拆：頂層元素要在 `transition` 列入 `overlay`（見 mwg:animate-to-from-top-layer）；`@starting-style` 不能拿來寫離場
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
