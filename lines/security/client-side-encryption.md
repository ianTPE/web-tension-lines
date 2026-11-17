---
guide: client-side-encryption
category: security
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/security/client-side-encryption.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 用 WebCrypto 在用戶端加密資料

%% line-start id="mwg:client-side-encryption" %%
## 用 `encapsulateKey()`（MLKEM768-X25519）加 AEAD 在瀏覽器裡做抗量子的信封加密
- 做法：收件方用 `crypto.subtle.generateKey('MLKEM768-X25519', false, …)` 產生不可匯出的金鑰對並存進 IndexedDB、以 `'raw-public'` 匯出公鑰；寄件方對每則訊息呼叫 `encapsulateKey()` 取得一次性共享金鑰與密文膠囊，再用 `ChaCha20-Poly1305` 或 `AES-GCM` 加密，送出 `{ capsule, iv, ciphertext }`
- 對手：指南只說混合式 KEM 讓共享秘密在任一演算法成立時都保持安全，沒說只用古典金鑰交換在哪個時刻出問題（引用："it combines post-quantum ML-KEM (standardized in NIST FIPS 203) with classical `'X25519'` so the shared secret remains secure as long as either algorithm holds."）
- 退路：失去主要好處——退回 `X25519`＋`HKDF`＋`AES-GCM` 的古典金鑰交換，瀏覽器裡加密仍在，但失去抗量子這一段
- 解鎖：以前端對端加密要自己載密碼學函式庫、私鑰也得自己保管；現在 WebCrypto 能在瀏覽器裡做抗量子的信封加密，私鑰以不可匯出的 `CryptoKey` 留在本機

經過：在瀏覽器裡做端對端加密，不必再載入密碼學函式庫，私鑰也不必離開 `CryptoKey` 物件。新演算法尚未普及的瀏覽器，同一套介面退回古典金鑰交換。
%% line-end %%

### 細節（不索引）
- 對手組：敏感資料外露
- 支援狀態：Web Cryptography：Widely available（2017-09-19）；X25519 deriveBits：Newly available（2025-02-06）。指南沒附 ML-KEM／`encapsulateKey()` 的支援資料，取所列最低者記 Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：日記或筆記 app 可以在瀏覽器裡把每篇內容加密後才上傳，伺服器只存密文，私鑰是不可匯出的 `CryptoKey`，不必內附任何加密函式庫。新演算法不支援時退回古典交換
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:client-side-encryption:2" %%
## 用 AEAD 的 `additionalData` 把未加密的中繼資料綁進驗證標籤
- 做法：加密時把紀錄 ID、收件者 ID、協定版本等不加密的中繼資料放進 `additionalData`；每次加密都用新的 12 位元組隨機 IV，不重用 `(iv, key)` 組合
- 對手：未綁定時，竄改密文旁邊的中繼資料不會被發現（引用："Bind unencrypted metadata (such as a record ID, recipient ID, or protocol version) to the authentication tag via `additionalData` so tampering with either the ciphertext or the metadata causes `decrypt()` to reject with `OperationError`."）
- 退路：不需要——`additionalData` 隨 WebCrypto 已 Widely，不必退路
- 解鎖：（缺）

經過：密文本身有驗證，但「這是給誰的、第幾筆」寫在旁邊，攻擊者可以把密文搬到別的紀錄底下。把中繼資料一起綁進標籤，搬動就解不開。
%% line-end %%

### 細節（不索引）
- 對手組：內容遭竄改未察覺
- 支援狀態：Web Cryptography（AES-GCM）：Widely available（2017-09-19）
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:client-side-encryption:3" %%
## 新演算法不收 `'raw'`：明確寫 `'raw-public'`／`'raw-seed'`／`'raw-secret'`
- 做法：`MLKEM768-X25519`、`ML-KEM-*`、`ChaCha20-Poly1305` 的 `importKey()`／`exportKey()` 一律指定明確格式；匯入 KEM 私鑰只給 `['decapsulateKey']`；演算法名稱只用指南列出的三種
- 對手：沿用舊的 `'raw'` 格式，新演算法直接丟出 `NotSupportedError`（引用："Modern WebCrypto algorithms (…) **reject the legacy `'raw'` format** in `importKey()` and `exportKey()` with a `NotSupportedError`."）
- 退路：保住主要行為——舊瀏覽器本來就只認 `'raw'`，退回舊格式時反而正確
- 解鎖：（缺）

經過：照舊習慣寫 `'raw'`，在新演算法上整段流程第一步就失敗。新舊兩條路徑的格式名稱不同，要分開寫。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：同 mwg:client-side-encryption，記 Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:client-side-encryption:4" %%
## `SubtleCrypto.supports()` 要在建構子上呼叫，不是 `crypto.subtle`
- 做法：用 `globalThis.SubtleCrypto?.supports?.('encapsulateKey', 'MLKEM768-X25519', 'ChaCha20-Poly1305')` 偵測；探測 `'encrypt'`／`'decrypt'` 時要帶 `iv`
- 對手：在 `crypto.subtle` 上找 `supports`，拿到的是 `undefined`（引用："`globalThis.SubtleCrypto?.supports?.(…)` is a synchronous static method returning a boolean (`crypto.subtle.supports` is `undefined`)."）
- 退路：保住主要行為——偵測不到 `supports()` 時就直接走古典路徑，功能偵測仍然有效
- 解鎖：以前沒有同步的方法知道瀏覽器支不支援某個演算法，只能送出後用例外判斷；現在有靜態的 `SubtleCrypto.supports()` 直接回傳布林值

經過：偵測寫在錯的物件上，永遠判定不支援，支援的瀏覽器也被送去走古典路徑。
%% line-end %%

### 細節（不索引）
- 對手組：功能偵測不可靠
- 支援狀態：同 mwg:client-side-encryption，記 Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
