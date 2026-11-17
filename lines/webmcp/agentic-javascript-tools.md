---
guide: agentic-javascript-tools
category: webmcp
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/webmcp/agentic-javascript-tools.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 給代理用的 JavaScript 工具

%% line-start id="mwg:agentic-javascript-tools" %%
## 用 registerTool() 依路由與使用者狀態註冊頁面工具
- 做法：用 `document.modelContext.registerTool()` 註冊名稱、描述、`inputSchema`、`execute()` 與 annotations；SPA 依目前路由和使用者狀態動態增刪工具
- 對手：（缺）指南只說命令式 API 適合需要動態增刪工具的 SPA，沒說固定宣告在哪個時刻出問題（引用："This is ideal for Single Page Applications (SPAs) where tools need to be added or removed based on the current route or user state."）
- 退路：失去主要好處——不支援時靠功能偵測跳過註冊，頁面照常但代理完全看不到這些工具
- 解鎖：以前要讓瀏覽器內助理操作頁面功能，得另架 MCP server 或做頁內橋接；現在頁面直接註冊工具，代理就能依目前路由與狀態操作

經過：頁面是工具生產者，瀏覽器、擴充功能、DevTools 與系統助理是主要消費者。只要註冊即可，頁面不必為了暴露工具再呼叫 `getTools()` 或 `executeTool()`。
%% line-end %%

### 細節（不索引）
- 對手組：頁面功能對代理不透明
- 支援狀態：document.modelContext：無瀏覽器支援（Early Preview 需 Chromium 旗標）
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 缺／解鎖 有
- 類型：新能力
- 發想（非指南原文）：SPA 可以把目前頁面真正能做的事交給瀏覽器代理，例如商品頁暴露查庫存、結帳頁暴露套用折扣，不必另做後端 MCP server。目前只有 Chromium 旗標預覽
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:agentic-javascript-tools:2" %%
## 跨框架工具要 exposedTo 與 fromOrigins 雙向授權
- 做法：提供者註冊時用 `exposedTo` 列出可發現、執行的來源；消費者用 `getTools({ fromOrigins: [...] })` 明確查詢提供者，所有來源限 HTTPS 或 localhost
- 對手：只有單邊授權時跨來源工具仍不可見；不是潛在可信來源會讓 `registerTool()` 以 `SecurityError` 拒絕（引用："Without `fromOrigins`, `getTools()` queries only same-origin documents."）
- 退路：沒說——指南只給整體的功能偵測退路，沒有針對跨來源授權說明
- 解鎖：（缺）

經過：結帳頁要呼叫購物車 iframe 的工具，iframe 開放還不夠，外層也要指明信任哪個來源。預設仍只限本文件與同來源框架。
%% line-end %%

### 細節（不索引）
- 對手組：合法連線被安全規則擋下
- 支援狀態：document.modelContext：無瀏覽器支援
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:agentic-javascript-tools:3" %%
## inputSchema 的驗證與 default 都在 execute 裡處理
- 做法：在 `execute` 開頭檢查輸入型別、enum 與必要欄位，並在參數解構或函式內套用預設值
- 對手：瀏覽器不會依 `inputSchema` 驗證引數，也不會套用 `default`，只寫 schema 會讓錯誤輸入直接進入工具（引用："The browser does not validate arguments against `inputSchema` or apply `default` values, so do both in `execute`."）
- 退路：沒說——指南只給整體的功能偵測退路，沒有針對輸入驗證說明
- 解鎖：（缺）

經過：schema 是給代理理解的契約，不是執行時的守門員。排序值不在 enum 時要回傳可修正的錯誤，而不是拿去做查詢。
%% line-end %%

### 細節（不索引）
- 對手組：表單假設錯的資料格式
- 支援狀態：document.modelContext：無瀏覽器支援
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:agentic-javascript-tools:4" %%
## 可修正的錯誤用結構化回傳值，不要 throw
- 做法：找不到項目、輸入錯誤、HTTP 失敗時回傳 `{ error, ...診斷資料 }`；只有執行被取消時重新拋出
- 對手：`execute` 拋錯或 Promise reject 時，代理只收到一般執行失敗，原始錯誤訊息不會轉交，無法自我修正或重試（引用："The error message is not forwarded to the agent."）
- 退路：沒說——指南只給整體的功能偵測退路，沒有針對錯誤回傳方式說明
- 解鎖：（缺）

經過：代理找不存在的餐點時，與其只得到「工具失敗」，不如回傳可用餐點清單。例外留給真正的取消與未處理程式錯誤。
%% line-end %%

### 細節（不索引）
- 對手組：播報時機或可靠度出錯
- 支援狀態：document.modelContext：無瀏覽器支援
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:agentic-javascript-tools:5" %%
## 註銷與執行各用 AbortSignal，避免孤兒請求寫回舊畫面
- 做法：註冊時傳 `signal` 供路由離開時 abort 註銷；每次 `execute(input, { signal })` 把執行訊號傳給 fetch／事件，計時器自行清除，並回復取消前的 UI 狀態
- 對手：abort 註冊訊號只會註銷工具，不會取消已在跑的工作；長任務不理會執行訊號時會繼續耗資源，並在代理離開後寫入過期資料（引用："Aborting the registration signal only unregisters the tool — it does not cancel executions that are already running."）
- 退路：沒說——指南只給整體的功能偵測退路，沒有針對執行取消說明
- 解鎖：（缺）

經過：使用者換頁後工具消失了，上一頁的搜尋卻回來把新畫面蓋掉，因為兩種生命週期被混為一談。註冊與每次執行要分別收尾。
%% line-end %%

