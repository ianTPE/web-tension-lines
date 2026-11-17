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
- 做法：`crypto.subtle.generateKey('ML-DSA-65', false, ['sign', 'verify'])` 產生金鑰對，以 `'raw-public'` 匯出公鑰給驗證方，`sign()`／`verify()` 處理訊息、權杖或發布檔清單；不支援時退回 `'Ed25519'`（或 `'ECDSA'` P-256）
- 對手：指南只說數位簽章保證資料完整性與簽署者真實性、而且不需要共用秘密金鑰，沒說其他做法在哪個時刻出問題（引用："Digital signatures guarantee data integrity and signer authenticity without requiring shared secret keys."）
- 退路：保住主要行為——退回 `'Ed25519'`（或 `'ECDSA'`），瀏覽器裡簽章驗證照常，只是沒有抗量子強度
- 解鎖：以前要在瀏覽器裡簽章得帶密碼學函式庫或交給伺服器；現在 `crypto.subtle` 就能簽章與驗證，還有抗量子選項

經過：要在瀏覽器裡確認一份清單沒被改過、確實出自某人，以前得帶密碼學函式庫或交給伺服器。現在 `crypto.subtle` 直接做，還有抗量子選項。
%% line-end %%

### 細節（不索引）
- 對手組：內容遭竄改未察覺
- 支援狀態：Web Cryptography：Widely available（2017-09-19）；Ed25519 sign：Newly available（2025-05-29）。指南沒附 ML-DSA 的支援資料，取所列最低者記 Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：靜態網站可以附一份簽過名的發布清單，訪客的瀏覽器下載檔案後自己驗簽，不必信任中間的 CDN；匯出的筆記也能附簽章證明沒被改過
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:digital-signatures:2" %%
## 用 `context` 做領域分離，讓一個用途的簽章不能拿去別處重放
- 做法：`sign()`／`verify()` 傳 `{ name: 'ML-DSA-65', context }`（0～255 位元組，雙方必須完全相同）；退回 Ed25519／ECDSA 時，自己在資料前加上帶長度前綴的 context 標頭
- 對手：共用同一組金鑰時，為某個用途產生的簽章可以被拿到應用程式的其他部分重放；古典演算法還會默默忽略 `context` 屬性（引用："To prevent a signature created for one purpose from being replayed in another part of your application or protocol that shares the same key pair, bind the signature to a domain-separation `context`."）
- 退路：保住主要行為——退回古典演算法時自己加帶長度前綴的 `context` 標頭，領域分隔照常有效
- 解鎖：以前簽章不帶用途標籤，同一把鑰簽的東西可以互相冒用；現在能用 `context` 把簽章綁在特定用途上

經過：同一把金鑰簽登入挑戰也簽發布清單，攻擊者可能把一種簽章挪去冒充另一種。綁上用途標籤，簽章就只在原本的用途裡有效；退回古典演算法時這個標籤會被靜默丟掉，要手動補。
%% line-end %%

### 細節（不索引）
- 對手組：內容遭竄改未察覺
- 支援狀態：同 mwg:digital-signatures，記 Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：一個瀏覽器端身分金鑰可以同時用來簽「登入挑戰」「留言」「檔案清單」，各用途的簽章互相不能冒用，不必為每個用途各管一把鑰匙
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:digital-signatures:3" %%
## ML-DSA 不收 `'raw'`：公鑰用 `'raw-public'`、私鑰用 `'raw-seed'`
- 做法：ML-DSA 的匯入匯出指定 `'raw-public'`、`'raw-seed'`、`'spki'`、`'pkcs8'` 或 `'jwk'`；匯入公鑰只給 `['verify']`、私鑰只給 `['sign']`；不用 `'Dilithium'` 這類標準化前的名稱
- 對手：沿用舊的 `'raw'` 格式，ML-DSA 直接丟出 `NotSupportedError`（引用："`'ML-DSA-44'`, `'ML-DSA-65'`, and `'ML-DSA-87'` **reject the legacy `'raw'` format** in `importKey()` and `exportKey()` with a `NotSupportedError`."）
- 退路：保住主要行為——舊瀏覽器本來就只認 `'raw'`，退回舊格式時反而正確
- 解鎖：（缺）

經過：與 mwg:client-side-encryption:3 同一個坑：新演算法改了格式名稱，照舊寫就在第一步失敗。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：同 mwg:digital-signatures，記 Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:digital-signatures:4" %%
## `SubtleCrypto.supports()` 要在建構子上呼叫，不是 `crypto.subtle`
- 做法：用 `globalThis.SubtleCrypto?.supports?.('sign', 'ML-DSA-65')` 偵測，決定走 ML-DSA 或 Ed25519
- 對手：在 `crypto.subtle` 上找 `supports`，拿到的是 `undefined`（引用："`globalThis.SubtleCrypto?.supports?.('sign', 'ML-DSA-65')` is a synchronous static method returning a boolean (`crypto.subtle.supports` is `undefined`)."）
- 退路：保住主要行為——偵測不到 `supports()` 時就直接走古典路徑，功能偵測仍然有效
- 解鎖：以前沒有同步的方法知道瀏覽器支不支援某個簽章演算法，只能送出後用例外判斷；現在有靜態的 `SubtleCrypto.supports()` 直接回傳布林值

經過：與 mwg:client-side-encryption:4 相同：偵測寫在錯的物件上，就永遠走退路。
%% line-end %%

### 細節（不索引）
- 對手組：功能偵測不可靠
- 支援狀態：同 mwg:digital-signatures，記 Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
