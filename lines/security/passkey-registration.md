---
guide: passkey-registration
category: security
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/security/passkey-registration.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 通行金鑰註冊

%% line-start id="mwg:passkey-registration" %%
## 用 `excludeCredentials` 擋掉同一提供者上的重複通行金鑰
- 做法：產生建立選項時把使用者既有的憑證 ID（含 `transports`）放進 `excludeCredentials`；用戶端把 `InvalidStateError` 當成「已有通行金鑰」並告知使用者
- 對手：沒有排除清單時，同一個通行金鑰提供者帳戶上會註冊出重複的憑證（引用："This prevents the authenticator from registering duplicate credentials on the same passkey provider account."）
- 退路：保住主要行為——排除清單是伺服器端選項的內容，瀏覽器缺新的 JSON 序列化時載 polyfill 即可，重複防護照常
- 解鎖：（缺）

經過：使用者在設定頁多按了一次「建立通行金鑰」，提供者裡就多一筆一模一樣的。把既有的列進排除清單，瀏覽器會直接說已經有了。
%% line-end %%

### 細節（不索引）
- 對手組：憑證狀態錯亂
- 支援狀態：parseCreationOptionsFromJSON()：Newly available（2025-03-31）。記 Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:passkey-registration:2" %%
## `userVerification: "preferred"` 時，伺服器驗證要設 `requireUserVerification: false`
- 做法：建立選項用 `"preferred"` 時，伺服器端驗證函式庫設 `requireUserVerification: false`；但仍要求使用者在場（UP）旗標為 `true`
- 對手：選項說「偏好」驗證、伺服器卻「要求」驗證，沒開螢幕鎖的驗證器註冊時會被誤判失敗（引用："Otherwise, authenticators that register without user verification (e.g., screen locks disabled) will trigger spurious server verification failures."）
- 退路：保住主要行為——這是伺服器端驗證參數的對應，不涉及瀏覽器功能支援
- 解鎖：（缺）

經過：瀏覽器照「偏好」完成註冊，伺服器照「必須」驗證，兩邊說的不是同一件事，使用者看到莫名其妙的失敗。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：同上，記 Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 3 個糾錯提醒未拆（伺服器驗證失敗時呼叫 `signalUnknownCredential()`，同 mwg:passkey-conditional-create:2；rpId 取自 `publicKey.rp.id`，見 mwg:passkeys；推廣流程設 `authenticatorAttachment: "platform"`、管理頁省略）
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
