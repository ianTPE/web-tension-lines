---
guide: privacy
category: privacy
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/privacy/privacy.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 給開發者的網頁隱私準則

%% line-start id="mwg:privacy" %%
## 只收最低粒度的資料：問年齡區間，不問生日
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：用最低必要粒度收集資料（年齡區間 `<select>` 取代出生日期）；提供訪客結帳；用完即刪；彙總統計時加雜訊（差分隱私）；不「以防萬一」先收
- 被什麼擋：收了用不到的資料，外洩時就會一起丟掉（引用："If you don't have the data, you can't lose it."）
- 戰報：部分改善——儲存的資料越少，外洩風險越低，使用者也更信任（官方宣稱）

經過：多收一個欄位當下沒成本，出事時卻是多一份要賠的資料。只收任務需要的那一層粒度，沒收的就不會外洩。
%% line-end %%

### 細節（不索引）
- 對手組：敏感資料外露
- 支援狀態：指南未附瀏覽器支援資料，記不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:privacy:2" %%
## 工作階段識別碼放 `HttpOnly` cookie，不放 `localStorage`
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：存工作階段 ID 的 cookie 加 `HttpOnly`（並配 `Secure`、`SameSite=Lax`）；敏感權杖與個資不放 `localStorage`
- 被什麼擋：`localStorage` 裡的權杖與個資，頁面上任何嵌入的腳本都讀得到（引用："DON'T store sensitive tokens or PII in `localStorage`, as it is accessible by any embedded script."）
- 戰報：勝——`HttpOnly` cookie 不讓其他腳本存取（官方宣稱）

經過：權杖放 `localStorage` 很方便，頁面上每一支第三方腳本也一樣方便。改成 `HttpOnly`，腳本就碰不到。
%% line-end %%

### 細節（不索引）
- 對手組：敏感資料外露
- 支援狀態：指南未附瀏覽器支援資料，記不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:privacy:3" %%
## 登出時送 `Clear-Site-Data`，不讓資料留在瀏覽器
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：使用者登出時回應 `Clear-Site-Data: "*"`；要清快取時改由子資源觸發，不放在主導覽頁
- 被什麼擋：登出後資料仍殘留在瀏覽器裡（引用："DO use the `Clear-Site-Data` header when a user logs out to ensure no lingering data remains in the browser."）
- 戰報：勝——登出後瀏覽器裡不留殘餘資料（官方宣稱）

經過：共用電腦上登出了，cookie、儲存區、快取卻還在。一個回應標頭就讓瀏覽器全部清掉。
%% line-end %%

### 細節（不索引）
- 對手組：敏感資料外露
- 支援狀態：指南未附瀏覽器支援資料，記不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:privacy:4" %%
## 設嚴格的 `Referrer-Policy`，別把網址參數漏給第三方
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：回應 `Referrer-Policy: strict-origin-when-cross-origin`
- 被什麼擋：網址裡的敏感參數經由 Referer 外流給第三方（引用："DO set a strict `Referrer-Policy` to prevent leaking sensitive URL parameters to third parties."）
- 戰報：勝——跨來源請求只帶來源，不帶路徑與查詢參數（官方宣稱）

經過：網址裡有搜尋字詞、訂單編號，每個第三方資源請求都把它們帶出去。限制 Referer 之後，第三方只知道你從哪個網站來。
%% line-end %%

### 細節（不索引）
- 對手組：敏感資料外露
- 支援狀態：指南未附瀏覽器支援資料，記不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:privacy:5" %%
## 敏感端點加速率限制，擋大量抓取
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：使用者搜尋、個人頁瀏覽等敏感端點實作速率限制
- 被什麼擋：敏感端點被拿來大量抓取使用者資料（引用："DO implement rate limiting on sensitive endpoints (e.g., user search or profile views) to prevent bulk data scraping."）
- 戰報：勝——大量抓取被擋下（官方宣稱）

經過：個人頁一頁一頁都是公開的，合起來就是一份名冊。限制速率，抓取就做不成規模。
%% line-end %%

### 細節（不索引）
- 對手組：敏感資料外露
- 支援狀態：指南未附瀏覽器支援資料，記不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:privacy:6" %%
## 重型嵌入用 façade、分享按鈕用靜態連結，不讓第三方先追蹤
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：YouTube、TikTok 等嵌入先顯示靜態縮圖，點了才載入 iframe（可用 `youtube-nocookie.com`）；社群分享 SDK 換成純 HTML 連結；處理結帳、健康資訊的頁面不載第三方腳本；定期用 DevTools 或 HAR 稽核網路請求
- 被什麼擋：第三方腳本與資源是常見的隱私外洩來源（引用："Third-party scripts and resources are a common source of privacy leaks."）
- 戰報：勝——使用者點下去之前不載入第三方 iframe；靜態分享連結不追蹤使用者（官方宣稱）

