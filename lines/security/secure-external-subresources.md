---
guide: secure-external-subresources
category: security
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/security/secure-external-subresources.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 用 SRI、CORS 與 Referrer Policy 保護外部子資源

%% line-start id="mwg:secure-external-subresources" %%
## 外部腳本與樣式表加 `integrity`，並釘在不可變的版本網址
- 做法：在建置或發布時從已知正確的本機檔案算出 `sha384-` 摘要，寫進 `<script>`、`<link rel="stylesheet|preload|modulepreload">` 與 `fetch()` 的 `integrity`；外部資源用帶版本或內容定址的網址；同一網址可能回傳多種合法內容時列出多個摘要；會原地更新的第三方腳本不加 `integrity`，改用 CSP 或 iframe 沙箱
- 對手：引用 `latest/` 這類會變動的網址，網站暴露在無聲的供應鏈變更下；在瀏覽器執行時抓遠端檔案自己算雜湊，等於相信遠端給的任何內容（引用："rather than mutable floating URLs (`latest/app.min.js`), which expose your site to silent supply-chain changes and break SRI as soon as the remote file updates."）
- 退路：不需要——`integrity` 與 `referrerpolicy` 在 `<link>`／`<script>` 上早已 Widely，不必退路
- 解鎖：以前只能信任 CDN 網址上的內容有沒有被換掉；現在可以在建置時算好雜湊寫進標記，內容一變就被擋下

經過：CDN 上的檔案被換掉，網站照樣載入執行。釘住版本、寫上雜湊，內容一變就被擋下。
%% line-end %%

### 細節（不索引）
- 對手組：內容遭竄改未察覺
- 支援狀態：指南寫 `<link rel="stylesheet">` 的 subresource-integrity 與 referrer-policy "widely available across all browsers"，記 Widely
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:secure-external-subresources:2" %%
## 有 `integrity` 就一定要有 `crossorigin`，否則資源直接被擋
- 做法：跨來源資源設 `integrity` 時同時設 `crossorigin="anonymous"`（或 `use-credentials`），並確認伺服器回 CORS 標頭
- 對手：少了 `crossorigin`，瀏覽器以 `no-cors` 模式抓取，拿到無法驗證雜湊的不透明回應，於是擋下資源（引用："Omitting `crossorigin` causes the browser to fetch the resource in `no-cors` mode (producing an opaque response that cannot be hash-verified) and block the resource."）
- 退路：不需要——`crossorigin` 是既有 HTML 屬性，不涉及瀏覽器功能支援
- 解鎖：（缺）

經過：加了完整性檢查，結果檔案根本載不進來，因為瀏覽器看不到內容就無從比對。
%% line-end %%

### 細節（不索引）
- 對手組：合法連線被安全規則擋下
- 支援狀態：同 mwg:secure-external-subresources，記 Widely
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:secure-external-subresources:3" %%
## 用 CSS `url()` 的 `integrity()`／`cross-origin()`／`referrer-policy()` 驗證樣式表裡載的資源
- 做法：`@import`、`@font-face src`、`background-image`、`mask-image` 等的 `url("…")` 內加 `cross-origin(anonymous) referrer-policy(no-referrer) integrity("sha384-…")`；網址要加引號、每種修飾子只寫一次
- 對手：`background-image`、`content`、`border-image-source`、`@import` 預設用 `no-cors` 抓取，拿到的不透明回應無法驗證雜湊（引用："`background-image`, `content`, `border-image-source`, and `@import` default to `no-cors` mode (producing an opaque response that cannot be hash-verified)"）
- 退路：失去主要好處——退回 `<link>` 與文件層政策時，樣式表本身還能驗雜湊，但 CSS 裡的字型與圖片驗不了
- 解鎖：以前 CSS 裡的 `@import`、字型與背景圖只能以 no-cors 抓取，無法驗雜湊；現在可在 `url()` 裡直接寫雜湊與跨來源模式

經過：HTML 裡的腳本都加了 SRI，樣式表裡從 CDN 拉的字型和 `@import` 卻沒辦法驗。現在可以在 `url()` 裡寫雜湊，只是目前只有 Chromium 會檢查。
%% line-end %%

### 細節（不索引）
- 對手組：內容遭竄改未察覺
- 支援狀態：cross-origin() for url()：Limited availability（Chrome 150, Edge 150, Safari 26.2；不支援 Firefox）；referrer-policy() for url()：同上；integrity() for url()：Limited availability（Chrome 150, Edge 150；不支援 Firefox、Safari）
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：從 CDN 發布的設計系統可以在 CSS 裡把字型、圖示雪碧圖、主題變數檔全部釘上雜湊，不必為了 SRI 把 `@import` 拆成一堆 `<link>`。目前只有 Chromium 會驗
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:secure-external-subresources:4" %%
## `@font-face` 的 `src` 不要在同一個清單裡放未驗證的退路
- 做法：用**分開的** `src:` 宣告做漸進增強：先寫純 `url()`，再寫只有 `cross-origin()`／`referrer-policy()` 的版本，最後寫含 `integrity()` 的版本
- 對手：把驗證版與未驗證版寫在同一個逗號分隔的 `src` 裡，CDN 送來被竄改的字型時，驗證失敗被當成載入失敗，瀏覽器自動改用第二個未驗證的網址（引用："in a single `src` descriptor bypasses Subresource Integrity at runtime"）
- 退路：保住主要行為——不支援的瀏覽器會丟掉整條含修飾子的宣告，前面的純 `url()` 仍會生效，字型照常載入
- 解鎖：（缺）

經過：為了相容多寫一個退路，結果退路成了後門：驗證一失敗，瀏覽器乖乖去載未驗證的同一個檔案。
%% line-end %%

### 細節（不索引）
- 對手組：新功能的副作用
- 支援狀態：同 mwg:secure-external-subresources:3，記 Limited
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:secure-external-subresources:5" %%
## 外部資源設 `referrerpolicy="no-referrer"`，文件層再設基準政策
- 做法：文件送 `Referrer-Policy: strict-origin-when-cross-origin`（或 `<meta name="referrer">`）當基準；第三方 CDN 的 `<script>`、`<link>` 加 `referrerpolicy="no-referrer"`，`fetch()` 傳 `referrerPolicy`
- 對手：請求第三方主機時，`Referer` 標頭把來源或路徑資訊洩漏出去（引用："Overrides the document referrer policy to prevent leaking any origin or path information in the `Referer` request header to the third-party host."）
- 退路：不需要——`referrerpolicy` 與 `Referrer-Policy` 早已 Widely，不必退路
- 解鎖：（缺）

經過：每個從 CDN 載的檔案都順便告訴 CDN「使用者正在看哪一頁」。逐個關掉，再用文件層政策兜底。
%% line-end %%

### 細節（不索引）
- 對手組：敏感資料外露
- 支援狀態：同 mwg:secure-external-subresources，記 Widely
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
