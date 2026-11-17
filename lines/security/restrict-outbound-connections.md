---
guide: restrict-outbound-connections
category: security
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/security/restrict-outbound-connections.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 用 Connection Allowlist 限制對外連線

%% line-start id="mwg:restrict-outbound-connections" %%
## 用 `Connection-Allowlist` 一條清單管住所有對外連線，連 CSP 管不到的管道也算
- 做法：在文件與 worker 腳本的回應送 `Connection-Allowlist: (response-origin "https://api.example.com" …); report-to=…`，配 `Reporting-Endpoints` 與 `Vary: Sec-Fetch-Dest`；Dedicated／Shared Worker 給相同清單，Service Worker 給所有受控文件的聯集；可同時送 `-Report-Only` 試更嚴的清單
- 對手：CSP 要分資源類型各寫指令，而且管不到 `dns-prefetch`、`preconnect`、WebRTC 這類預測性或非 Fetch 的管道，被入侵的頁面腳本還能透過 `worker.postMessage()` 把資料送出去（引用："does not govern speculative or non-Fetch network channels such as `<link rel="dns-prefetch">`, `<link rel="preconnect">`, or WebRTC"）
- 退路：失去主要好處——退回 CSP 時只管得住 `fetch()`、子資源與表單送出，DNS 預取、預連線與 WebRTC 這些管道又漏出去
- 解鎖：以前 CSP 要分資源類型各寫指令，也管不到 DNS 預取、預連線與 WebRTC；現在一個網路層清單就管住所有對外連線

經過：寫好了 CSP，資料還是能從 DNS 預取、預連線或 WebRTC 溜出去。改成在網路層列出「只准連這些地方」，所有管道一起管；只是目前僅 Chromium 執行。
%% line-end %%

### 細節（不索引）
- 對手組：敏感資料外露
- 支援狀態：Connection allowlists：Limited availability。Supported by: Chrome 152, Edge 152。Unsupported in: Firefox and Safari
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：密碼產生器、本機筆記、錢包這類「資料不該離開這頁」的工具，可以在回應標頭宣告只連自己（甚至載入後 `()` 全斷），讓使用者或稽核者確認它不會偷偷回傳。目前僅 Chromium
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:restrict-outbound-connections:2" %%
## 清單語法寫錯或忘了預設值，合法連線也全被擋
- 做法：標頭寫成 RFC 9651 Inner List `(...)`、項目以空白分隔、`response-origin` 與參數不加引號；只到來源的樣式去掉結尾斜線或寫 `/*`；`ws(s)://` 改寫成 `http(s)://`；把外部導覽目標（OAuth、金流）列進清單；需要時加 `; redirects=allow`、`; webrtc=allow`；用戶端 `fetch` 包 `try/catch` 顯示被擋狀態
- 對手：非空的標頭解析失敗時，瀏覽器以空清單「失效即關閉」，擋掉所有對外連線；`new URL()` 補上的結尾斜線讓樣式只符合根路徑；預設連同源的 3xx 重新導向都擋（引用："the browser fails closed with an empty allowlist and blocks **all** outbound network connections."）
- 退路：保住主要行為——退回 Report-Only 觀察或退回 CSP，標頭寫錯也不會讓全站連線中斷
- 解鎖：（缺）

經過：少一對括號或多一個斜線，頁面上每個請求都失敗，或只有根路徑能通。這個標頭對錯誤的反應是全關，所以要照格式產生、先用 Report-Only 觀察。
%% line-end %%

### 細節（不索引）
- 對手組：合法連線被安全規則擋下
- 支援狀態：同 mwg:restrict-outbound-connections，記 Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:restrict-outbound-connections:3" %%
## 退回 CSP 時要明寫 `form-action` 與 `worker-src 'self'`
- 做法：不支援 `Connection-Allowlist` 的瀏覽器搭配 CSP：明寫 `form-action`、`worker-src 'self'`（不含 `blob:`），`connect-src` 列出 `wss://` 來源
- 對手：`default-src` 不會套用到 `<form action>`；沒限制 `worker-src`，受限頁面可以開 `blob:` SharedWorker 繞過文件層的限制（引用："Include `worker-src 'self'` (excluding `blob:`) so restricted pages cannot spawn `blob:` SharedWorkers to bypass document-level restrictions."）
- 退路：不需要——CSP 的 `form-action`、`worker-src` 是既有指令，不涉及瀏覽器功能支援
- 解鎖：（缺）

經過：以為 `default-src 'self'` 已經全包，表單卻還能送到任何地方，worker 也能另起爐灶。這兩個指令要明寫。
%% line-end %%

### 細節（不索引）
- 對手組：敏感資料外露
- 支援狀態：CSP：指南只附 Connection-Allowlist 的支援資料，沒附 CSP 的，記不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 1 個糾錯提醒未拆（嵌入用的 `<iframe connectionAllowlist>` 與 `Allow-Connection-Allowlist-From` 尚未預設啟用，正式環境不要依賴）
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
