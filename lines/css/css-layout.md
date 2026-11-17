---
guide: css-layout
category: css
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/css/css-layout.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# CSS 版面與響應式設計

%% line-start id="mwg:css-layout" %%
## 替換元素的縫隙用 display: block 消掉，不用 overflow: hidden 遮
- 做法：對 `<img>`、`<canvas>`、`<svg>`、`<video>`、`<iframe>` 改用區塊外部顯示值（`display: block`／`grid`／`flex`），從源頭移除縫隙
- 對手：這些替換元素預設是 `display: inline`，在某些版面會多出一條縫（引用："certain replaced elements like `<canvas>`, `<img>`, `<svg>`, `<video>`, `<iframe>` use `display: inline` by default, which can add a gap in certain layouts."）
- 退路：不需要——支援狀態為 Widely 或不適用，不必退路
- 解鎖：（缺）

經過：圖片底下莫名多幾 px，常見的「修法」是在父層加 `overflow: hidden` 把它切掉，但這只是把版面問題藏起來。指南的原則是不用 `overflow: hidden` 掩飾版面問題，要從源頭修。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：—（display 指南未給支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:css-layout:2" %%
## 用 aspect-ratio 先替媒體留位置
- 做法：媒體元素設 `aspect-ratio`（例如 `16 / 9`），搭配 `inline-size: 100%; block-size: auto`
- 對手：圖片、影片載入前沒有預留空間，載入後把下方內容往下推，造成版面位移（引用："Use `aspect-ratio` to reserve space for media and prevent layout shift before assets load."）
- 退路：不需要——支援狀態為 Widely 或不適用，不必退路
- 解鎖：（缺）

經過：讀到一半文字突然往下跳，是因為上方圖片剛載入完成。先宣告比例，瀏覽器在圖片抵達前就知道要留多高。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：—（aspect-ratio 指南未給支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:css-layout:3" %%
## 可能放不下的 flex 列要開 flex-wrap: wrap
- 做法：只要有溢出的可能，flex 容器就設 `flex-wrap: wrap`；含長網址、程式碼的項目另設 `min-inline-size: 0`
- 對手：`nowrap` 又沒有 `overflow: auto/hidden`，窄視窗下項目會溢出容器（引用："`nowrap` without `overflow: auto/hidden` will spill on narrow viewports."）
- 退路：不需要——支援狀態為 Widely 或不適用，不必退路
- 解鎖：（缺）

經過：桌面寬度下看起來好好的一列按鈕，到手機上就衝出畫面。指南另外建議在 `wrap` 後面疊一行 `flex-wrap: balance` 讓各列平均、避免最後一列只剩一個孤兒項目，但那是 Limited 的新功能，不在這條線的範圍。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：—（flex-wrap: wrap 指南未給支援資料；同節的 flex-wrap: balance 為 Limited，Chrome 150、Edge 150）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:css-layout:4" %%
## 用 flex-wrap: balance 避免最後一列只剩一個孤兒項目
- 做法：標籤雲、篩選 pills、按鈕群等緊湊項目先設 `flex-wrap: wrap`，再疊 `flex-wrap: balance`
- 對手：一般換行只決定何時折列，最後一列可能只剩一個項目，視覺重量不均（引用："distribute items evenly across lines and prevent a single orphaned item on the final row"）
- 退路：失去主要好處——退回一般 `wrap`，保留換行但最後一列仍可能只有一項
- 解鎖：`flex-wrap: balance` 可平均分配各列項目，避免最後一列落單

經過：九個標籤變成五、三、一三列，最後那個像被丟下。支援的瀏覽器會重新分配各列數量，不支援時保留一般換行。
%% line-end %%

### 細節（不索引）
- 對手組：版面擠壓破壞可讀性
- 支援狀態：flex-wrap: balance：Limited（Chrome 150、Edge 150；Firefox、Safari 不支援）
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：標籤牆、導覽列、篩選晶片不必依寬度手調每列數量，就能讓最後一列不孤單。目前僅 Chromium，其他瀏覽器退回一般 wrap
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:css-layout:5" %%
## 置中對齊加 safe，窄容器不裁掉焦點內容
- 做法：位置對齊寫成 `align-items: safe center` 等 safe alignment
- 對手：容器比內容窄時，普通置中會把可聚焦內容切掉（引用："Prefix positional alignment with `safe` (e.g., `align-items: safe center`) so focusable content isn't clipped when the container is narrower than its content."）
- 退路：不需要——支援狀態為 Widely 或不適用，不必退路
- 解鎖：（缺）

