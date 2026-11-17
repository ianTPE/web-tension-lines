---
guide: performance
category: performance
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/performance/performance.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 效能

%% line-start id="mwg:performance" %%
## 用 `async`/`defer`、內嵌關鍵 CSS 擋掉卡住渲染的 `@import` 與 head 裡的大腳本
- 做法：首屏需要的 CSS 內嵌進 `<head>`、其餘延後；非關鍵腳本一律 `async` 或 `defer`（`type="module"` 預設延後）；用 `<link media>` 切分樣式表；第三方腳本加 `defer` 放到頁尾
- 對手：CSS 裡的 `@import` 造成循序請求鏈、延後 CSSOM；head 裡的大型非關鍵腳本讓 DOM 建構停下來等它下載、解析、執行（引用："This halts DOM construction until the script is downloaded, parsed, and executed."）
- 退路：不需要——支援狀態不適用，不必另設退路
- 解鎖：（缺）

經過：head 裡一支大腳本、樣式表裡一行 `@import`，就讓整頁停在白畫面等。關鍵的內嵌、其他的延後，第一次繪製就不必等不重要的東西。
%% line-end %%

### 細節（不索引）
- 對手組：載入優先序錯置
- 支援狀態：指南未附瀏覽器支援資料，記不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:performance:2" %%
## LCP 圖片寫在原始 HTML 裡、不延遲載入，別讓 JS 或 CSS 當唯一來源
- 做法：LCP 圖片用 `<img>`（或 `<link rel="preload" as="image">`）直接出現在原始 HTML，加 `fetchpriority="high"`；首屏圖片不加 `loading="lazy"`；不要用 JS 載入器渲染 hero 區塊
- 對手：對 LCP 圖片加 `loading="lazy"` 會刻意延後到排版完成才抓；用 JS 渲染 hero 形成 HTML→JS→執行→圖片請求的長鏈（引用："This purposefully delays the fetch until layout calculation is complete, severely degrading LCP."）
- 退路：不需要——支援狀態不適用，不必另設退路
- 解鎖：（缺）

經過：最大的那張圖藏在 JS 或被標成 lazy，瀏覽器得等排版或等腳本跑完才知道要抓它。直接寫在 HTML 裡，掃描器第一時間就找得到。
%% line-end %%

### 細節（不索引）
- 對手組：載入優先序錯置
- 支援狀態：指南未附瀏覽器支援資料，記不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:performance:3" %%
## 優先序是零和的：high 和預載給太多就互相抵銷
- 做法：`fetchpriority="high"` 只給 LCP 圖片；字型預設已是高優先，不加 high；不要預載所有字型
- 對手：提升太多資源造成網路互搶、讓提升失效；預載所有字型餓死其他關鍵資源（引用："Prioritization is a zero-sum mechanism. Elevating too many resources creates network contention and negates the benefit."）
- 退路：不需要——支援狀態不適用，不必另設退路
- 解鎖：（缺）

經過：每個都想排第一，結果大家一起擠。高優先序是稀缺品，只能給一兩個。
%% line-end %%

### 細節（不索引）
- 對手組：載入優先序錯置
- 支援狀態：指南未附瀏覽器支援資料，記不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:performance:4" %%
## 用 `scheduler.yield()` 讓出主執行緒，續行排在佇列前面而不是最後
- 做法：超過 50ms 的 JS 切塊，用 `scheduler.yield()` 讓出主執行緒（不支援時退回包在 Promise 裡的 `setTimeout`）；超過 250ms 的工作移到 Web Worker
- 對手：只靠 `setTimeout(..., 0)` 讓出，續行會被排到任務佇列最後，前面有其他任務時要等很久（引用："Standard `setTimeout` places continuations at the *back* of the task queue, potentially causing long delays if other tasks are pending."）
- 退路：不需要——支援狀態不適用（不支援時另有 `setTimeout` 退路）
- 解鎖：用 `scheduler.yield()` 讓出主執行緒並把續行排在佇列前面，避免被後續任務拖慢

經過：切塊讓出是為了讓使用者輸入插隊，但 `setTimeout` 讓出之後，自己的下半段也得排到別人後面。`scheduler.yield()` 讓出又不丟掉位置。
%% line-end %%

### 細節（不索引）
- 對手組：主執行緒被重活卡住
- 支援狀態：指南未附瀏覽器支援資料，記不適用（同一功能的支援資料見 mwg:break-up-long-tasks）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：同 mwg:break-up-long-tasks：瀏覽器裡跑大量運算（解析大檔、建索引）時介面仍能捲動、能按取消，而且長工作不會因為讓出而被別的任務拖到很久之後才做完
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:performance:5" %%
## 用 `contain` 與 `content-visibility: auto` 把排版重算圈在元件裡
- 做法：對獨立的 UI 元件（彈窗、小工具）用 `contain: layout style paint`；大型複雜頁面的畫面外區塊用 `content-visibility: auto` 並配 `contain-intrinsic-size`（用 `auto` 與依內容推算的值）
- 對手：元件內部變動觸發整頁重排（引用："use `contain: layout style paint` to prevent internal changes from triggering page-wide reflows."）
- 退路：不需要——支援狀態不適用，不必另設退路
- 解鎖：（缺）

經過：小工具裡改一個數字，整頁都跟著重排。宣告圍堵之後，重算範圍就停在元件邊界。
%% line-end %%