### 細節（不索引）
- 對手組：生命週期假設錯
- 支援狀態：document.modelContext：無瀏覽器支援
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:agentic-javascript-tools:6" %%
## consequentialHint 之外仍保留應用程式自己的確認
- 做法：訂票、轉帳、寄訊息、刪資料的工具標 `consequentialHint: true`，同時保留應用程式原有的確認 UI
- 對手：這個標記只是提示，不會自行阻止執行；不認得標記的舊瀏覽器完全不會要求確認（引用："It does not block execution on its own, and browsers that predate the hint will not prompt at all."）
- 退路：保住主要行為——不認得這個標記的舊瀏覽器不會提示，但應用程式自己的確認 UI 照舊擋著
- 解鎖：（缺）

經過：把提示當成安全機制，會讓不可復原動作在舊環境直接執行。標記改善代理判斷，不取代產品原有的確認門。
%% line-end %%

### 細節（不索引）
- 對手組：防線形同虛設
- 支援狀態：consequentialHint：Chrome 154 起；WebMCP 整體無瀏覽器支援
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:agentic-javascript-tools:7" %%
## 除錯工具用 annotations.debugging 與使用者工具分開
- 做法：傾倒內部狀態、切 feature flag、填測試資料的工具設 `annotations.debugging: true`
- 對手：（缺）指南只說標記能讓代理區分開發者工具與使用者任務，沒說混在一起的具體後果（引用："This lets agents tell developer-only tools apart from tools meant to act for the user."）
- 退路：失去主要好處——不支援時工具根本註冊不了，代理分不出開發工具與使用者操作
- 解鎖：以前同一頁的開發工具與使用者操作混在一起，代理分不出；現在能用標記讓代理區分兩者

經過：同一個頁面既有「送出訂單」也有「重置測試資料」，metadata 至少讓消費者知道後者是開發用途。標記預設為 false。
%% line-end %%

### 細節（不索引）
- 對手組：確認到錯的身分
- 支援狀態：annotations.debugging：Chrome 156 起；WebMCP 整體無瀏覽器支援
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 缺／解鎖 有
- 類型：新能力
- 發想（非指南原文）：測試控制台可以讓頁內代理只列開發工具，一般助理則避開重置資料、切旗標這類操作。目前只有 Chromium 旗標預覽
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:agentic-javascript-tools:8" %%
## getTools()／executeTool() 給頁內代理與測試，不是暴露工具的必要步驟
- 做法：頁內助理、iframe 代理與自動化測試用 `getTools()` 探索、`executeTool()` 呼叫；監聽 `toolchange` 更新清單
- 對手：（缺）指南只區分瀏覽器代理的 out-of-band 消費與頁內消費，沒說誤用時出了什麼事（引用："The `getTools()` and `executeTool()` methods exist specifically for consumers running inside the JavaScript environment"）
- 退路：失去主要好處——不支援時這兩個方法不存在，頁內代理與自動化測試都無從探索或呼叫工具
- 解鎖：以前沒有不依賴外部模型的瀏覽器內測試途徑，也做不了嵌入式 copilot；現在頁內可用這兩個方法探索並呼叫工具

經過：一般網站註冊後已由瀏覽器代理發現；這兩個方法用在嵌入式聊天 widget 或 Playwright、Vitest 這類同頁消費者。
%% line-end %%

### 細節（不索引）
- 對手組：頁面功能對代理不透明
- 支援狀態：document.modelContext：無瀏覽器支援
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 缺／解鎖 有
- 類型：新能力
- 發想（非指南原文）：工具可以有不依賴外部模型的瀏覽器內測試，也能做成嵌入式 copilot 直接操作目前頁面。目前只有 Chromium 旗標預覽
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:agentic-javascript-tools:9" %%
## executeTool() 對舊 Chrome 保留 JSON 字串輸入退路
- 做法：Chrome 155 起直接傳 plain object；遇到 "Failed to parse input" 才改用 `JSON.stringify(inputObject)`，其他錯誤照樣拋出
- 對手：舊版不接受 plain object，若把所有錯誤都當成格式問題重試，會掩蓋真正的執行或取消錯誤（引用："Since Chrome 155, `executeTool()` accepts a plain JavaScript object directly for `inputObject`, matching the input format your tool's `execute` callback receives."）
- 退路：保住主要行為——舊版 Chrome 不接受 plain object 時改成傳 JSON 字串，工具照樣能被呼叫
- 解鎖：（缺）

經過：輸入是循環參照或含 BigInt 時仍會拒絕；函式與 undefined 則會在 JSON 序列化時被省略，不是拋錯。
%% line-end %%

### 細節（不索引）
- 對手組：生命週期假設錯
- 支援狀態：executeTool() plain object：Chrome 155 起；WebMCP 整體無瀏覽器支援
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:agentic-javascript-tools:10" %%
## React／Angular／Vue 用官方整合，不自己包工具生命週期
- 做法：React 用 `useWebMCP`、Angular 用 provider／declare 整合、Vue 用 `useWebMCP` composable；React／Vue 以 `enabled` 控制可用性，不把 hook 放在條件裡
- 對手：在元件裡直接呼叫 `registerTool()` 或自寫 wrapper，會重複處理功能偵測、AbortSignal 清理與元件／injector 生命週期（引用："Each integration already handles feature detection, `AbortSignal` cleanup, and scoping tools to the component or injector lifecycle."）
- 退路：沒說——指南只給整體的功能偵測退路，沒有針對框架整合說明
- 解鎖：（缺）

經過：工具定義的形狀不變，但註冊時機交給框架。整合可能把結果包成 `{ content, isError }`，錯誤格式不能直接假設與原生 API 相同。
%% line-end %%

### 細節（不索引）
- 對手組：生命週期假設錯
- 支援狀態：框架整合為實驗性；WebMCP 整體無瀏覽器支援
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