經過：頁面上放一個影片嵌入、一排分享按鈕，訪客還沒點任何東西就已經被第三方記錄。先放靜態替身，等使用者表達意圖才載入。
%% line-end %%

### 細節（不索引）
- 對手組：使用者被暗中追蹤
- 支援狀態：指南未附瀏覽器支援資料，記不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:privacy:7" %%
## 用 FedCM 中介「用某某帳號登入」，加上 CHIPS 分割 cookie
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：第三方登入改用 Federated Credential Management API（`navigator.credentials.get({ identity })`）；一對一嵌入的 cookie 加 `Partitioned`（CHIPS），不依賴未分割的 `SameSite=None` cookie
- 被什麼擋：身分提供者在使用者同意之前就能追蹤使用者去了哪些網站（引用："use the **Federated Credential Management API (FedCM)** to mediate "Sign-In" flows natively, preventing IdP tracking of Relying Parties prior to user consent."）
- 戰報：勝——登入流程由瀏覽器原生中介，使用者同意前身分提供者看不到依賴方（官方宣稱）

經過：每個網站放一顆「用 X 登入」按鈕，X 就知道使用者逛過哪些網站，哪怕從沒按過。由瀏覽器居中之後，同意前什麼都不透露。
%% line-end %%

### 細節（不索引）
- 對手組：使用者被暗中追蹤
- 支援狀態：指南未附瀏覽器支援資料，記不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：小型網站可以提供「用某某帳號登入」，又不讓身分提供者在使用者按下之前就知道誰來過；嵌入式小工具的偏好設定用分割 cookie 保存，不變成跨站追蹤器
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:privacy:8" %%
## 用功能偵測與 UA Client Hints 取代指紋與 UA 字串
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：用功能偵測（`'IntersectionObserver' in window`）判斷能力；真的需要鎖定裝置時用 `navigator.userAgentData.getHighEntropyValues()` 只要必要的欄位；不用 canvas、字型清單、媒體裝置列舉做指紋，不依賴完整的 `navigator.userAgent`
- 被什麼擋：指紋依賴不變的特徵、在看不見的地方發生，使用者無法退出也無法清除識別碼（引用："Fingerprinting takes away user control because it relies on unchanging characteristics and happens invisibly, preventing users from opting out or clearing their identifier."）
- 戰報：缺——指南只要求改用功能偵測與 UA-CH，沒說 UA-CH 對指紋的影響有多少（官方宣稱）

經過：為了判斷瀏覽器能力去解析 UA 字串、讀 canvas，順手就做出了使用者刪不掉的識別碼。改成問「有沒有這個功能」，需要時才要明確的裝置欄位。
%% line-end %%

### 細節（不索引）
- 對手組：使用者被暗中追蹤
- 支援狀態：指南未附瀏覽器支援資料，記不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 缺
- 類型：新能力
- 解鎖（發想，非指南原文）：需要分平台下載連結或依 CPU 架構給安裝檔的頁面，可以只要求平台版本與架構兩個欄位，不必解析整串 UA 或做指紋
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:privacy:9" %%
## 用 `<permission>` 元素讓權限請求由使用者主動發起
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在支援時用 Page Embedded Permission Control（`<permission type="geolocation">`）宣告式地請求權限，裡面放一般按鈕當退路；請求相機、位置等強大權限前先說明原因與情境
- 被什麼擋：指南只要求在請求權限前提供清楚的理由與情境，沒說直接跳出權限請求在哪個時刻出問題（引用："DO provide a clear reason and context *before* requesting powerful browser permissions (e.g., camera, location)."）
- 戰報：缺——指南只說 `<permission>` 讓權限請求變得宣告式、由使用者發起、作為資料中介，沒說它對哪個問題改善了多少（官方宣稱）

經過：權限對話框常在使用者還不知道為什麼時就跳出來。`<permission>` 讓請求變成頁面上一顆由使用者自己按的控制項；不支援時就是一般按鈕。
%% line-end %%

### 細節（不索引）
- 對手組：權限請求不看時機
- 支援狀態：指南未附瀏覽器支援資料（只寫 "if supported"），記不適用
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 缺
- 類型：新能力
- 解鎖（發想，非指南原文）：地圖或找附近店家的頁面可以把「使用我的位置」做成頁面內一顆原生控制項，權限請求一定來自使用者點擊，不再在載入時就跳出對話框
- 另有 6 個糾錯提醒未拆（不要把隱私工作丟給使用者、不要用欺騙性設計騙取同意、目的限制、`Permissions-Policy` 預設關閉強大功能、記錄檔去除個資、資料存取與刪除權）
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出