### 細節（不索引）
- 對手組：主執行緒被重活卡住
- 支援狀態：指南未附瀏覽器支援資料，記不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:performance:6" %%
## `will-change` 只在需要時加，不要全域撒
- 做法：`will-change: transform` 只在真的要動畫時（例如 `:hover`）加在單一元素上；小而簡單的頁面也不要套 `content-visibility: auto`
- 對手：對大量元素無差別加 `will-change`，耗掉過多顯示記憶體，造成 GPU 當掉或渲染變慢（引用："Indiscriminately applying `will-change: transform` to multiple elements consumes excessive VRAM, causing GPU crashes or sluggish rendering."）
- 退路：不需要——支援狀態不適用，不必另設退路
- 解鎖：（缺）

經過：`will-change` 是給瀏覽器的提示，撒滿整頁就變成要求瀏覽器替每個元素都開圖層。效能手段用過頭，反而拖垮效能。
%% line-end %%

### 細節（不索引）
- 對手組：優化用過頭反傷
- 支援狀態：指南未附瀏覽器支援資料，記不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:performance:7" %%
## 圖片與影片寫上 `width`／`height`，載入前就預留空間
- 做法：`<img>`、`<video>` 寫明確的 `width` 與 `height`（HTML 屬性或 CSS 皆可），讓瀏覽器立刻算出長寬比
- 對手：延遲載入的圖片沒有尺寸，載入時造成版面位移（引用："Failing to specify width/height on lazy loaded images causes layout shifts."）
- 退路：不需要——支援狀態不適用，不必另設退路
- 解鎖：（缺）

經過：圖片還沒到時高度是 0，到了才撐開，把下面的文字推走。先寫上尺寸，位子一開始就留好。
%% line-end %%

### 細節（不索引）
- 對手組：版面意外溢出或位移
- 支援狀態：指南未附瀏覽器支援資料，記不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:performance:8" %%
## 用了 `srcset` 就要寫 `sizes`，否則手機抓桌機大圖
- 做法：響應式圖片用 `srcset` 加 `sizes`；用 `<picture>` 依序提供 AVIF／WebP／JPEG
- 對手：有 `srcset` 沒有 `sizes`，瀏覽器假設圖片占滿視窗寬，下載最大的那張（引用："Without `sizes`, the browser assumes `100vw` and downloads the largest available image."）
- 退路：不需要——支援狀態不適用，不必另設退路
- 解鎖：（缺）

經過：準備了好幾種尺寸，卻因為少寫一個屬性，瀏覽器還是挑最大的。補上 `sizes`，手機才真的拿到小圖。
%% line-end %%

### 細節（不索引）
- 對手組：載入超過需要的資源
- 支援狀態：指南未附瀏覽器支援資料，記不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:performance:9" %%
## 用動態 `import()` 切分程式，不要整包 `app.js`
- 做法：路由與重型 UI 函式庫用動態 `import()` 切開；打包設定把第三方套件與應用邏輯分塊
- 對手：單一巨大的 `app.js` 拉長初始畫面的解析時間與記憶體用量（引用："DON'T ship a single, enormous `app.js` bundle: It increases parse time and memory consumption for initial views."）
- 退路：不需要——支援狀態不適用，不必另設退路
- 解鎖：（缺）

經過：整個 app 的程式碼都塞進一包，低階裝置光解析就卡住。按需載入之後，第一個畫面只付第一個畫面的成本。
%% line-end %%

### 細節（不索引）
- 對手組：載入超過需要的資源
- 支援狀態：指南未附瀏覽器支援資料，記不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:performance:10" %%
## Service Worker 快取要分策略、要版本化、要設上限
- 做法：帶雜湊的靜態資源用 CacheFirst、可略舊的 API 用 StaleWhileRevalidate、HTML 用 NetworkFirst；設定過期與容量上限；不透明回應不要用 CacheFirst 大量快取；資源更新時一定換雜湊／版本
- 對手：不更新資源雜湊或版本，使用者被困在無止盡的快取循環；盲目快取不透明回應大量耗用配額且靜默失敗（引用："Failing to update asset hashes/versions will trap users in infinite cache loops."）
- 退路：不需要——支援狀態不適用，不必另設退路
- 解鎖：（缺）

經過：Service Worker 讓頁面不用網路就能開，但快取寫錯，使用者就永遠看不到新版本。依資源類型選策略、加上版本與上限，快取才是幫手。
%% line-end %%

### 細節（不索引）
- 對手組：快取策略錯置
- 支援狀態：指南未附瀏覽器支援資料，記不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:performance:11" %%
## 非敏感頁面別用 `Cache-Control: no-store`，否則失去 bfcache
- 做法：`no-store` 只留給真正私密的資料；只是需要最新內容的頁面改用 `no-cache` 或 `max-age=0`
- 對手：`no-store` 讓瀏覽器不能把頁面放進上一頁／下一頁快取，感知速度明顯變慢（引用："This directive prevents the browser from storing the page in the **Back-Forward Cache (bfcache)**, leading to significantly slower perceived performance."）
- 退路：不需要——支援狀態不適用，不必另設退路
- 解鎖：（缺）

經過：為了「永遠拿最新」而寫 `no-store`，代價是每次按上一頁都得重新載入。改用 `no-cache`，內容一樣新、返回一樣快。
%% line-end %%

### 細節（不索引）
- 對手組：快取策略錯置
- 支援狀態：指南未附瀏覽器支援資料，記不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 4 個糾錯提醒未拆（版面抖動 layout thrashing、高頻事件要 debounce／throttle、不要盲目自動播放大影片、tree-shaking 與壓縮）
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
