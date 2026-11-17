---
guide: local-network-access
category: security
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/security/local-network-access.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 區域網路存取

%% line-start id="mwg:local-network-access" %%
## 用 `targetAddressSpace` 讓 https 頁面連到區網的 http 裝置
- 做法：對區網裝置（印表機、IoT hub、路由器）或本機輔助程式的 `fetch()`／`Request` 加 `targetAddressSpace: 'local'` 或 `'loopback'`；經使用者授予 `local-network`／`loopback-network` 權限後連線
- 對手：混合內容檢查在 DNS 解析之前就執行，https 頁面對區網 http 端點的請求會被當成混合內容擋下（引用："Mixed Content checks run *before* DNS resolution. Declaring `targetAddressSpace: 'local'` (…) informs the browser ahead of DNS resolution that an `http://` URL (…) targets a local/loopback endpoint and should be exempted from Mixed Content blocking once the user grants the permission."）
- 退路：失去主要好處——不支援的瀏覽器沒有位址空間宣告，https 頁面對區網 http 端點仍被混合內容擋下，只能改連 https 端點
- 解鎖：以前 https 頁面連不到家裡的 http 裝置；現在瀏覽器先問過使用者就放行，還會確認主機名稱沒有解析到公網

經過：家裡的裝置只講 http，網頁卻一定是 https，兩邊連不起來。先宣告「我要連區網」，瀏覽器問過使用者就放行，還會確認主機名稱沒有解析到公網。
%% line-end %%

### 細節（不索引）
- 對手組：合法連線被安全規則擋下
- 支援狀態：Local network access：Limited availability。Supported by: Chrome 145, Edge 145。Unsupported in: Firefox and Safari
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：智慧家電、3D 印表機、NAS 的設定頁可以直接做成公開的 https 網頁，連到使用者家裡的裝置，不必再發行桌面 app 或要人輸入 IP 開 http 頁面。目前僅 Chromium
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:local-network-access:2" %%
## 區網請求等使用者點擊才發，不在載入時或 Service Worker 裡發
- 做法：先用 `navigator.permissions.query({ name: 'local-network' })` 查狀態：`granted` 就直接連；`prompt` 時先說明原因，由按鈕點擊觸發；`denied` 時顯示如何在網站設定重新開啟；頁面一律用 https
- 對手：從 Service Worker 或 Shared Worker 發出第一個需要授權的請求，沒有附屬的 Document，權限還沒給就立刻失敗；不安全的 http 頂層頁面則直接被拒（引用："never initiate the first permission-triggering request from a **Service Worker** or **Shared Worker** (which lack an attached `Document` and will immediately fail if permission is not already `'granted'`)."）
- 退路：保住主要行為——不支援的瀏覽器用 `try/catch` 把權限當成 `'prompt'`，一樣等使用者點擊才發請求
- 解鎖：（缺）

經過：一載入就去連區網，使用者還不知道為什麼就看到權限提示；放在 worker 裡更慘，連提示都沒有就失敗。改成先查狀態、讓使用者按按鈕，再發請求。
%% line-end %%

### 細節（不索引）
- 對手組：權限請求不看時機
- 支援狀態：同 mwg:local-network-access，記 Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 交叉核對仲裁：解鎖改為缺

%% line-start id="mwg:local-network-access:3" %%
## 不要查詢舊的 `'local-network-access'` 權限名：舊版 Chrome 會整個分頁崩潰
- 做法：只查詢細分的 `'local-network'`／`'loopback-network'`，包在 `try/catch` 裡，不認得時當成 `'prompt'`
- 對手：查詢合併的舊權限名，舊版 Chrome 的渲染程序直接崩潰，`try/catch` 也救不了（引用："In older Chrome versions this query crashes the renderer process, and `try / catch` cannot prevent it."）
- 退路：保住主要行為——只查新的細分權限名，舊瀏覽器認不得就當成 `'prompt'`，分頁不會崩潰
- 解鎖：（缺）

經過：為了相容想多查一個舊名稱，結果在舊版 Chrome 上把整個分頁弄當。只用新名稱，例外就能被正常接住。
%% line-end %%

### 細節（不索引）
- 對手組：功能偵測不可靠
- 支援狀態：同 mwg:local-network-access，記 Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:local-network-access:4" %%
## `WebSocket` 不吃 `{ targetAddressSpace }`，靠網址本身被辨認
- 做法：`new WebSocket(url, protocols)` 第二個參數只放子協定；用私有／回送 IP、`localhost` 或 `.local` 主機名讓瀏覽器從網址辨認；自訂 DNS 名稱的本機端點改用 `wss://`；`WebTransport` 也不傳 `targetAddressSpace`
- 對手：把 `{ targetAddressSpace }` 物件當第二個參數傳給 `WebSocket`，直接丟出 `SyntaxError`（引用："do **not** pass a `{ targetAddressSpace }` options object, which throws a `SyntaxError`."）
- 退路：保住主要行為——不支援的瀏覽器沒有這組權限提示，WebSocket 仍照網址辨識，出錯照樣自己接
- 解鎖：（缺）

經過：`fetch` 要宣告位址空間，照樣套到 `WebSocket` 上卻直接報錯。WebSocket 的判斷靠網址長相，不靠選項。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：同 mwg:local-network-access，記 Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:local-network-access:5" %%
## 跨來源 iframe 要連區網，得用 `allow` 與 `Permissions-Policy` 委派
- 做法：`<iframe allow="local-network; loopback-network">`，並在**外層文件**的回應送 `Permissions-Policy: local-network=(self "https://partner…")`
- 對手：兩個權限的預設允許清單只有 `'self'`，嵌入的跨來源 iframe 無法發出區網或本機請求（引用："`local-network` and `loopback-network` have a default allowlist of `'self'`, blocking cross-origin `<iframe>` embeds from making local or loopback requests."）
- 退路：沒說——指南未交代不支援時怎麼辦
- 解鎖：（缺）

經過：合作夥伴的裝置設定頁嵌在 iframe 裡，連不到使用者的裝置。由外層頁面明確授權，iframe 才拿得到權限。
%% line-end %%

### 細節（不索引）
- 對手組：合法連線被安全規則擋下
- 支援狀態：同 mwg:local-network-access，記 Limited
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 1 個糾錯提醒未拆（不要再新增已棄用的 Private Network Access 預檢標頭）
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 交叉核對仲裁：退路改為「沒說」、解鎖改為缺
