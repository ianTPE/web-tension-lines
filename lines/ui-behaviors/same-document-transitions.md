---
guide: same-document-transitions
category: ui-behaviors
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-behaviors/same-document-transitions.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 同文件轉場

%% line-start id="mwg:same-document-transitions" %%
## 用 `startViewTransition()` 加共用的 `view-transition-name`，讓縮圖「長成」詳細頁主圖
- 做法：把 SPA 的視圖切換包進 `document.startViewTransition()`；列表項目與詳細頁主圖共用同一個 `view-transition-name`（列表各給唯一名稱再動態套到詳細頁，或反過來只在被選的項目上加名稱）
- 對手：從列表點進詳細頁時，縮圖直接消失、大圖瞬間出現在別處，使用者難以追蹤兩者的關係（引用："the thumbnail disappears and a new, larger image appears instantly elsewhere on the screen. This lack of continuity makes it harder for users to track relationships between elements."）
- 退路：保住主要行為——偵測不支援時直接執行 DOM 更新並切換視圖，功能完整只是沒有縮圖變形動畫
- 解鎖：單頁應用切換視圖時能自動比對共有元素的大小與位置差異，讓縮圖平滑變形成詳細頁主圖

經過：商品列表點進去，畫面一跳，眼睛得重新找剛剛點的那張圖。把更新包進轉場、給兩端同一個名字，圖就從原位飛到新位置。舊瀏覽器只是退回瞬間切換。
%% line-end %%

### 細節（不索引）
- 對手組：尺寸動畫只能跳變
- 支援狀態：View transitions：Baseline Newly available（2025-10-14 起）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前列表到詳細頁的「接續感」要動畫函式庫算 FLIP → 現在相簿、商品目錄、聯絡人清單可以幾行 JS 讓點到的那張卡片變形成詳細頁，不支援的瀏覽器照常切換
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:same-document-transitions:2" %%
## 同一個 `view-transition-name` 前後各只能有一個元素，轉場完要清掉
- 做法：確保轉場前後每個名稱只對應一個元素；用 `.selected` 臨時加上的名稱，在 `transition.finished` 之後移除
- 對手：同名元素有兩個以上時，DOM 直接更新、完全沒有轉場（引用："If there are 2 or more elements with a given `view-transition-name`, the DOM will be updated to the new state immediately, without a transition."）
- 退路：保住主要行為——不支援轉場的瀏覽器原本就直接更新 DOM，結束後清理名稱只保住支援環境後續轉場
- 解鎖：（缺）

經過：第一次點進去有動畫，回到列表再點另一張就沒了——上一次留下的名稱還掛在舊項目上，跟新項目撞名。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：View transitions：Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:same-document-transitions:3" %%
## 轉場不管焦點，切換視圖後要自己把焦點送到新標題
- 做法：在 DOM 更新後或 `transition.finished` 時，把焦點移到新視圖的標題或容器（加 `tabindex="-1"`）；不支援轉場的分支也要做
- 對手：焦點留在轉場中被隱藏或移除的元素上就會被丟棄，鍵盤與輔助技術使用者失去位置（引用："If focus remains on an element that is hidden or removed during the transition, focus is abandoned, leaving keyboard and assistive technology users without context."）
- 退路：保住主要行為——不支援轉場的分支同樣在 DOM 更新後移動焦點，舊瀏覽器的鍵盤與讀屏脈絡不丟失
- 解鎖：（缺）

經過：用鍵盤按下縮圖，畫面漂亮地變形成詳細頁，但焦點掉回頁首，下一個 Tab 從頭開始。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：View transitions：Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:same-document-transitions:4" %%
## 文字轉場用 `fit-content` 固定比例，避免快照被拉伸
- 做法：轉場的文字元素在新舊視圖都設 `width: fit-content`；比例會變的元素把 `::view-transition-old/new()` 設 `height: 100%`，必要時用 `object-fit`
- 對手：瀏覽器預設在一個會同時容納新舊快照的群組裡交叉淡化，群組被拉伸，快照跟著變形（引用："By default, the browser cross-fades the old and new snapshots within a group that stretches to fit both."）
- 退路：保住主要行為——尺寸與比例調整在無轉場時只是正常排版，不支援時直接切換視圖亦不變形
- 解鎖：（缺）

經過：標題從列表飛到詳細頁時被壓扁再撐開。快照是圖片，容器多寬它就被拉多寬。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：View transitions：Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 2 個糾錯提醒未拆：有進行中動畫的元素不要轉場（快照會讓動畫看起來暫停）；用 `prefers-reduced-motion` 關掉轉場動畫
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