經過：置中的長按鈕在窄視窗突出兩側，其中一側可能完全無法捲到。safe 讓對齊在放不下時改往安全方向。
%% line-end %%

### 細節（不索引）
- 對手組：裁切切掉不該切的
- 支援狀態：不適用（本指南未附 safe alignment 支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:css-layout:6" %%
## 不用 order、*-reverse、dense 改變互動內容的視覺順序
- 做法：互動項目在 DOM 就排成實際閱讀順序，不用 `order`、`flex-direction: *-reverse` 或 `grid-auto-flow: dense` 重排
- 對手：這些功能只改視覺順序，DOM 仍驅動 Tab，鍵盤焦點與畫面位置對不上（引用："They change visual order only; the DOM order still drives sequential focus, so keyboard tab flow won't match what the user sees."）
- 退路：不需要——支援狀態為 Widely 或不適用，不必退路
- 解鎖：（缺）

經過：grid 的 dense 會為了填空把項目前移；flex 的 reverse 也一樣。非互動的純視覺排列與鍵盤操作要分開判斷。
%% line-end %%

### 細節（不索引）
- 對手組：視覺順序與DOM順序脫鉤
- 支援狀態：不適用（本指南未附這些屬性的支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:css-layout:7" %%
## 用 subgrid 對齊不同卡片裡的標題、 metadata 與 CTA
- 做法：卡片以 `grid-row: span 2` 跨軌，內層 `grid-template-rows: subgrid` 繼承外層軌道，前面保留一般 rows 宣告作退路
- 對手：卡片內容長短不一時，各卡的標題、metadata 與行動鈕形成參差不齊的邊緣（引用："Subgrid lets a nested grid inherit its parent's tracks so grandchildren align across siblings."）
- 退路：不需要——subgrid 已 Widely，不必退路
- 解鎖：卡片內層可繼承外層 grid 軌道，讓標題與 CTA 跨卡片對齊

經過：一張卡片標題特別長，不該把其他卡的 CTA 也跟著推高或錯開。外層決定共同節拍，內容仍留在各卡片裡。
%% line-end %%

### 細節（不索引）
- 對手組：版面依賴錯的量測
- 支援狀態：Subgrid：Widely（2023-09-15）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:css-layout:8" %%
## 子項目數量不固定時 subgrid 只沿一個軸
- 做法：子項目數量會變時只在一軸用 subgrid，另一軸用 `grid-auto-rows`／`grid-auto-columns`
- 對手：兩軸都 subgrid 時，多出的項目會全部落在最後一條軌道（引用："Don't apply subgrid to both axes when the child count is variable. Extras land in the last track"）
- 退路：不需要——支援狀態為 Widely 或不適用，不必退路
- 解鎖：（缺）

經過：卡片有固定欄位時可兩軸共用；會多出一串 tags 或 actions 時，另一軸必須讓瀏覽器自行增加軌道。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：Subgrid：Widely（2023-09-15）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:css-layout:9" %%
## container-type: size 要同時給容器明確高度
- 做法：需要查詢兩軸時用 `container-type: size` 並給容器明確 `block-size`；只查寬度用 `inline-size`
- 對手：size containment 會忽略子元素的內在尺寸，沒給高度時容器與後代會塌陷（引用："without one, descendants collapse because size containment forces the container to ignore its content."）
- 退路：不需要——支援狀態為 Widely 或不適用，不必退路
- 解鎖：（缺）

經過：以為容器會像平時一樣由內容撐高，宣告 size 後卻變成 0。只關心寬度時不要多鎖高度軸。
%% line-end %%

### 細節（不索引）
- 對手組：版面依賴錯的量測
- 支援狀態：Container queries (size)：Widely（2023-02-14）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:css-layout:10" %%
## 用 scrollbar-gutter: stable 先留捲軸位置
- 做法：可能長出捲軸的容器設 `scrollbar-gutter: stable`，捲動需求用 `overflow: auto`
- 對手：內容變多才出現捲軸時，可用寬度突然改變，整個版面跟著位移（引用："Use `scrollbar-gutter: stable` to reserve space for scrollbars and prevent layout shifts when content grows."）
- 退路：沒說——指南未交代不支援 `scrollbar-gutter` 時怎麼辦
- 解鎖：可預留捲軸空間，內容長出捲軸時版面寬度不再改變

