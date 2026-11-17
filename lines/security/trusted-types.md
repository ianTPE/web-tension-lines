---
guide: trusted-types
category: security
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/security/trusted-types.md
first_seen: 2026-11-17（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 用 Trusted Types 防止 DOM 型 XSS

%% line-start id="mwg:trusted-types" %%
## 用 Trusted Types 讓危險 sink 只收政策產生的物件
- 做法：用 `trustedTypes.createPolicy()` 定義清理政策（交給 DOMPurify 或應用程式的跳脫規則），寫入 `innerHTML`、`document.write()`、`<script src>`、`Worker()` 等 sink 前先轉成 `TrustedHTML`／`TrustedScriptURL`；以 CSP `require-trusted-types-for 'script'` 強制，`trusted-types` 指令限定可建立的政策名稱
- 對手：這些 DOM API 預設接受原始字串，字串裡若有來自不可信來源的惡意腳本就會被執行（引用："If a string contains malicious script from an untrusted source, it can be executed."）
- 退路：失去主要好處——舊瀏覽器只能靠 tinyfill 讓程式不壞，sink 仍接受原始字串，瀏覽器不再替你擋漏網的寫入
- 解鎖：以前要靠 grep 與 code review 保證沒有原始字串進 `innerHTML`；現在危險 sink 只收政策產生的物件，漏網的寫入直接丟錯

經過：要求大家別用 `innerHTML` 是一回事，保證程式碼裡沒有任何一條路徑把原始字串塞進去是另一回事。Trusted Types 把後者交給瀏覽器：漏網的寫入直接丟錯。
%% line-end %%

### 細節（不索引）
- 對手組：不可信內容當HTML解析
- 支援狀態：Trusted Types：Newly available（2026-02-24）。Supported by: Chrome 83, Edge 83, Firefox 148, Safari 26
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：以前只能靠 code review 與 grep 確認沒有 `innerHTML` 漏網 → 現在留言區、Markdown 預覽、CMS 編輯器這類會插 HTML 的頁面可以在四大瀏覽器上讓瀏覽器擔保：任何沒經過清理政策的寫入都會丟錯並回報
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:trusted-types:2" %%
## 先 Report-Only 收違規，歸零再強制 Trusted Types
- 做法：先確認框架與第三方函式庫會產生 `TrustedHTML`／`TrustedScript`；先送 `Content-Security-Policy-Report-Only: require-trusted-types-for 'script'`，必要時註冊暫時的 `default` 政策，在 `createHTML` 裡記錄仍在傳字串的位置；違規報告歸零後才換成強制的 `Content-Security-Policy`
- 對手：還有 sink 寫入沒改完，或框架、第三方函式庫不產生 Trusted Type 時就直接強制，應用程式會壞（引用："it carries a risk of site breakage if every sink write hasn't been migrated."）
- 退路：保住主要行為——先送 Report-Only 觀察再強制，這個流程在支援的瀏覽器照走，不支援的瀏覽器本來也沒有強制模式
- 解鎖：（缺）

經過：Trusted Types 的保護力來自「一律丟錯」，同一個特性也讓它一開就可能把網站打掛。先觀察、再修、最後才開強制。
%% line-end %%

### 細節（不索引）
- 對手組：合法連線被安全規則擋下
- 支援狀態：同 mwg:trusted-types，記 Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:trusted-types:3" %%
## 字元跳脫不是 HTML 清理器
- 做法：只需要純文字時用 `element.textContent`（它不是 Trusted Types sink）；要接受標記或屬性時用完整的清理器（DOMPurify 或 `element.setHTML()`）；不把跳脫政策 `escapePolicy.createHTML()` 的輸出再插進另一個 HTML 樣板
- 對手：把字元層級跳脫後的字串插進沒加引號的屬性或 `href` 這類網址屬性，`javascript:` 網址不會被實體跳脫中和（引用："a URL attribute (`<a href="${escaped}">`, where `javascript:` URLs are not neutralized by entity escaping)"）
- 退路：保住主要行為——不支援 Trusted Types 的瀏覽器本來就沒有跳脫政策，改用 `textContent` 或完整清理器一樣安全
- 解鎖：（缺）

經過：跳脫政策讓 Trusted Types 不再報錯，看起來就像通過了檢查。可是 `&lt;` 救不了 `javascript:alert(1)`：它本來就沒有角括號。
%% line-end %%

### 細節（不索引）
- 對手組：防線形同虛設
- 支援狀態：同 mwg:trusted-types，記 Newly
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-17（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
