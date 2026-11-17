---
guide: cpp-on-the-web
category: wasm
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/wasm/cpp-on-the-web.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 用 Emscripten 把 C／C++ 編譯成 WebAssembly

%% line-start id="mwg:cpp-on-the-web" %%
## 用 `-sENVIRONMENT=web`、靜態連結與乾淨的發行設定，只出貨瀏覽器需要的程式碼
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：連結時加 `-sSTRICT`、`-sEXPORT_ES6`（輸出 ES 模組、不汙染全域）與 `-sENVIRONMENT=web`（或 `worker`、`web,worker`）；發行版用 `-O3`／`-Os`／`-Oz` 加 `-flto`，不帶 `-g` 與 `-sASSERTIONS`，必要時 `--closure=1`；用靜態函式庫（`.a`），非得載入外掛才用 `-sMAIN_MODULE`／`-sSIDE_MODULE`
- 被什麼擋：預設輸出帶著 Node.js 與 shell 的執行環境程式碼；動態連結再加上程式碼大小與執行時的額外負擔（引用："Strip Node.js and shell runtime support code to minimize bundle size. … add code-size and runtime overhead"）
- 戰報：勝——去掉用不到的執行環境與除錯資訊，套件縮到最小（官方宣稱）

經過：把一個影像處理函式庫移植到網頁，產出的 JS 黏合碼裡有一大段只在 Node 用得到的檔案系統支援。指定只跑在瀏覽器、改成靜態連結後，下載量明顯變小。
%% line-end %%

### 細節（不索引）
- 對手組：載入超過需要的資源
- 支援狀態：工具鏈指南，沒有瀏覽器支援資料；不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:cpp-on-the-web:2" %%
## Wasm 入口一次處理整塊緩衝區，不逐像素跨越 JS 邊界
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：把 C／C++ 入口設計成接收指標與長度、一次處理整張影像或整段音訊，JS 端 `_malloc` 一塊線性記憶體、呼叫一次、再從 `HEAPU8` 讀出並 `_free`
- 被什麼擋：每個像素、音訊取樣或頂點都呼叫一次匯出函式，跨邊界的開銷把 Wasm 的效能優勢吃光（引用："Calling an exported Wasm function per pixel, per audio sample, or per vertex incurs boundary overhead that negates Wasm performance gains."）
- 戰報：勝——一次呼叫處理整塊連續記憶體，邊界開銷只付一次（官方宣稱）

經過：濾鏡改寫成 C++ 後反而比純 JS 慢，原因是 JS 迴圈每個像素都呼叫一次 Wasm。改成一次把整張圖交進去，Wasm 才真正快起來。
%% line-end %%

### 細節（不索引）
- 對手組：邊界往返吃掉效能
- 支援狀態：工具鏈指南，沒有瀏覽器支援資料；不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:cpp-on-the-web:3" %%
## 開了記憶體成長時，每次 Wasm 呼叫後重新讀取 `HEAPU8`
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：使用 `-sALLOW_MEMORY_GROWTH` 時，不快取 `HEAPU8` 或它的 `buffer`；在可能配置記憶體的 Wasm 呼叫回來後，重新從 `wasm.HEAPU8` 建立視圖並 `.slice()` 複製出來
- 被什麼擋：記憶體成長時舊的 `ArrayBuffer` 會被分離，先前拿到的視圖失效（引用："`-sALLOW_MEMORY_GROWTH` detaches the previous `ArrayBuffer` when resizing."）
- 戰報：勝——讀到的永遠是成長後的那塊記憶體（官方宣稱）

經過：小圖處理正常，換一張大圖讓堆積長大後，JS 端拿著呼叫前存下的視圖去讀，讀到的是已經分離的緩衝區。改成呼叫後才取 `HEAPU8` 就沒事。
%% line-end %%

### 細節（不索引）
- 對手組：生命週期假設錯
- 支援狀態：工具鏈指南，沒有瀏覽器支援資料；不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:cpp-on-the-web:4" %%
## 超過幾毫秒的 Wasm 計算移到 Worker、多執行緒，或拆成逐幀讓出
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在模組 Worker 裡實例化 ES6 Wasm 模組，算完用可轉移的 `ArrayBuffer` 經 `postMessage` 送回；或用 `-pthread` 多執行緒（需要 `SharedArrayBuffer`，頁面要設 COOP `same-origin` 與 COEP `require-corp` 達成跨來源隔離）；或用 `emscripten_set_main_loop` 每幀跑一次，需要等待非同步 JS API 時用 `-sJSPI`／`-sASYNCIFY`
- 被什麼擋：在主執行緒同步跑影像渲染、光線追蹤、物理模擬或大量解析，頁面渲染與輸入全部凍結（引用："Any WebAssembly call that takes more than a few milliseconds … **must not** run synchronously on the main thread, or it will freeze page rendering and input."）
- 戰報：勝——重計算離開主執行緒，介面維持回應；多執行緒的代價是頁面必須跨來源隔離（官方宣稱）

經過：瀏覽器裡的光線追蹤示範一按「渲染」，整頁卡住十幾秒，連取消鈕都按不到。移進 Worker 後畫面照常捲動，算好的影像才一次送回來。
%% line-end %%

### 細節（不索引）
- 對手組：主執行緒被重活卡住
- 支援狀態：工具鏈指南，沒有瀏覽器支援資料；不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:cpp-on-the-web:5" %%
## 深度遞迴改成迴圈或加大 `-sSTACK_SIZE`，開發時用 `-sASSERTIONS` 驗證
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：把遞迴的光線追蹤、樹走訪改寫成迭代迴圈，或連結時加大堆疊（如 `-sSTACK_SIZE=1MB`）；開發版開 `-sASSERTIONS` 抓無效記憶體存取、缺少的匯出與 ABI 不符，發行前拿掉；一律在真瀏覽器跑過、確認主控台沒有警告
- 被什麼擋：Emscripten 預設堆疊只有 64 KB，比原生作業系統的堆疊小得多，深度遞迴會溢位並破壞線性記憶體（引用："Deeply recursive algorithms (such as recursive ray tracers or tree traversals) can overflow the stack and corrupt linear memory"）
- 戰報：勝——遞迴深度不再超出堆疊，記憶體不被悄悄破壞（官方宣稱）

經過：在桌機上跑得好好的 C++ 場景樹走訪，編成 Wasm 後在複雜場景偶爾算出亂碼。原因是 64 KB 堆疊撐不住遞迴，溢位寫壞了旁邊的資料。
%% line-end %%

### 細節（不索引）
- 對手組：移植時沿用原生假設
- 支援狀態：工具鏈指南，沒有瀏覽器支援資料；不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 另有 3 個糾錯提醒未拆：命令列風格（省略預設旗標與 `=1`、用標準編譯旗標、逗號清單與回應檔、分開編譯再連結）；`-Werror -Wall` 及早抓錯；把 `emcc` 接進專案的 build 腳本，第三方函式庫用 `emcmake`／`emconfigure`／`emmake`
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
