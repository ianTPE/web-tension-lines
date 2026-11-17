---
guide: webmcp
category: webmcp
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/webmcp/webmcp.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# WebMCP

%% line-start id="mwg:webmcp" %%
## 用瀏覽器分頁當工具註冊表，不架後端 MCP transport
- 做法：在分頁內用命令式 `document.modelContext.registerTool()` 或宣告式表單屬性，把 client-side 功能暴露成結構化工具
- 對手：（缺）指南只說 WebMCP 全在瀏覽器分頁執行，沒說後端做法在哪個時刻出問題（引用："WebMCP runs entirely **client-side** in the browser tab. It is *not* a backend server, and it does *not* use HTTP, Server-Sent Events (SSE), or `stdio` transports."）
- 退路：沒說——指南只寫這是 Chromium 旗標預覽，沒有交代不支援時該怎麼辦
- 解鎖：以前要讓助理操作網站功能，得自己架 MCP server 或做頁內腳本橋接；現在網頁本身就是工具註冊表，頁面內就能把功能暴露成結構化工具

經過：網頁自己就是 tool registry，目前只支援 Tools，不支援後端 MCP 的 Resources 或 Prompts。不要把 Node.js 背景程序、HTTP/SSE/stdio 架構搬進來。
%% line-end %%

### 細節（不索引）
- 對手組：頁面功能對代理不透明
- 支援狀態：WebMCP：無瀏覽器支援（Chromium 146 旗標 Early Preview）
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 缺／解鎖 有
- 類型：新能力
- 發想（非指南原文）：網站不必另架 MCP server，就能讓瀏覽器內助理操作搜尋、篩選、購物車等 client-side 功能。目前僅 Chromium 旗標預覽，且沒有 Resources／Prompts
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:webmcp:2" %%
## schema 收原始輸入並寫清參數用途，降低代理猜錯
- 做法：參數直接收使用者原始輸入，不讓代理先做數學換算；每個參數給明確型別與用途，選項意義寫在自己的 description
- 對手：schema 結構或參數描述不清會增加代理幻覺，讓它猜出不符合工具預期的輸入（引用："Always provide clear descriptions for every parameter to minimize agent hallucinations."）
- 退路：沒說——指南只寫工具 schema 的寫法，沒有交代不支援 WebMCP 時怎麼辦
- 解鎖：（缺）

經過：工具描述只說做什麼、何時用，參數名、型別、enum、default、限制都放 schema，不在散文重複。工具保持 atomic、composable，不把流程控制硬寫給代理。
%% line-end %%

### 細節（不索引）
- 對手組：表單假設錯的資料格式
- 支援狀態：WebMCP：無瀏覽器支援
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:webmcp:3" %%
## 回傳可重試錯誤，並等 UI 更新完才回應代理
- 做法：在程式碼驗證限制、回傳描述性錯誤與 rate-limit 處理；`execute` 等畫面狀態更新完成後才回傳結果
- 對手：太早回傳會讓工具結果和畫面狀態不一致，代理拿到成功時使用者還看不到對應更新（引用："Ensure the function returns *after* UI state updates for consistency."）
- 退路：沒說——指南只寫工具回傳的時機，沒有交代不支援 WebMCP 時怎麼辦
- 解鎖：（缺）

經過：代理收到「已加入購物車」時，畫面上的數量也必須已經改好。秘密不能放 client-side，資料庫仍要透過安全 API 層，重計算交給 Worker／WASM／WebGPU。
%% line-end %%

### 細節（不索引）
- 對手組：生命週期假設錯
- 支援狀態：WebMCP：無瀏覽器支援
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:webmcp:4" %%
## 高風險工具保留代理控制之外的人工確認
- 做法：刪除或不可逆動作不自動送出，UI 必須在代理控制之外要求使用者手動確認
- 對手：沒有外部防護時，代理可能直接執行破壞性或不可逆操作（引用："Avoid auto-submitting tools for destructive or irreversible actions (e.g., deleting data) unless the UI requires manual user confirmation outside the agent's control."）
- 退路：沒說——指南只寫高風險動作的防護，沒有交代不支援 WebMCP 時怎麼辦
- 解鎖：（缺）

經過：工具描述得再清楚，都不能取代不可逆動作的確認門。這裡的防線在產品 UI，不是代理的一句指令。
%% line-end %%

### 細節（不索引）
- 對手組：動作被意外觸發
- 支援狀態：WebMCP：無瀏覽器支援
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:webmcp:5" %%
## 資料變得比代理反應快時不要暴露即時工具
- 做法：高頻變動資料避免直接依賴代理操作，改用一般即時 UI 或明確刷新後再呼叫
- 對手：資料更新速度超過代理反應時，代理會拿過期脈絡判斷與執行（引用："If data changes faster than the agent can react, it may work with stale context."）
- 退路：沒說——指南只寫不該暴露即時工具的理由，沒有交代不支援 WebMCP 時怎麼辦
- 解鎖：（缺）

經過：報價、即時庫存每秒都在變，代理理解上一刻的畫面後再下指令，目標早已不同。動態註冊與 `AbortSignal` 也只能管工具生命週期，不能讓資料停止變動。
%% line-end %%

### 細節（不索引）
- 對手組：生命週期假設錯
- 支援狀態：WebMCP：無瀏覽器支援
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
