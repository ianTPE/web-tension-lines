---
guide: passkey-reauthentication
category: security
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/security/passkey-reauthentication.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 通行金鑰重新驗證

%% line-start id="mwg:passkey-reauthentication" %%
## 重新驗證時把 `allowCredentials` 限定為目前使用者的憑證，伺服器再核對擁有者
- 做法：敏感操作（改密碼、轉帳）前的重新驗證，伺服器在 `allowCredentials` 填入已登入使用者的所有憑證 ID（含 `transports`）；驗證端點確認回傳的憑證屬於目前使用者（`storedCredential.passkeyUserId === req.user.id`），不是就拒絕
- 對手：`allowCredentials` 留空或省略會退回可發現憑證，違反工作階段安全；回傳的可能是另一個使用者的有效通行金鑰（引用："Leaving this empty or omitting it regresses to discoverable credentials, violating session safety."）
- 退路：保住主要行為——這是伺服器端選項與驗證的流程設計，`allowCredentials` 與擁有者核對不受瀏覽器支援度影響
- 解鎖：（缺）

經過：已登入的使用者要轉帳，跳出的通行金鑰選單卻列出裝置上所有帳號，選錯了也可能通過。限定清單、再在伺服器核對擁有者，確認的才是同一個人。
%% line-end %%

### 細節（不索引）
- 對手組：確認到錯的身分
- 支援狀態：getClientCapabilities()：Newly available（2025-02-06）；parseRequestOptionsFromJSON()：Newly available（2025-03-31）。記 Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 2 個糾錯提醒未拆（404 時呼叫 `signalUnknownCredential()`，同 mwg:passkey-authentication:3；rpId 取自伺服器選項，見 mwg:passkeys）
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
