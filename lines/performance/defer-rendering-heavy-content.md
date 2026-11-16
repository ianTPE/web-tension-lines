---
guide: defer-rendering-heavy-content
category: performance
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/performance/defer-rendering-heavy-content.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 延後渲染沉重內容

%% line-start id="mwg:defer-rendering-heavy-content" %%
## 用 content-visibility: auto 讓首屏以下的重區塊等捲近了才排版繪製
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：對確定在首屏以下、內部 DOM 很深的大區塊（無限捲動的卡片、留言串、頁尾重區）加 `content-visibility: auto`
- 被什麼擋：內容很多的頁面（無限捲動、複雜儀表板、長文）初次渲染很慢、互動遲鈍（引用："Web pages with extensive content—such as infinite scrolls, complex dashboards, or dense articles can suffer from slow initial rendering and sluggish interactions."）
- 戰報：部分改善——瀏覽器把畫面外區塊的排版與繪製延到捲近時才做；不支援的瀏覽器忽略此屬性，照常渲染，只是失去效能好處（官方宣稱）

經過：整頁幾百張卡片在載入時全部排版繪製，首屏出得慢、點擊也卡。加上 `content-visibility: auto` 後，畫面外的區塊先跳過，捲到附近才算。
%% line-end %%

### 細節（不索引）
- 對手組：工作花在看不到的地方
- 支援狀態：content-visibility：Newly available（2025-09-15）。Supported by: Chrome 108, Edge 108, Firefox 130, Safari 26
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：一頁放完整本手冊、整年的週記或上千則留言也能秒開，不必為了效能做分頁或虛擬捲動
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:defer-rendering-heavy-content:2" %%
## content-visibility: auto 一定要配 contain-intrinsic-size
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：替每個 `content-visibility: auto` 區塊寫 `contain-intrinsic-size: auto none auto 150px` 這類預估尺寸，`auto` 讓瀏覽器記住渲染過的真實尺寸
- 被什麼擋：沒給預估尺寸時，畫面外的區塊被收成 0px 高，捲動時版面大幅位移、捲軸亂跳（引用："Failure to do so forces the browser to collapse the element to a 0px height when off-screen, causing severe layout shifting and scrollbar jumping as the user scrolls."）
- 戰報：部分改善——有預估尺寸佔位，捲動時不再跳動，渲染過的區塊離開畫面後沿用記住的尺寸（官方宣稱）

經過：只加 `content-visibility: auto`，每個區塊進出畫面時高度在 0 和真實值之間切換，捲軸長度一直變。預估尺寸讓它們在被跳過時仍佔著位置。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：content-visibility：Newly available（同上）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:defer-rendering-heavy-content:3" %%
## 首屏內的元素不要加 content-visibility: auto
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：只對初始視窗以外的區塊套 `content-visibility: auto`，首屏內的元素不套
- 被什麼擋：套在首屏元素上，瀏覽器得先判斷可見範圍才渲染，反而拖慢關鍵的頁面載入（引用："Doing so forces the browser to evaluate visibility boundaries before rendering, which paradoxically delays critical page load performance."）
- 戰報：部分改善——只對首屏以下套用，首屏照常立即渲染（官方宣稱）

經過：為了省事把整頁每個 section 都加上同一個 class，結果首屏也要先過一次可見性判斷，最需要快的那一塊反而變慢。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：content-visibility：Newly available（同上）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:defer-rendering-heavy-content:4" %%
## 用 content-visibility: hidden 藏起來但保留渲染狀態，切換時立即顯示
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：對初始隱藏的重區塊（大型資料表的額外列、切換的視圖）設 `content-visibility: hidden`，要顯示時改成 `visible` 或 `auto`；以 `@supports (content-visibility: hidden)` 包住，預設仍是 `display: none`
- 被什麼擋：缺——指南只說它比 `display: none` 好（"superior to `display: none`"），沒說 `display: none` 在切換時具體出了什麼事
- 戰報：部分改善——隱藏時跳過排版但保留狀態，切換幾乎即時、不產生結構位移；不支援的瀏覽器會把 `hidden` 的元素整個顯示出來，所以要以 `@supports` 退回 `display: none`（官方宣稱）

經過：在幾個視圖間來回切換時，每次重新顯示都要重算。改用 `content-visibility: hidden`，隱藏期間不排版也不繪製，渲染結果留著，顯示時直接拿來用。
%% line-end %%

### 細節（不索引）
- 對手組：工作花在看不到的地方
- 支援狀態：content-visibility：Newly available（同上）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：資料表的「展開全部列」、設定頁的多個分頁可以預先建好、藏著不算，按下去立刻出現。對手的具體描述見 mwg:faster-spa-view-transitions
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:defer-rendering-heavy-content:5" %%
## content-visibility 可能把內容移出無障礙樹與頁內搜尋
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：需要在隱藏時仍能被搜尋到的內容改用 `hidden="until-found"`，不用 `content-visibility: hidden`；用了 `content-visibility: auto` 時只用鍵盤實際走一遍，確認畫面外的節點仍能依序到達
- 被什麼擋：`content-visibility: hidden` 把元素與子元素排除在無障礙樹與頁內搜尋之外；`auto` 在某些輔助技術設定下，畫面外的節點也可能在焦點移進去之前都不在無障礙樹或循序導覽裡（引用："In certain assistive technology configurations, off-screen nodes utilizing `content-visibility: auto` may be excluded from the accessibility tree or sequential navigation routes until focus is forcibly moved inside them."）
- 戰報：部分改善——`hidden` 的情況改用 `hidden="until-found"` 就保住頁內搜尋；`auto` 的情況指南只要求鍵盤實測，沒有給出解法（官方宣稱）

經過：為了效能把收合內容換成 `content-visibility: hidden`，Ctrl+F 再也找不到裡面的字。畫面外的 `auto` 區塊也可能讓部分讀屏使用者照順序走不到。
%% line-end %%

### 細節（不索引）
- 對手組：隱藏或停用把人擋在外面
- 支援狀態：content-visibility：Newly available（同上）；hidden="until-found" 的支援狀態指南未列，見 search-hidden-content
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出
