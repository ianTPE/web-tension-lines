---
guide: verify-email-ownership
category: security
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/security/verify-email-ownership.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 驗證電子郵件地址的擁有權

%% line-start id="mwg:verify-email-ownership" %%
## 用 `autocomplete="email-verification-token"` 不寄信就確認信箱擁有權
- 做法：在同一個 `<form>` 裡放 `autocomplete="email"` 的信箱欄位，和帶伺服器端 nonce 的隱藏欄位 `autocomplete="email-verification-token"`；瀏覽器查信箱網域的 DNS 記錄、向信箱供應商取得 Email Verification Token，綁定來源與 nonce 後填入送出；後端驗證成功就跳過一次性驗證碼或魔法連結
- 對手：傳統做法寄一次性驗證碼或魔法連結，使用者得離開頁面、等信、抄碼，造成流失與釣魚風險，信箱供應商還會知道使用者在造訪哪個網站（引用："This forces users to leave your page, wait for email delivery, and copy codes—introducing friction, drop-off, and phishing risk, while also revealing to the email provider which relying party (RP) the user is visiting."）
- 退路：失去主要好處——不支援或信箱網域沒參與時，改回寄一次性驗證碼或魔法連結，使用者一樣要離開頁面抄碼
- 解鎖：以前驗證信箱一定要寄信、等信、抄碼，信箱供應商還看得到你在造訪哪個網站；現在瀏覽器直接出示證明，不寄信也不透露 relying party

經過：註冊時「去收信、把六位數抄回來」是流失最多的一步。瀏覽器本來就登入著信箱，新協定讓它直接替使用者出示證明；不支援的時候，舊流程原封不動地接手。
%% line-end %%

### 細節（不索引）
- 對手組：登入打斷使用者
- 支援狀態：Email Verification API：指南未給 Baseline 資料，只說要啟用 origin trial，並提到 Chrome Origin Trial 版本；記 Limited（僅 Chrome origin trial）
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前驗證信箱一定要切去收信抄碼 → 現在註冊、結帳、訂閱電子報可以在同一頁一次完成，Gmail 這類參與供應商的使用者幾乎零摩擦。目前僅 Chrome origin trial
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:verify-email-ownership:2" %%
## 驗證 nonce 存在伺服器端、只用一次
- 做法：每次渲染表單都在伺服器產生至少 128 位元的 nonce，存在以 `HttpOnly`、`Secure`、`SameSite=Lax` 工作階段 cookie 為鍵的伺服器端狀態；頁面送 `Cache-Control: no-store`；收到 POST 時原子地讀取並刪除 nonce
- 對手：把預期的 nonce 直接放在用戶端 cookie，攻擊者可以把 cookie 和權杖一起重放（引用："never store the expected `nonce` value directly inside a client cookie where an attacker could replay both the cookie and token"）
- 退路：保住主要行為——這是伺服器端流程設計，不受瀏覽器支援度影響；不支援時本來就走舊的驗證流程
- 解鎖：（缺）

經過：權杖綁的是 nonce，如果 nonce 本身也放在用戶端，攻擊者拿到一組就能一再使用。nonce 留在伺服器、用完即刪，重放就失去意義。
%% line-end %%

### 細節（不索引）
- 對手組：確認到錯的身分
- 支援狀態：同 mwg:verify-email-ownership，記 Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:verify-email-ownership:3" %%
## 權杖只在伺服器用現成函式庫驗證，先確認 DNS 委派再信任 `iss`
- 做法：用 `@sd-jwt/core`、`jose` 這類 SD-JWT／JOSE 函式庫解析 `EVT~KB-JWT`；信任 `iss` 前先查 `_email-verification.<domain>` 的 DNS TXT 委派，並確認 `.well-known/email-verification` 回傳的 issuer 相符；驗 EVT 簽章、KB-JWT 的 nonce、aud、時效與演算法允許清單
- 對手：在用戶端 JavaScript 驗證權杖，檢查可以被輕易繞過或偽造，對依賴方沒有任何信任保證（引用："client-side checks can be trivially bypassed or forged and provide zero trust guarantee to the relying party."）
- 退路：保住主要行為——這是伺服器端驗證與 DNS 委派檢查，不涉及瀏覽器功能支援
- 解鎖：（缺）

經過：權杖是一串可以解開來看的 JWT，在前端看一眼「email_verified: true」很容易，但那一眼誰都能偽造。真正的檢查在伺服器：簽章、委派、綁定，一個都不能少。
%% line-end %%

### 細節（不索引）
- 對手組：內容遭竄改未察覺
- 支援狀態：同 mwg:verify-email-ownership，記 Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:verify-email-ownership:4" %%
## EVT 沒有 `kid` 時逐把試驗供應商的金鑰
- 做法：`jwtVerify` 接到 `ERR_JWKS_MULTIPLE_MATCHING_KEYS` 時，用 `for await` 走過錯誤物件給出的每把候選金鑰逐一驗證；KB-JWT 的演算法在過渡期把 `Ed25519` 與 `EdDSA` 視為相同
- 對手：Gmail 等供應商的 EVT 標頭省略 `kid`，JWKS 裡有多把金鑰時 `jose` 直接丟出錯誤（引用："When `kid` is absent and the JWKS contains multiple keys, `jose` throws `ERR_JWKS_MULTIPLE_MATCHING_KEYS`"）
- 退路：保住主要行為——這是伺服器端驗證流程的處理方式，不涉及瀏覽器功能支援
- 解鎖：（缺）

經過：照教科書寫的驗證程式，碰到最大的信箱供應商就全部失敗，因為對方的權杖沒標是哪把鑰匙簽的。
%% line-end %%

### 細節（不索引）
- 對手組：參數或格式用錯就丟例外
- 支援狀態：同 mwg:verify-email-ownership，記 Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 3 個糾錯提醒未拆：信箱比對不分大小寫；擁有權驗證不代表信件送得到，照常寄歡迎信與處理退信；權杖為空或驗證失敗時不要擋下註冊，一律退回傳統驗證
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 對手組由「新功能的副作用」改為「參數或格式用錯就丟例外」
