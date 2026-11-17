---
guide: group-element-transitions
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/group-element-transitions.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 新增、移除、重排時平滑重排卡片與清單

%% line-start id="mwg:group-element-transitions" %%
## 用 `view-transition-class` 一次定義整組元素的轉場
- 做法：每個項目給唯一的 `view-transition-name`，再共用 `view-transition-class: list-item`；用 `::view-transition-group(.list-item)` 設時長與緩動，`::view-transition-new(.list-item):only-child`／`::view-transition-old(.list-item):only-child` 做新增與移除的進出場；DOM 更新包進 `document.startViewTransition()`
- 對手：指南只說沒有 class 時要為每個名稱各寫一次轉場邏輯，沒說重複在哪個時刻造成可觀察的問題（引用："define that logic once in CSS rather than repeating it for every unique `view-transition-name`"）
- 退路：保住主要行為——不支援 view-transition-class 時忽略該樣式，不支援轉場則直接更新 DOM 維持功能
- 解鎖：群組內多個元素共享同一套 CSS 轉場邏輯，不必為每個唯一名稱重複撰寫動畫規則

經過：清單有幾十個項目，每個都要自己的名字才能被追蹤，但動畫應該只寫一次。class 把「哪個是哪個」和「怎麼動」分開。
%% line-end %%

### 細節（不索引）
- 對手組：樣式邏輯到處重複
- 支援狀態：View transitions：Newly（2025-10-14）；view-transition-class：Newly（2025-10-14）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前清單增刪重排的動畫要 FLIP 函式庫 → 現在待辦清單、購物車、看板欄可以讓新項目滑入、刪掉的滑出、其他自動補位，只寫一組 CSS
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:group-element-transitions:2" %%
## 轉場期間讓沒參與的元素仍可操作
- 做法：`::view-transition { pointer-events: none; }`，並在只轉場特定元素時設 `:root { view-transition-name: none; }` 關掉預設的 root 轉場
- 對手：轉場期間畫面是覆蓋在上面的快照，元素無法互動；root 轉場還會在兩張相同的整頁快照之間轉場，整頁都點不到（引用："during the transition, elements are not interactive"）
- 退路：保住主要行為——不支援轉場的瀏覽器直接更新 DOM，支援時關掉 root 轉場並停用快照指標即可互動
- 解鎖：（缺）

經過：只是一個清單項目在動，使用者卻發現整頁按鈕在那半秒都沒反應。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：View transitions：Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
