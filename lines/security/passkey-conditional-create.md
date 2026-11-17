---
guide: passkey-conditional-create
category: security
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/security/passkey-conditional-create.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 通行金鑰條件式建立（登入後推廣）

%% line-start id="mwg:passkey-conditional-create" %%
## 密碼登入成功後用 `mediation: 'conditional'` 默默建立通行金鑰
- 做法：只在含密碼、所有驗證因素都通過的完整登入之後，先 `abort()` 自動填入的條件式 `get()`，確認 `capabilities.conditionalCreate`，再以 `mediation: 'conditional'` 呼叫 `navigator.credentials.create()`（`excludeCredentials` 填入既有憑證）；`InvalidStateError`、`NotAllowedError`、`AbortError` 一律靜默吞掉；伺服器只對這類請求放寬使用者在場（UP）檢查
- 對手：一般的建立流程會跳出顯眼的模態對話框打斷使用者（引用："This signals the browser to handle the passkey creation flow silently in the background or contextually without throwing obtrusive modal dialogs."）
- 退路：失去主要好處——不支援條件式建立時整段流程直接略過，使用者不會自動多出通行金鑰
- 解鎖：以前要推廣通行金鑰只能跳一個大對話框打斷使用者；現在能在密碼登入後默默建立，下次就多一個通行金鑰選項

經過：使用者剛用密碼登入，再跳一個「要不要建立通行金鑰」的大對話框，多半被關掉。改成條件式建立，瀏覽器在不打擾的情況下替他存好，下次就能用通行金鑰登入。
%% line-end %%

### 細節（不索引）
- 對手組：登入打斷使用者
- 支援狀態：getClientCapabilities()：Newly available（2025-02-06）；parseCreationOptionsFromJSON()：Newly available（2025-03-31）。指南沒附 conditional create 本身的支援資料，記 Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：既有的密碼登入網站不必做「升級到通行金鑰」的引導頁，使用者照常登入，下次就自動多了一個通行金鑰選項
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:passkey-conditional-create:2" %%
## 伺服器驗證失敗時用 `signalUnknownCredential()` 清掉孤兒憑證
- 做法：`create()` 成功但伺服器驗證回應不 OK 或網路失敗時，呼叫 `PublicKeyCredential.signalUnknownCredential({ rpId: publicKey.rp.id, credentialId: encodedResponse.id })`；伺服器選項必須帶 `rp.id`
- 對手：伺服器沒收下的憑證留在通行金鑰提供者裡成為孤兒（引用："invoke `PublicKeyCredential.signalUnknownCredential(…)` to prevent orphaned credentials from lingering in the passkey provider."）
- 退路：失去主要好處——Firefox 不支援 Signal API，孤兒憑證清不掉，會留在通行金鑰提供者裡
- 解鎖：以前註冊失敗的憑證會變成孤兒留在提供者裡；現在伺服器驗證失敗當下就能通知提供者清掉

經過：瀏覽器那邊已經建好通行金鑰，伺服器卻驗證失敗沒存，使用者之後會看到一個永遠登不進去的選項。驗證失敗當下就通知提供者。
%% line-end %%

### 細節（不索引）
- 對手組：憑證狀態錯亂
- 支援狀態：Web authentication signal methods：Limited availability。Supported by: Chrome 132, Edge 132, Safari 26。Unsupported in: Firefox
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：同 mwg:passkey-authentication:3：註冊流程失敗不會在使用者的密碼管理器裡留下壞掉的通行金鑰。Firefox 不支援
- 另有 2 個糾錯提醒未拆（只在含密碼的完整登入後觸發、伺服器只對條件式建立放寬 UP 檢查；rpId 取自 `publicKey.rp.id`，見 mwg:passkeys）
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
