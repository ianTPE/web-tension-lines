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
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：捲動容器設 `container-type: scroll-state`；浮動按鈕用 `position: sticky` 放在容器裡，預設隱藏，`@container scroll-state(scrollable: top)`（表示還能往上捲，也就是已經往下捲了）時顯示並滑入
- 被什麼擋：指南只說不必依賴 JavaScript 的 scroll 監聽器或 observer，沒說那些做法在哪個時刻出問題（引用："without relying on JavaScript scroll listeners or observers."）
- 戰報：僵持——僅 Chrome／Edge 144；其他瀏覽器要嘛讓按鈕永遠顯示，要嘛用 IntersectionObserver 觀察頂端的哨兵元素切換 class（官方宣稱）

經過：回到頂端的按鈕在頁首時沒有用，只是擋路。判斷「現在有沒有往下捲」以前要靠腳本，新查詢讓樣式自己問容器。
%% line-end %%

### 細節（不索引）
- 對手組：捲動連動效果靠JS監聽
- 支援狀態：Container scroll-state queries：Limited availability。Supported by: Chrome 144, Edge 144。Unsupported in: Firefox, Safari
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前「捲下去才出現」的浮動按鈕要寫監聽或哨兵 → 現在長文的回到頂端、長清單的浮動新增鈕、捲過開頭才出現的迷你標題列可以純 CSS 決定何時現身。目前僅 Chromium
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:scroll-position-aware-elements:2" %%
## 預設可見，只在支援時才改成預設隱藏
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：按鈕的基礎樣式設成可見；在 `@supports (container-type: scroll-state)` 裡才改成 `visibility: hidden`，並寫顯示用的 scroll-state 查詢
- 被什麼擋：按鈕預設 `visibility: hidden`，不支援 scroll-state 的瀏覽器永遠不會把它顯示出來（引用："the floating element will remain invisible because of the default `visibility: hidden`."）
- 戰報：部分改善——不支援的瀏覽器裡按鈕一直在，功能保住，只是不會依捲動位置出現與消失（官方宣稱）

經過：漸進增強寫反了：「先藏起來，等查詢成立再顯示」，在查詢永遠不成立的瀏覽器裡就是永遠藏著。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：同 mwg:scroll-position-aware-elements，記 Limited
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:scroll-position-aware-elements:3" %%
## 浮動按鈕下方要留空間，別蓋住最後幾個項目
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：主內容底部留足夠的 padding 或 margin
- 被什麼擋：sticky 或浮動的按鈕浮在內容上，捲到底時最後幾個元素被它永久蓋住（引用："so that the last few elements are not permanently covered by the button when the user scrolls completely to the bottom."）
- 戰報：勝——捲到底時最後的內容露在按鈕上方（官方宣稱）

經過：清單最後一項的刪除鈕剛好在回到頂端鈕底下，怎麼捲都按不到。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：padding／margin：指南未給支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
