---
guide: passkeys
category: security
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/security/passkeys.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 通行金鑰總覽

%% line-start id="mwg:passkeys" %%
## RP ID 由伺服器決定並傳給用戶端，不在用戶端從網址推
- 做法：伺服器選項裡的 RP ID 必須等於目前來源的網域，或是它合法的可註冊上層網域，或經 `/.well-known/webauthn` 授權；用戶端（包括呼叫 Signal API 時）一律讀 `publicKey.rp.id`／`publicKey.rpId` 或後端回應
- 對手：RP ID 對不上時用戶端丟出 `SecurityError`；從 `window.location.hostname` 推出來的值對不上上層網域或相關來源的設定（引用："Mismatches result in `SecurityError` exceptions on the client side."）
- 退路：不需要——RP ID 的規則屬 WebAuthn 的既有規範，不涉及新功能支援
- 解鎖：（缺）

經過：通行金鑰綁在 RP ID 上。登入頁在子網域、憑證綁在上層網域，用戶端自己從網址猜，就會猜錯。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：指南未附瀏覽器支援資料，記不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:passkeys:2" %%
## AAGUID 只用來顯示提供者名稱與圖示，不拿來做安全判斷
- 做法：AAGUID 只用於 UX 提示（在管理列表顯示是哪個通行金鑰提供者），不用於任何密碼學安全或存取控制決策
- 對手：平台通行金鑰的 AAGUID 沒有密碼學證明，可以被使用者代理改動或模擬（引用："Platform passkeys do not currently provide cryptographic attestation for their AAGUIDs, meaning it can be altered or simulated by user agents."）
- 退路：不需要——AAGUID 的性質屬既有規範，不涉及新功能支援
- 解鎖：（缺）

經過：看到 AAGUID 是某家硬體金鑰，就想只允許那一家；但這個值可以被假造。它只適合告訴使用者「這把是 iCloud 鑰匙圈的」。
%% line-end %%

### 細節（不索引）
- 對手組：確認到錯的身分
- 支援狀態：指南未附瀏覽器支援資料，記不適用
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 2 個糾錯提醒未拆（WebAuthn 只能在安全環境使用；伺服器端用審核過的函式庫、用戶端直接呼叫原生 API 而不用函式庫包裝）
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
