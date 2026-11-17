---
guide: scroll-position-aware-elements
category: ui-atoms
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/ui-atoms/scroll-position-aware-elements.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 知道捲動位置的元素

%% line-start id="mwg:scroll-position-aware-elements" %%
## 用 `scroll-state(scrollable: top)` 只在往下捲之後顯示「回到頂端」
- 做法：捲動容器設 `container-type: scroll-state`；浮動按鈕用 `position: sticky` 放在容器裡，預設隱藏，`@container scroll-state(scrollable: top)`（表示還能往上捲，也就是已經往下捲了）時顯示並滑入
- 對手：指南只說不必依賴 JavaScript 的 scroll 監聽器或 observer，沒說那些做法在哪個時刻出問題（引用："without relying on JavaScript scroll listeners or observers."）
- 退路：保住主要行為——不支援時用 IntersectionObserver 觀察頂端哨兵，保留動態顯示
- 解鎖：浮動控制項可用純 CSS 在容器離開頂端後顯示

經過：回到頂端的按鈕在頁首時沒有用，只是擋路。判斷「現在有沒有往下捲」以前要靠腳本，新查詢讓樣式自己問容器。
%% line-end %%

### 細節（不索引）
- 對手組：捲動連動效果靠JS監聽
- 支援狀態：Container scroll-state queries：Limited availability。Supported by: Chrome 144, Edge 144。Unsupported in: Firefox, Safari
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前「捲下去才出現」的浮動按鈕要寫監聽或哨兵 → 現在長文的回到頂端、長清單的浮動新增鈕、捲過開頭才出現的迷你標題列可以純 CSS 決定何時現身。目前僅 Chromium
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:scroll-position-aware-elements:2" %%
## 預設可見，只在支援時才改成預設隱藏
- 做法：按鈕的基礎樣式設成可見；在 `@supports (container-type: scroll-state)` 裡才改成 `visibility: hidden`，並寫顯示用的 scroll-state 查詢
- 對手：按鈕預設 `visibility: hidden`，不支援 scroll-state 的瀏覽器永遠不會把它顯示出來（引用："the floating element will remain invisible because of the default `visibility: hidden`."）
- 退路：保住主要行為——不支援時讓按鈕一律可見，失去依捲動位置切換
- 解鎖：（缺）

經過：漸進增強寫反了：「先藏起來，等查詢成立再顯示」，在查詢永遠不成立的瀏覽器裡就是永遠藏著。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：同 mwg:scroll-position-aware-elements，記 Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:scroll-position-aware-elements:3" %%
## 浮動按鈕下方要留空間，別蓋住最後幾個項目
- 做法：主內容底部留足夠的 padding 或 margin
- 對手：sticky 或浮動的按鈕浮在內容上，捲到底時最後幾個元素被它永久蓋住（引用："so that the last few elements are not permanently covered by the button when the user scrolls completely to the bottom."）
- 退路：不需要——支援狀態不適用，不必退路
- 解鎖：（缺）

經過：清單最後一項的刪除鈕剛好在回到頂端鈕底下，怎麼捲都按不到。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：padding／margin：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
