---
guide: passkey-authentication
category: security
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/security/passkey-authentication.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 通行金鑰登入

%% line-start id="mwg:passkey-authentication" %%
## 用條件式中介（`mediation: "conditional"`）讓通行金鑰出現在表單自動填入裡
- 做法：伺服器回傳 `allowCredentials: []` 的可發現憑證選項；欄位標 `autocomplete="username webauthn"`；載入時用 `PublicKeyCredential.getClientCapabilities()` 確認 `conditionalGet`，再以 `mediation: "conditional"` 與 `AbortController` 呼叫 `navigator.credentials.get()`；另備一顆「用通行金鑰登入」按鈕
- 對手：指南只說可發現憑證讓使用者不必先輸入帳號、由通行金鑰提供者列出帳戶，沒說先輸入帳號的流程在哪個時刻出問題（引用："This requests discoverable credentials, meaning the user does not need to enter their username first; the passkey provider will present available accounts."）
- 退路：保住主要行為——不支援時載 `webauthn-polyfills`，條件式中介與自動填入建議照樣可用
- 解鎖：以前登入要先輸入帳號才會出現通行金鑰；現在可發現憑證讓帳號欄位的自動填入直接列出通行金鑰，點一下就登入

經過：登入頁一開，帳號欄位的自動填入選單裡就有通行金鑰，點一下就登入，不必先打帳號。不支援的環境照常用密碼表單。
%% line-end %%

### 細節（不索引）
- 對手組：登入打斷使用者
- 支援狀態：getClientCapabilities()：Newly available（2025-02-06），Chrome 133, Edge 133, Firefox 135, Safari 17.4；parseRequestOptionsFromJSON()：Newly available（2025-03-31）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：個人網站或小工具可以只放一個帳號欄位，使用者點一下就用手機或電腦裡的通行金鑰登入，不必設計密碼重設流程
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:passkey-authentication:2" %%
## 按鈕登入前先中止背景的條件式請求，避免兩個提示相撞
- 做法：按下「用通行金鑰登入」時先 `abort()` 掛著的條件式 `get()`、換一個新的 `AbortController`；按鈕流程被取消後重新掛回條件式自動填入；`NotAllowedError`、`AbortError` 視為預期例外
- 對手：背景的條件式請求還在時又發出明確的通行金鑰提示，兩者相撞（引用："Abort any pending Conditional Get call to prevent passkey prompt collisions"）
- 退路：保住主要行為——`AbortController` 早已 Widely，中止背景請求再重新掛上，這個流程不受支援度影響
- 解鎖：（缺）

經過：自動填入的請求在背景等著，使用者又按了按鈕，兩個 WebAuthn 請求打架。先取消背景那個，取消後再掛回去。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：同上，記 Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:passkey-authentication:3" %%
## 伺服器找不到憑證時，用 `signalUnknownCredential()` 通知密碼管理器
- 做法：伺服器查無憑證 ID 時明確回 HTTP 404；用戶端只在 404 且尚未登入時呼叫 `PublicKeyCredential.signalUnknownCredential({ rpId: publicKey.rpId, credentialId: encoded.id })`，先做功能偵測
- 對手：指南只說 Signal API 用來讓密碼管理器與伺服器的憑證狀態保持同步，沒說不同步時在哪個時刻出問題（引用："The WebAuthn Signal API (`webauthn-signals`) is a progressive optimization used to keep password managers in sync with the server credential state."）
- 退路：失去主要好處——Firefox 不支援 Signal API，背景同步直接略過，已刪的憑證仍留在密碼管理器裡
- 解鎖：以前伺服器刪掉憑證，密碼管理器裡還留著一個按了必定失敗的選項；現在伺服器回 404，瀏覽器能通知提供者把它清掉

經過：伺服器已經刪掉的通行金鑰，還留在使用者的密碼管理器裡。登入時回 404，瀏覽器就能通知提供者把它處理掉。
%% line-end %%

### 細節（不索引）
- 對手組：憑證狀態錯亂
- 支援狀態：Web authentication signal methods：Limited availability。Supported by: Chrome 132, Edge 132, Safari 26。Unsupported in: Firefox
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：網站可以主動清理使用者密碼管理器裡的過期通行金鑰，帳號刪除或憑證撤銷後，使用者不會再看到一個按了必定失敗的選項。Firefox 不支援
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:passkey-authentication:4" %%
## 使用者驗證等級存在伺服器工作階段，不從用戶端傳回
- 做法：產生選項時把 `userVerification` 等級寫進伺服器工作階段；驗證端點依工作階段裡的值決定是否 `requireUserVerification`
- 對手：從用戶端（例如查詢字串）傳回驗證等級，等於讓用戶端自己決定要不要驗生物特徵或 PIN（引用："The requested `userVerification` constraint level MUST be persisted inside the server session record at the options endpoint, rather than passed back from the client via query strings. This allows the verification endpoint to enforce strict matching constraints safely without risk of client manipulation."）
- 退路：保住主要行為——這是伺服器端的流程設計，不受瀏覽器支援度影響
- 解鎖：（缺）

經過：要求「必須驗 PIN」的設定若由瀏覽器傳回來，改個參數就能跳過。存在伺服器上，驗證時照自己的紀錄比對。
%% line-end %%

### 細節（不索引）
- 對手組：內容遭竄改未察覺
- 支援狀態：同上，記 Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 3 個糾錯提醒未拆（rpId 一律取自伺服器選項而非 `window.location.hostname`，見 mwg:passkeys；`credentialId` 要傳 Base64URL 字串而非 `rawId`；`autofocus` 只用在專門的登入頁並配 `aria-describedby`）
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
