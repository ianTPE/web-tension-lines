---
guide: passkey-management
category: security
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/security/passkey-management.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 通行金鑰管理

%% line-start id="mwg:passkey-management" %%
## 用 `signalAllAcceptedCredentials()` 與 `signalCurrentUserDetails()` 讓密碼管理器跟上伺服器
- 做法：管理頁載入時與刪除憑證後呼叫 `signalAllAcceptedCredentials({ rpId, userId, allAcceptedCredentialIds })`；使用者改帳號名稱或顯示名稱後呼叫 `signalCurrentUserDetails()`；單純改通行金鑰暱稱只改伺服器；每列顯示 AAGUID 對應的提供者名稱與圖示、建立與最後使用日期
- 對手：指南只說 Signal API 讓使用者同步的保管庫與後端資料庫保持一致，沒說不同步時在哪個時刻出問題（引用："The Signal API lets the application communicate credential states to password managers, keeping the user's synced vaults and your backend database in lockstep."）
- 退路：失去主要好處——Firefox 沒有 Signal API 也沒有 polyfill，背景同步只能略過，密碼管理器與伺服器仍然對不上
- 解鎖：以前在網站設定頁刪掉或改名通行金鑰，手機的密碼管理器不會跟著變；現在可以用 Signal API 把兩邊同步

經過：使用者在網站設定頁刪了一個通行金鑰、改了帳號名稱，手機的密碼管理器裡卻還是舊的。管理頁一載入、一刪除、一改名就送出信號，兩邊才對得上。
%% line-end %%

### 細節（不索引）
- 對手組：憑證狀態錯亂
- 支援狀態：Web authentication signal methods：Limited availability。Supported by: Chrome 132, Edge 132, Safari 26。Unsupported in: Firefox
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：帳號設定頁可以做到「在這裡刪掉，手機上的密碼管理器也跟著消失；在這裡改名，下次登入選單顯示新名字」，不必要使用者自己去密碼管理器清。Firefox 不支援
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:passkey-management:2" %%
## Signal API 的 `rpId` 用伺服器給的，不要用 `window.location.hostname`
- 做法：列表與帳號更新端點回傳伺服器設定的 `rpId`，用戶端呼叫 Signal API 時直接使用
- 對手：憑證註冊在上層網域或透過 Related Origin Requests 共用時，`window.location.hostname` 對不上，同步默默送錯 RP ID 或丟出 `SecurityError`（引用："`window.location.hostname` will not match the credential's RP ID, causing password manager synchronization to silently target the wrong RP ID or throw a `SecurityError`."）
- 退路：保住主要行為——沒有 Signal API 的瀏覽器本來就略過同步，不會送錯 RP ID；支援的瀏覽器用伺服器給的值就對得上
- 解鎖：（缺）

經過：設定頁在 `accounts.example.com`，通行金鑰卻註冊在 `example.com`。用目前網址當 RP ID，信號就送去一個不存在的地方。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：同 mwg:passkey-management，記 Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:passkey-management:3" %%
## 傳給 Signal API 的 ID 必須是合法的 Base64URL，失敗只 `console.warn`
- 做法：所有 `userId` 與憑證 ID（包括原型資料與模擬後端）都存成不帶補位的 Base64URL；呼叫前先驗格式、不合法就跳過；Signal API 呼叫包在 `try/catch`，失敗用 `console.warn` 而非 `console.error`
- 對手：傳入 `'passkey-1'` 這類人類可讀的假 ID，頁面一載入就丟 `TypeError`；被動同步失敗印成 `console.error`，讓 Lighthouse 的 `errors-in-console` 判定失敗（引用："Passing arbitrary human-readable placeholder or mock IDs (…) throws `TypeError: Invalid base64url string for allAcceptedCredentialIds` on page load."）
- 退路：保住主要行為——ID 不合法就自己跳過同步，頁面照常載入，失敗也只印警告不會中斷
- 解鎖：（缺）

經過：開發時用好讀的假資料，正式上線前沒人注意，Signal API 一載入就把頁面炸掉。先驗格式、失敗降級成警告，背景同步才真的是「背景」。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：同 mwg:passkey-management，記 Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 1 個糾錯提醒未拆（AAGUID 全為 0 時不要查註冊表，改用通用名稱；AAGUID 只能當 UX 提示，見 mwg:passkeys:2）
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
