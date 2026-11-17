---
guide: improve-text-layout-and-legibility
category: visual-design
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/visual-design/improve-text-layout-and-legibility.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 改善文字排版與易讀性

%% line-start id="mwg:improve-text-layout-and-legibility" %%
## 標題用 `text-wrap: balance` 讓每行長度接近
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`h1`–`h6`、副標、引言設 `text-wrap: balance`
- 被什麼擋：缺——指南只說它讓文字盡量平均分配到各行、外觀更對稱，沒說預設換行在哪個時刻出問題
- 戰報：部分改善——短標題各行長度接近；text-wrap: balance 為 Newly，不支援時退回一般換行（官方宣稱）

經過：兩行的標題，第一行滿滿、第二行只剩一個字。加上 balance 之後，兩行差不多長。
%% line-end %%

### 細節（不索引）
- 對手組：版面擠壓破壞可讀性
- 支援狀態：text-wrap: balance：Baseline Newly available（2024-05-13 起）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前標題斷行要手動插 `<br>` 或用 JS 平衡 → 現在新聞列表、卡片標題、多語系的行銷標語都能在任何寬度自動斷得整齊，不必為每種語言調整
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:improve-text-layout-and-legibility:2" %%
## 內文用 `text-wrap: pretty` 擋掉段落最後一行只剩一個字
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`p`、`blockquote`、`li` 等可能有長文字的元素設 `text-wrap: pretty`
- 被什麼擋：預設的貪婪換行讓段落最後一行常常只剩一個單字（孤字）（引用："It is specifically designed to prevent "orphans" (single words on the last line of a paragraph) and create a more pleasing visual "rag" for long blocks of text."）
- 戰報：部分改善——支援時段落結尾不再孤懸一字；Chrome、Edge、Safari 支援，Firefox 退回一般換行（官方宣稱）

經過：每段文章最後一行都只掛著一個詞，整頁看起來坑坑洞洞。
%% line-end %%

### 細節（不索引）
- 對手組：版面擠壓破壞可讀性
- 支援狀態：text-wrap: pretty：Limited availability，Supported by: Chrome 117, Edge 117, Safari 26；Unsupported in: Firefox
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前避免孤字只能手動加不換行空格 → 現在部落格、電子報、說明文件的段落可以由瀏覽器自動修整段尾，內容由 CMS 產生也一樣。Firefox 暫不支援
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:improve-text-layout-and-legibility:3" %%
## `balance` 與 `pretty` 只套在需要的元素上，不要全域套用
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`balance` 只給短的多行元素，`pretty` 只給可能有三行以上的段落；不要寫 `* { text-wrap: balance; }`
- 被什麼擋：`balance` 的二分搜尋很耗運算，而且超過行數上限（Chromium 約 6 行、Firefox 約 10 行）就退回一般換行；`pretty` 也比預設貴（引用："The iterative "binary search" algorithm used by browsers is computationally expensive."）
- 戰報：部分改善——效能成本只花在看得出效果的地方；balance 為 Newly（官方宣稱）

經過：為了省事把 balance 套到所有元素，文字很多的頁面排版變慢，長段落卻完全沒變化。
%% line-end %%

### 細節（不索引）
- 對手組：優化用過頭反傷
- 支援狀態：text-wrap: balance：Newly（2024-05-13 起）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:improve-text-layout-and-legibility:4" %%
## 有邊框或底色的元素不要用 `text-wrap: balance`
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：按鈕、標籤、有底色的標題框不套 `balance`
- 被什麼擋：`balance` 不改容器寬度，只改換行位置，容器尾端留下空白，有框的元素會看到一塊意外的空區（引用："Avoid elements that have visible boxes such as borders or backgrounds, as this can create unexpected visually empty areas in the layout."）
- 戰報：勝——框的大小與文字一致（官方宣稱）

經過：有底色的提示框套了 balance，文字兩行變得一樣短，右邊空出一大截底色。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：指南未給此情境的支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 另有 1 個糾錯提醒未拆：真的需要精細排版時才用 JS 函式庫，且可能拖慢效能
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
