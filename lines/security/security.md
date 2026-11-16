---
guide: security
category: security
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/security/security.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 網頁安全

%% line-start id="mwg:security" %%
## 用 nonce 加 `'strict-dynamic'` 取代腳本網域白名單
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：CSP 的 `script-src` 用每次請求新產生的 nonce（靜態 HTML 改用腳本雜湊）加 `'strict-dynamic'` 與 `'report-sample'`，再搭配 `object-src 'none'`、`base-uri 'none'`、`frame-ancestors`；第三方分析腳本靠 `'strict-dynamic'` 載入自己的相依，不把它的網域加進白名單
- 被什麼擋：以 `https:` 或 `script-src https://cdn.example.com` 這種網域白名單當主要防線，攻擊者可以透過白名單網域上的開放重新導向、JSONP 端點或相依注入繞過（引用："they are easily bypassed by open redirects, JSONP endpoints, and dependency injection on the allowed origin."）
- 戰報：勝——只有帶著當次 nonce 的腳本（以及它們載入的相依）能執行，白名單網域上的漏洞不再等於放行；指南稱這是防止 XSS 的主要機制（官方宣稱）

經過：白名單看起來很嚴，實際上等於信任那個網域上的每一個端點。改成 nonce 之後，信任的是「這次回應裡我自己寫的那幾個 `<script>`」。
%% line-end %%

### 細節（不索引）
- 對手組：防線形同虛設
- 支援狀態：CSP：指南未給瀏覽器支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:security:2" %%
## nonce 要在樣板裡發給自己的腳本，不要事後用正規表示式蓋章
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在伺服器或 SSR middleware 每次請求用 `crypto.getRandomValues()` 產生 nonce，同時放進 `Content-Security-Policy` 標頭並傳入樣板的渲染脈絡，只有樣板裡開發者寫的 `<script>` 拿到 nonce
- 被什麼擋：對已經渲染好的 HTML 用正規表示式替每個 `<script>` 補上 nonce，分不出哪個是開發者寫的、哪個是反射或儲存型注入塞進來的，等於替攻擊者的腳本授權（引用："authorizing attacker-injected scripts under `script-src 'nonce-...'`."）
- 戰報：勝——nonce 只在樣板渲染時發給可信的標籤，注入進來的 `<script>` 拿不到（官方宣稱）

經過：為了趕快上 CSP，有人在輸出前掃一遍 HTML 幫所有 `<script>` 蓋章。這一步把 CSP 最核心的判斷交給了正規表示式，而正規表示式看不出誰是自己人。
%% line-end %%

### 細節（不索引）
- 對手組：防線形同虛設
- 支援狀態：CSP nonce：指南未給瀏覽器支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:security:3" %%
## 不讓不可信字串進危險 sink，並用 Trusted Types 在執行期把關
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：設定文字用 `textContent`／`innerText`；插入不可信 HTML 用 `setHTML()`；以 `document.createElement` 或 DOMParser 建元素，不串接 HTML 字串；CSP 加 `require-trusted-types-for 'script'`，必要的 sink 寫入走具名的 `trustedTypes.createPolicy()`，不建立原樣回傳輸入的 pass-through 政策
- 被什麼擋：把不可信或未清理的輸入用 `innerHTML`、`setHTMLUnsafe` 寫進 DOM，形成 DOM XSS；直接回傳輸入的 pass-through 政策則讓 Trusted Types 的保護失效（引用："**DO NOT**: Use `innerHTML` or `setHTMLUnsafe` with untrusted or unsanitized input."）
- 戰報：勝——Trusted Types 在執行期擋下對 `innerHTML`、`outerHTML`、`document.write`、`script.src` 的原始字串指派，除非經過具名政策（官方宣稱）

經過：`innerHTML`、`eval`、帶字串的 `setTimeout` 是要 grep 出來的清單。原始碼層級的約定靠人遵守，Trusted Types 把同一條規則變成執行期的錯誤。
%% line-end %%

