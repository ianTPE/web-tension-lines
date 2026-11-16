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
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：每個項目給唯一的 `view-transition-name`，再共用 `view-transition-class: list-item`；用 `::view-transition-group(.list-item)` 設時長與緩動，`::view-transition-new(.list-item):only-child`／`::view-transition-old(.list-item):only-child` 做新增與移除的進出場；DOM 更新包進 `document.startViewTransition()`
- 被什麼擋：指南只說沒有 class 時要為每個名稱各寫一次轉場邏輯，沒說重複在哪個時刻造成可觀察的問題（引用："define that logic once in CSS rather than repeating it for every unique `view-transition-name`"）
- 戰報：部分改善——整組元素共用一份轉場樣式，新增、移除、重排都有動畫；兩者皆 Newly，不支援時直接更新 DOM、沒有動畫（官方宣稱）

經過：清單有幾十個項目，每個都要自己的名字才能被追蹤，但動畫應該只寫一次。class 把「哪個是哪個」和「怎麼動」分開。
%% line-end %%

### 細節（不索引）
- 對手組：樣式邏輯到處重複
- 支援狀態：View transitions：Newly（2025-10-14）；view-transition-class：Newly（2025-10-14）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前清單增刪重排的動畫要 FLIP 函式庫 → 現在待辦清單、購物車、看板欄可以讓新項目滑入、刪掉的滑出、其他自動補位，只寫一組 CSS
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:group-element-transitions:2" %%
## 轉場期間讓沒參與的元素仍可操作
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`::view-transition { pointer-events: none; }`，並在只轉場特定元素時設 `:root { view-transition-name: none; }` 關掉預設的 root 轉場
- 被什麼擋：轉場期間畫面是覆蓋在上面的快照，元素無法互動；root 轉場還會在兩張相同的整頁快照之間轉場，整頁都點不到（引用："during the transition, elements are not interactive"）
- 戰報：部分改善——沒參與轉場的控制項在動畫期間仍可點擊（官方宣稱）

經過：只是一個清單項目在動，使用者卻發現整頁按鈕在那半秒都沒反應。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：View transitions：Newly
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
