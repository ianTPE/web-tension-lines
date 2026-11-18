---
guide: sanitize-untrusted-html
category: security
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/security/sanitize-untrusted-html.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 清理不可信的 HTML

%% line-start id="mwg:sanitize-untrusted-html" %%
## 用原生 `setHTML()` 一步完成解析、清理與插入
- 做法：使用者產生的 HTML 用 `element.setHTML(html)` 插入（預設清理器移除腳本、事件處理器與白名單外的元素和屬性）；需要更嚴時傳 `new Sanitizer({ elements, attributes, replaceWithChildrenElements })`；不插入只解析時用 `Document.parseHTML()`；不支援時才動態載入 DOMPurify
- 對手：使用者產生的 HTML 裡的 `<script>` 標籤與 `on*` 屬性，在進入 DOM 時就會執行（引用："The native **Sanitizer API** provides a built-in, browser-optimized way to strip dangerous content (like `<script>` tags or `on*` attributes) before it reaches the DOM."）
- 退路：保住主要行為——Safari 沒有原生 API 時才動態載入 DOMPurify，內容照樣清乾淨才進 DOM
- 解鎖：以前顯示使用者的 HTML 一定要帶一個清理函式庫；現在瀏覽器自己會清，而且不能被設定成放行 XSS

經過：顯示留言或 Markdown 預覽，以前一定要帶一個清理函式庫。現在瀏覽器自己會清，而且不能被設定成放行 XSS；Safari 還得備著函式庫。
%% line-end %%

### 細節（不索引）
- 對手組：不可信內容當HTML解析
- 支援狀態：Sanitizer API：Limited availability。Supported by: Chrome 146, Edge 146, Firefox 148。Unsupported in: Safari
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：留言區、Markdown 筆記預覽、Email 內容檢視可以直接 `setHTML()` 使用者的 HTML，支援的瀏覽器不必下載清理函式庫；也能用 `parseHTML()` 先產生乾淨的預覽再決定要不要插入。Safari 仍需 DOMPurify
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:sanitize-untrusted-html:2" %%
## 清理後直接搬節點，不要序列化成字串再塞回 `innerHTML`
- 做法：`Document.parseHTML()` 的結果用 `replaceChildren(...doc.body.childNodes)` 搬進頁面
- 對手：把清理過的節點序列化成字串、再用 `innerHTML` 重新解析，可能重新引入突變型 XSS（引用："Move the resulting nodes into the page rather than serializing them to a string and re-parsing it with `innerHTML`, which can reintroduce mutation XSS (mXSS)."）
- 退路：保住主要行為——退路用 DOMPurify 清理後同樣把節點搬進頁面，不序列化就不會有二次解析的風險
- 解鎖：（缺）

經過：清乾淨的內容轉回字串再解析一次，瀏覽器可能把它解析成不一樣的結構，攻擊就從這個縫鑽進來。
%% line-end %%

### 細節（不索引）
- 對手組：不可信內容當HTML解析
- 支援狀態：同 mwg:sanitize-untrusted-html，記 Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:sanitize-untrusted-html:3" %%
## 自訂清理器會連內容一起刪，DOMPurify 退路的預設又不一樣
- 做法：想保留文字的外層元素列進 `replaceWithChildrenElements`；DOMPurify 退路設 `ALLOW_ARIA_ATTR: false`、`ALLOW_DATA_ATTR: false`、`KEEP_CONTENT: false` 並允許 `#text`；需要對齊退路的設定不用 `replaceWithChildrenElements`
- 對手：不在 `elements` 裡的元素連同內容一起被刪；DOMPurify 預設卻保留 `aria-*`、`data-*` 與被刪元素的文字，兩條路徑輸出不一致（引用："Elements that are not in `elements` are removed **together with their content**."）
- 退路：保住主要行為——退回 DOMPurify 時用 `ALLOW_ARIA_ATTR: false` 等設定對齊輸出，兩邊結果一致
- 解鎖：（缺）

經過：只允許幾個行內標籤，結果整段包在 `<div>` 裡的文字全不見了；換到 Safari 的 DOMPurify 退路，又多出一堆屬性。兩邊要刻意對齊。
%% line-end %%

### 細節（不索引）
- 對手組：新屬性的隱藏前提
- 支援狀態：同 mwg:sanitize-untrusted-html，記 Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 對手組由「新功能的副作用」改為「新屬性的隱藏前提」

%% line-start id="mwg:sanitize-untrusted-html:4" %%
## 強制 Trusted Types 時，DOMPurify 退路要回傳 TrustedHTML
- 做法：退路呼叫 `DOMPurify.sanitize()` 時傳 `RETURN_TRUSTED_TYPE: true`，並在 `trusted-types` CSP 指令允許 `dompurify` 政策名稱
- 對手：頁面強制 Trusted Types 時，把字串指派給 `innerHTML` 會丟出例外（引用："If the page enforces Trusted Types (`require-trusted-types-for 'script'`), assigning a string to `innerHTML` throws."）
- 退路：保住主要行為——退路傳 `RETURN_TRUSTED_TYPE: true` 並在 CSP 放行 `dompurify` 政策名稱，就不會被自家政策擋下
- 解鎖：（缺）

經過：原生路徑在 Trusted Types 下暢通無阻，退路卻因為塞字串而被自家的安全政策擋下。
%% line-end %%

### 細節（不索引）
- 對手組：參數或格式用錯就丟例外
- 支援狀態：同 mwg:sanitize-untrusted-html，記 Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 1 個糾錯提醒未拆（同一份內容在其他地方渲染時，伺服器端也要清理，且規則不能互相衝突）
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 對手組由「新功能的副作用」改為「參數或格式用錯就丟例外」