### 細節（不索引）
- 對手組：不可信內容當HTML解析
- 支援狀態：本指南未給 Trusted Types 支援資料，記 不適用（`trusted-types` 指南記 Newly，見 mwg:trusted-types）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:security:4" %%
## HSTS 的 max-age 從短的開始逐步拉長
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：送 `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload` 強制 HTTPS；正式上線時先用約 300 秒的 `max-age`，確認無誤再逐步加到一年
- 被什麼擋：一開始就送很長的 `max-age`，若設定有誤，網站在每個見過這個標頭的瀏覽器裡都打不開，直到快取過期（引用："A misconfigured HSTS with a long max-age can render the site permanently inaccessible until the cache expires in every browser that saw it."）
- 戰報：部分改善——從短的 `max-age` 起步，設錯時被鎖住的時間只到短快取過期為止；拉長之後就回到同樣的風險（官方宣稱）

經過：HSTS 一送出就收不回來，瀏覽器會記住整整一年。所以先送五分鐘，看清楚子網域都跟得上 HTTPS，再一步步放長。
%% line-end %%

### 細節（不索引）
- 對手組：合法連線被安全規則擋下
- 支援狀態：HSTS：指南未給瀏覽器支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:security:5" %%
## 工作階段 cookie 用 `__Host-` 前綴加 `HttpOnly`
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：單一網域的第一方工作階段 cookie 命名為 `__Host-session`（必須 `Secure`、`Path=/`、不設 `Domain`），不適用時用 `__Secure-`；工作階段與驗證 cookie 設 `HttpOnly`，並明確設 `SameSite=Lax`
- 被什麼擋：工作階段 cookie 沒有 `HttpOnly`，被注入的用戶端腳本讀得到（引用："Set `HttpOnly` (`httpOnly: true`) on session and authentication cookies so they cannot be read by injected client-side scripts"）
- 戰報：勝——`HttpOnly` 讓注入的腳本讀不到工作階段 cookie；`__Host-` 前綴擋住同站與網路攻擊者（官方宣稱）

經過：一旦頁面有 XSS，能讀 cookie 的腳本就能把登入狀態帶走。把 cookie 設成腳本碰不到，XSS 的損害就少一大塊。
%% line-end %%

### 細節（不索引）
- 對手組：敏感資料外露
- 支援狀態：Cookie 屬性與前綴：指南未給瀏覽器支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:security:6" %%
## 會被嵌入第三方頁面的 app 改用分割 cookie
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：應用程式會以 iframe 嵌入第三方情境時，cookie 設 `SameSite=None; Secure; Partitioned`
- 被什麼擋：依賴未分割的 `SameSite=None` cookie，這類 cookie 正因防追蹤而被系統性封鎖（引用："Rely on unpartitioned `SameSite=None` — these are being systematically blocked for tracking prevention."）
- 戰報：缺——指南只要求改用 `Partitioned`，沒說改了之後嵌入情境的 cookie 會怎樣

經過：嵌入式小工具一直靠第三方 cookie 記住使用者，而瀏覽器正在把這條路關掉。指南指出的出路是分割 cookie：每個嵌入它的網站各有一份。
%% line-end %%

### 細節（不索引）
- 對手組：合法連線被安全規則擋下
- 支援狀態：CHIPS（Partitioned）：指南未給瀏覽器支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 缺
- 類型：新能力
- 解鎖（發想，非指南原文）：以前第三方 cookie 一被封鎖，嵌在別人頁面裡的留言框、客服視窗、付款小工具就記不住使用者 → 現在可以用分割 cookie 保住「在這個網站裡」的登入與偏好，不必變成跨站追蹤器。同 mwg:privacy:7 的 CHIPS
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:security:7" %%
## 依嵌入需求選 `frame-ancestors` 層級，跨來源夥伴就別再送 X-Frame-Options
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：不需嵌入時送 `frame-ancestors 'none'` 加 `X-Frame-Options: DENY`；只有同源嵌入時用 `'self'` 加 `SAMEORIGIN`；要讓特定跨來源夥伴嵌入時只用 `frame-ancestors 'self' https://trusted-partner.com`，省略 `X-Frame-Options`
- 被什麼擋：需要跨來源嵌入時還送 `X-Frame-Options: DENY` 或 `SAMEORIGIN`，只看 XFO 不看 `frame-ancestors` 的用戶端會把嵌入擋掉（引用："`DENY` or `SAMEORIGIN` would block the embed in any client that evaluates `X-Frame-Options` without `frame-ancestors`"）
- 戰報：勝——每一層都有對應寫法，防點擊劫持的同時不擋掉合法夥伴的嵌入（官方宣稱）

