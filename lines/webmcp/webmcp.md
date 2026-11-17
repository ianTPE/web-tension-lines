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
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在分頁內用命令式 `document.modelContext.registerTool()` 或宣告式表單屬性，把 client-side 功能暴露成結構化工具
- 被什麼擋：（缺）指南只說 WebMCP 全在瀏覽器分頁執行，沒說後端做法在哪個時刻出問題（引用："WebMCP runs entirely **client-side** in the browser tab. It is *not* a backend server, and it does *not* use HTTP, Server-Sent Events (SSE), or `stdio` transports."）
- 戰報：僵持——Chromium 146.0.7672.0 起仍需開 `#enable-webmcp-testing`；其他瀏覽器沒有原生支援（官方宣稱）

經過：網頁自己就是 tool registry，目前只支援 Tools，不支援後端 MCP 的 Resources 或 Prompts。不要把 Node.js 背景程序、HTTP/SSE/stdio 架構搬進來。
%% line-end %%

### 細節（不索引）
- 對手組：頁面功能對代理不透明
- 支援狀態：WebMCP：無瀏覽器支援（Chromium 146 旗標 Early Preview）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：網站不必另架 MCP server，就能讓瀏覽器內助理操作搜尋、篩選、購物車等 client-side 功能。目前僅 Chromium 旗標預覽，且沒有 Resources／Prompts
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:webmcp:2" %%
## schema 收原始輸入並寫清參數用途，降低代理猜錯
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：參數直接收使用者原始輸入，不讓代理先做數學換算；每個參數給明確型別與用途，選項意義寫在自己的 description
- 被什麼擋：schema 結構或參數描述不清會增加代理幻覺，讓它猜出不符合工具預期的輸入（引用："Always provide clear descriptions for every parameter to minimize agent hallucinations."）
- 戰報：僵持——代理能照 schema 組出較可預期的輸入；WebMCP 仍只有 Chromium 旗標預覽（官方宣稱）

經過：工具描述只說做什麼、何時用，參數名、型別、enum、default、限制都放 schema，不在散文重複。工具保持 atomic、composable，不把流程控制硬寫給代理。
%% line-end %%

### 細節（不索引）
- 對手組：表單假設錯的資料格式
- 支援狀態：WebMCP：無瀏覽器支援
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:webmcp:3" %%
## 回傳可重試錯誤，並等 UI 更新完才回應代理
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在程式碼驗證限制、回傳描述性錯誤與 rate-limit 處理；`execute` 等畫面狀態更新完成後才回傳結果
- 被什麼擋：太早回傳會讓工具結果和畫面狀態不一致，代理拿到成功時使用者還看不到對應更新（引用："Ensure the function returns *after* UI state updates for consistency."）
- 戰報：僵持——代理與使用者看到同一個完成狀態，失敗時也有資訊可重試；WebMCP 仍只有 Chromium 旗標預覽（官方宣稱）

經過：代理收到「已加入購物車」時，畫面上的數量也必須已經改好。秘密不能放 client-side，資料庫仍要透過安全 API 層，重計算交給 Worker／WASM／WebGPU。
%% line-end %%

### 細節（不索引）
- 對手組：生命週期假設錯
- 支援狀態：WebMCP：無瀏覽器支援
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:webmcp:4" %%
## 高風險工具保留代理控制之外的人工確認
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：刪除或不可逆動作不自動送出，UI 必須在代理控制之外要求使用者手動確認
- 被什麼擋：沒有外部防護時，代理可能直接執行破壞性或不可逆操作（引用："Avoid auto-submitting tools for destructive or irreversible actions (e.g., deleting data) unless the UI requires manual user confirmation outside the agent's control."）
- 戰報：僵持——最後確認仍由人決定；WebMCP 本身沒有提供普遍可用的安全保證（官方宣稱）

經過：工具描述得再清楚，都不能取代不可逆動作的確認門。這裡的防線在產品 UI，不是代理的一句指令。
%% line-end %%

### 細節（不索引）
- 對手組：動作被意外觸發
- 支援狀態：WebMCP：無瀏覽器支援
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:webmcp:5" %%
## 資料變得比代理反應快時不要暴露即時工具
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：高頻變動資料避免直接依賴代理操作，改用一般即時 UI 或明確刷新後再呼叫
- 被什麼擋：資料更新速度超過代理反應時，代理會拿過期脈絡判斷與執行（引用："If data changes faster than the agent can react, it may work with stale context."）
- 戰報：僵持——指南只建議在這種情況避免 WebMCP，沒有提供同步機制（官方宣稱）

經過：報價、即時庫存每秒都在變，代理理解上一刻的畫面後再下指令，目標早已不同。動態註冊與 `AbortSignal` 也只能管工具生命週期，不能讓資料停止變動。
%% line-end %%

### 細節（不索引）
- 對手組：生命週期假設錯
- 支援狀態：WebMCP：無瀏覽器支援
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
