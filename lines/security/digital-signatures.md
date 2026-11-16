---
guide: digital-signatures
category: security
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/security/digital-signatures.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 用 WebCrypto 簽章與驗證

%% line-start id="mwg:digital-signatures" %%
## 用 ML-DSA 在瀏覽器裡簽章與驗證，不必共用秘密金鑰
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`crypto.subtle.generateKey('ML-DSA-65', false, ['sign', 'verify'])` 產生金鑰對，以 `'raw-public'` 匯出公鑰給驗證方，`sign()`／`verify()` 處理訊息、權杖或發布檔清單；不支援時退回 `'Ed25519'`（或 `'ECDSA'` P-256）
- 被什麼擋：指南只說數位簽章保證資料完整性與簽署者真實性、而且不需要共用秘密金鑰，沒說其他做法在哪個時刻出問題（引用："Digital signatures guarantee data integrity and signer authenticity without requiring shared secret keys."）
- 戰報：部分改善——支援的瀏覽器用抗量子的 ML-DSA 簽章；不支援時退回古典的 Ed25519（官方宣稱）

經過：要在瀏覽器裡確認一份清單沒被改過、確實出自某人，以前得帶密碼學函式庫或交給伺服器。現在 `crypto.subtle` 直接做，還有抗量子選項。
%% line-end %%

### 細節（不索引）
- 對手組：內容遭竄改未察覺
- 支援狀態：Web Cryptography：Widely available（2017-09-19）；Ed25519 sign：Newly available（2025-05-29）。指南沒附 ML-DSA 的支援資料，取所列最低者記 Newly
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：靜態網站可以附一份簽過名的發布清單，訪客的瀏覽器下載檔案後自己驗簽，不必信任中間的 CDN；匯出的筆記也能附簽章證明沒被改過
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:digital-signatures:2" %%
## 用 `context` 做領域分離，讓一個用途的簽章不能拿去別處重放
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：`sign()`／`verify()` 傳 `{ name: 'ML-DSA-65', context }`（0～255 位元組，雙方必須完全相同）；退回 Ed25519／ECDSA 時，自己在資料前加上帶長度前綴的 context 標頭
- 被什麼擋：共用同一組金鑰時，為某個用途產生的簽章可以被拿到應用程式的其他部分重放；古典演算法還會默默忽略 `context` 屬性（引用："To prevent a signature created for one purpose from being replayed in another part of your application or protocol that shares the same key pair, bind the signature to a domain-separation `context`."）
- 戰報：部分改善——ML-DSA 原生綁定 context，換個 context 驗證就不通過；古典路徑要自己加前綴才有同樣效果（官方宣稱）

經過：同一把金鑰簽登入挑戰也簽發布清單，攻擊者可能把一種簽章挪去冒充另一種。綁上用途標籤，簽章就只在原本的用途裡有效；退回古典演算法時這個標籤會被靜默丟掉，要手動補。
%% line-end %%

### 細節（不索引）
- 對手組：內容遭竄改未察覺
- 支援狀態：同 mwg:digital-signatures，記 Newly
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：新能力
- 解鎖（發想，非指南原文）：一個瀏覽器端身分金鑰可以同時用來簽「登入挑戰」「留言」「檔案清單」，各用途的簽章互相不能冒用，不必為每個用途各管一把鑰匙
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:digital-signatures:3" %%
## ML-DSA 不收 `'raw'`：公鑰用 `'raw-public'`、私鑰用 `'raw-seed'`
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：ML-DSA 的匯入匯出指定 `'raw-public'`、`'raw-seed'`、`'spki'`、`'pkcs8'` 或 `'jwk'`；匯入公鑰只給 `['verify']`、私鑰只給 `['sign']`；不用 `'Dilithium'` 這類標準化前的名稱
- 被什麼擋：沿用舊的 `'raw'` 格式，ML-DSA 直接丟出 `NotSupportedError`（引用："`'ML-DSA-44'`, `'ML-DSA-65'`, and `'ML-DSA-87'` **reject the legacy `'raw'` format** in `importKey()` and `exportKey()` with a `NotSupportedError`."）
- 戰報：部分改善——改用明確格式後匯入匯出正常；退回 Ed25519 的路徑仍用 `'raw'`（官方宣稱）

經過：與 mwg:client-side-encryption:3 同一個坑：新演算法改了格式名稱，照舊寫就在第一步失敗。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：同 mwg:digital-signatures，記 Newly
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:digital-signatures:4" %%
## `SubtleCrypto.supports()` 要在建構子上呼叫，不是 `crypto.subtle`
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：用 `globalThis.SubtleCrypto?.supports?.('sign', 'ML-DSA-65')` 偵測，決定走 ML-DSA 或 Ed25519
- 被什麼擋：在 `crypto.subtle` 上找 `supports`，拿到的是 `undefined`（引用："`globalThis.SubtleCrypto?.supports?.('sign', 'ML-DSA-65')` is a synchronous static method returning a boolean (`crypto.subtle.supports` is `undefined`)."）
- 戰報：部分改善——在正確的物件上偵測，才能正確分流（官方宣稱）

經過：與 mwg:client-side-encryption:4 相同：偵測寫在錯的物件上，就永遠走退路。
%% line-end %%

### 細節（不索引）
- 對手組：功能偵測不可靠
- 支援狀態：同 mwg:digital-signatures，記 Newly
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出