經過：清單從十筆變十一筆，捲軸占掉十幾像素，所有卡片突然換行。先留 gutter 就不會跳。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：scrollbar-gutter：Newly（2024-12-11）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：即時更新的清單、聊天紀錄、篩選結果可以在捲軸出現時保持卡片與欄寬不動，不必先寫死捲軸永遠顯示。目前為 Newly
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:css-layout:11" %%
## 只要裁切用 overflow: clip，不要 hidden 或永遠顯示捲軸
- 做法：單純裁切用 `overflow: clip`；需要時才用 `auto` 出捲軸，不用 `hidden` 或無條件 `scroll`
- 對手：`hidden` 仍建立可被程式捲動的容器；`scroll` 則在沒有溢出時也強制出現捲軸（引用："`hidden` establishes a scroll container that can be programmatically scrolled."）
- 退路：不需要——支援狀態為 Widely 或不適用，不必退路
- 解鎖：（缺）

經過：以為 hidden 等於完全不可捲，腳本卻還能改變它的捲動位置。clip 才不建立 scroll container。
%% line-end %%

### 細節（不索引）
- 對手組：裁切切掉不該切的
- 支援狀態：不適用（本指南未附 overflow 各值的支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:css-layout:12" %%
## 全寬版面不用 100vw，避免捲軸寬造成水平溢出
- 做法：全寬用 `100%`；需要視窗單位時依情境用 `100dvw`／`100svw`
- 對手：`100vw` 不扣捲軸寬，桌面出現捲軸時內容就比可見區域寬（引用："it ignores scrollbar width and causes horizontal overflow."）
- 退路：不需要——支援狀態為 Widely 或不適用，不必退路
- 解鎖：（缺）

經過：桌面瀏覽器的傳統捲軸一直占位，100vw 卻把它也算進內容寬，於是頁面左右多出一小段。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：Small, large, and dynamic viewport units：Widely（2022-12-05）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:css-layout:13" %%
## repeat(auto-fit／auto-fill) 前容器要有明確寬度
- 做法：自動重複軌道的容器設明確 `inline-size`，避免在 `inline-grid` 或未設寬 flex item 上直接用
- 對手：容器沒有寬度可分配時，軌道數量會變得不可預測（引用："inside `display: inline-grid` or an unsized flex item, the container has no width to divide, making track counts unpredictable."）
- 退路：不需要——支援狀態為 Widely 或不適用，不必退路
- 解鎖：（缺）

經過：repeat 的次數不是看卡片內容，而是看容器寬與 repeat 尺寸參數；容器本身沒寬就無從計算。
%% line-end %%

### 細節（不索引）
- 對手組：版面依賴錯的量測
- 支援狀態：不適用（本指南未附 repeat() 的支援資料）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2

%% line-start id="mwg:css-layout:14" %%
## Grid lanes 尚未可用，先用多欄或接受 dense 的重排代價
- 做法：文件片段用 multi-column；卡片用 `grid-auto-flow: dense` 並接受視覺／DOM 順序差異；masonry 只在 `@supports` 中當增強
- 對手：不同高度項目要緊密排列時，一般 grid 留空洞；grid lanes 卻尚無主要瀏覽器原生支援（引用："Grid lanes is not natively supported by any major browser yet."）
- 退路：保住主要行為——先用 multi-column 或 `grid-auto-flow: dense` 緊密排列，只在 `@supports` 內加上 masonry
- 解鎖：（缺）

經過：規格名稱是 `display: grid-lanes`，早期實驗用 `grid-template-rows: masonry`。現在做相簿或瀑布流，不能把實驗語法當唯一出路。
%% line-end %%

### 細節（不索引）
- 對手組：版面依賴錯的量測
- 支援狀態：Grid lanes：無瀏覽器支援
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：新能力
- 發想（非指南原文）：原生 masonry 若普及，相簿、卡片牆、新聞首頁可兼顧緊密排列與 grid 軌道模型；目前只能以多欄或 dense 退回
- 變更紀錄：2026-11-17（v1.0.0）補拆舊三條上限遺漏；2026-11-18 改為槽 v2；2026-11-18 交叉核對仲裁：退路改為「保住主要行為」