經過：X-Frame-Options 只能說「全擋」或「只准同源」，`ALLOW-FROM` 早已沒人支援。要放行特定夥伴時，留著 XFO 反而讓某些用戶端把夥伴也擋在外面。
%% line-end %%

### 細節（不索引）
- 對手組：合法連線被安全規則擋下
- 支援狀態：frame-ancestors、X-Frame-Options：指南未給瀏覽器支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:security:8" %%
## 用 `Document-Isolation-Policy` 取得跨來源隔離，不必替每個子資源補 CORP
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：只有需要 `SharedArrayBuffer`（例如 WebAssembly 多執行緒）才做跨來源隔離；Chromium 環境優先送 `Document-Isolation-Policy: isolate-and-credentialless`，對非 CORS 的跨來源資源剝掉憑證而不是擋下；需要擋下時改用 `isolate-and-require-corp`
- 被什麼擋：跨瀏覽器的做法（`COOP: same-origin` 加 `COEP: require-corp`）要求每個嵌入的子資源都送 CORP 標頭，否則瀏覽器不載入（引用："Every embedded subresource (images, styles, external media) MUST serve an explicit `Cross-Origin-Resource-Policy` header or the browser will prevent it from loading."）
- 戰報：僵持——`Document-Isolation-Policy` 讓沒有 CORP 的跨來源資源照樣載入（只是不帶憑證）；但主要只有 Chrome 142 起支援，其他廠商還沒表態，跨瀏覽器仍得走 COEP 那條路（官方宣稱）

經過：為了用 SharedArrayBuffer 開啟隔離，頁面上每張第三方圖片都得對方配合加標頭，不配合的就破圖。新政策改成「載入但不帶 cookie」，只是目前只在 Chrome。
%% line-end %%

### 細節（不索引）
- 對手組：合法連線被安全規則擋下
- 支援狀態：Document-Isolation-Policy：指南原文 "supported primarily in Chrome (142+) and other vendors have not yet shown interest"，記 Limited
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：以前要用 SharedArrayBuffer，頁面上每個第三方圖片、字型、影片都得對方補 CORP 標頭 → 現在瀏覽器裡的 Wasm 多執行緒工具（影片轉檔、本機影像處理）可以開啟隔離，同時照常嵌入外部素材。目前主要僅 Chrome
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:security:9" %%
## 用 Fetch Metadata 在驗證之前拒絕跨站請求
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：伺服器檢查 `Sec-Fetch-Site`／`Sec-Fetch-Mode`／`Sec-Fetch-Dest`，對非導覽端點拒絕 `cross-site` 請求，而且在驗證與授權檢查之前就拒絕；回應加 `Vary: Sec-Fetch-Dest, Sec-Fetch-Mode, Sec-Fetch-Site`；有子網域放使用者內容時，允許清單去掉 `same-site`
- 被什麼擋：在驗證之後才拒絕，回應時間會洩漏資源或工作階段是否存在；沒加 `Vary` 時，中間的 CDN 可能把快取的回應送給攻擊者（引用："Reject disallowed requests *before* authentication or authorization checks, so the response does not leak timing information about whether a resource or session exists."）
- 戰報：勝——提早拒絕不留時間差，`Vary` 讓快取依 Fetch Metadata 區分回應（官方宣稱）

