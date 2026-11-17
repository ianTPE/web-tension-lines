---
guide: equal-width-text-lines
category: visual-design
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/visual-design/equal-width-text-lines.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 等寬文字行

%% line-start id="mwg:equal-width-text-lines" %%
## 用 `text-fit` 讓海報式標題每一行自動撐滿寬度
- 做法：標題設 `text-fit: grow per-line-all 300%`，強制換行的每一行包成 `display: block; white-space: nowrap` 的 `<span>`；基礎 `font-size` 設成最小值，百分比當上限
- 對手：缺——指南只說瀏覽器在版面計算時縮放每一行，所以在調整大小、改文案、字型載入時都保持正確，沒說腳本量測在哪個時刻出錯
- 退路：失去主要好處——退回 `ResizeObserver` 腳本量測或流體字級，失去純排版自動等寬與自由換行支援
- 解鎖：用 `text-fit` 讓瀏覽器在排版時自動縮放每行撐滿容器，調整大小或改文案仍保持對齊

經過：活動頁主標想讓「夏日／音樂／祭」三行一樣寬、字級各不相同。以前改一個字就得重新量；現在瀏覽器每次排版都自己算。
%% line-end %%

### 細節（不索引）
- 對手組：尺寸不跟內容走
- 支援狀態：text-fit：Limited availability，Supported by: Chrome 150, Edge 150；Unsupported in: Firefox, Safari
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前等寬字級的標題要 fitty 這類函式庫或做成圖片 → 現在活動主視覺、雜誌封面式文章標題、可翻譯的海報標語都能用真文字排，換語言或改文案自動重排。目前僅 Chromium
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:equal-width-text-lines:2" %%
## 用 `per-line-all` 而不是 `per-line`，容器要有明確寬度
- 做法：關鍵字寫 `per-line-all`；標題容器給定 `inline-size`，不要是 `fit-content`／`max-content` 或依內容決定寬度的 flex／grid 項目
- 對手：`per-line` 會跳過最後一行與以強制換行結尾的行，每行一個區塊時什麼都不縮放；容器寬度依內容時 `text-fit` 也不起作用（引用："`per-line` skips the last line and any line ending in a forced break, so with one block per line it scales nothing."）
- 退路：保住主要行為——退回 JS 逐行量測縮放，不再跳過末行或強制換行
- 解鎖：（缺）

經過：照文件寫了 `text-fit`，畫面完全沒變，查半天才發現是關鍵字少了 `-all`，標題又放在一個 `fit-content` 的 flex 項目裡。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：text-fit：Limited availability（Chrome 150, Edge 150）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 交叉核對仲裁：退路改為「保住主要行為」

%% line-start id="mwg:equal-width-text-lines:3" %%
## 行距用 flex／grid 的 `gap` 與 `text-box` 控制，不要靠 `em` 或 `line-height`
- 做法：全部強制換行時，每行設 `text-box: trim-both cap alphabetic`，標題用 flex 或 grid 加 `gap` 排行距；有自由換行時不用 `text-box`，改由較小的 `line-height` 管
- 對手：`text-fit` 不改計算後的 `font-size`，以 `em` 寫的間距不會跟著放大；用 `line-height` 時，間距又會隨每一行的字級變大（引用："IMPORTANT: Note that computed `font-size` is unchanged, so `em` spacing does not scale."）
- 退路：失去主要好處——退回較小 line-height，行距仍隨各行字級變大
- 解鎖：（缺）

經過：放大後的第二行和第三行之間空出一大塊，第一行和第二行卻擠在一起。
%% line-end %%

### 細節（不索引）
- 對手組：版面依賴錯的量測
- 支援狀態：text-box：Limited availability，Supported by: Chrome 133, Edge 133, Safari 18.2；Unsupported in: Firefox
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 交叉核對仲裁：退路改為「失去主要好處」

%% line-start id="mwg:equal-width-text-lines:4" %%
## 退路腳本先全部讀、再全部寫，不要讀寫交錯
- 做法：先清掉舊的 `--text-fit-scale`，一次讀完所有行的 `offsetWidth` 與容器寬度，再一次寫入每行的縮放值；用 ResizeObserver 在尺寸改變與字型載入時重算
- 對手：在寫入迴圈裡讀 `lockup.clientWidth` 會每一行強制重排一次（引用："Interleaving them (e.g. reading lockup.clientWidth inside the write loop) forces one reflow per line."）
- 退路：不需要——支援狀態不適用，不必另設退路
- 解鎖：（缺）

經過：視窗一拉動，標題的縮放腳本讓整頁卡頓。
%% line-end %%

### 細節（不索引）
- 對手組：主執行緒被重活卡住
- 支援狀態：ResizeObserver：指南未給支援資料，記 不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 3 個糾錯提醒未拆：有自由換行時加 `text-wrap: balance` 或 `pretty` 避免孤字被過度放大；字級差異太小的行不適合做成等寬標題；放大的字視覺上會變粗，目前無法用 `font-weight` 抵銷
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