經過：跨站請求擋下來了，可是擋的時機若在查完帳號之後，攻擊者光看回應快慢就能推出東西存不存在。先擋再查，快取也要記得分開存。
%% line-end %%

### 細節（不索引）
- 對手組：敏感資料外露
- 支援狀態：Fetch Metadata：指南未給瀏覽器支援資料（範例對沒有 `Sec-Fetch-Site` 的舊瀏覽器直接放行），記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:security:10" %%
## 帶憑證的 CORS 要回傳具體來源，不能用 `*`
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：伺服器驗證 `Origin` 請求標頭，把 `Access-Control-Allow-Origin` 動態設成該來源；先處理 `OPTIONS` 預檢
- 被什麼擋：需要 `Access-Control-Allow-Credentials: true` 時把 `Access-Control-Allow-Origin` 設成 `*`，瀏覽器拒絕這個回應（引用："Use wildcard `*` for `Access-Control-Allow-Origin` if `Access-Control-Allow-Credentials: true` is required — the browser will reject the response."）
- 戰報：勝——回傳驗證過的具體來源，帶憑證的跨來源讀取能成立，也不會對所有來源開放（官方宣稱）

經過：CORS 是授權不是防禦，最常見的錯是開太寬。開成 `*` 又要帶 cookie 的組合，瀏覽器直接不給讀。
%% line-end %%

### 細節（不索引）
- 對手組：合法連線被安全規則擋下
- 支援狀態：CORS：指南未給瀏覽器支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:security:11" %%
## 登出時送完整的 `Clear-Site-Data`
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：登出端點回應 `Clear-Site-Data: "cookies", "storage", "cache"`，三個指令都要有
- 被什麼擋：少了其中任何一個，工作階段 cookie、Web Storage 狀態或快取的已登入頁面就留在瀏覽器裡（引用："omitting any of these directives leaves active session cookies, Web Storage state, or cached authenticated pages behind."）
- 戰報：勝——三種資料一起清除，工作階段完整結束（官方宣稱）

經過：登出按鈕按了，伺服器的 session 也刪了，但瀏覽器的快取裡還留著上一頁的帳戶資料。共用電腦的下一個人按上一頁就看得到。
%% line-end %%

### 細節（不索引）
- 對手組：敏感資料外露
- 支援狀態：Clear-Site-Data：指南未給瀏覽器支援資料，記 不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出

%% line-start id="mwg:security:12" %%
## SRI 只用在不可變、有版本的資源上
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：第三方腳本與樣式表用 `integrity`（偏好 `sha384`、`sha512` 或 `sha256`）加 `crossorigin="anonymous"`，CDN 要送 `Access-Control-Allow-Origin`；只對固定版本的網址這樣做
- 被什麼擋：對會靜默更新、沒有版本的資源加 SRI，一更新雜湊就對不上，腳本執行失敗（引用："Use SRI for dynamic or unversioned assets — silent updates will cause script execution to fail."）
- 戰報：勝——SRI 只綁固定版本的資源，不會因上游更新而自己壞掉（官方宣稱）

經過：SRI 的意義就是「內容一變就不執行」，所以拿它去綁會自動更新的檔案，等於在上游下一次發版那天自己把網站弄壞。
%% line-end %%

### 細節（不索引）
- 對手組：合法連線被安全規則擋下
- 支援狀態：SRI：本指南未給瀏覽器支援資料，記 不適用（`secure-external-subresources` 指南記 Widely）
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 另有 7 個糾錯提醒未拆：postMessage 驗證 `event.origin`、指定目標來源（詳見 `validate-origins`）；違規報告雜訊多、要用 `'report-sample'` 與過濾；報告裡不放個資與權杖；COOP 不要直接上 `same-origin`；Fetch Metadata 設錯會擋掉 webhook 與 SSO；Permissions-Policy 誤擋委派功能讓第三方小工具靜默失敗、第三方 iframe 搶焦點；`X-Content-Type-Options: nosniff` 與正確的 `Content-Type`
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出
