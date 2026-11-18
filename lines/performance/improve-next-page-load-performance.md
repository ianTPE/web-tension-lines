---
guide: improve-next-page-load-performance
category: performance
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/performance/improve-next-page-load-performance.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 加快下一頁的載入

%% line-start id="mwg:improve-next-page-load-performance" %%
## 用 Speculation Rules 在使用者點下去之前先預取或預渲染下一頁
- 做法：在 `<script type="speculationrules">` 寫 `prefetch`／`prerender` 規則，優先用 `where` 的 document rule 以 `href_matches`／`selector_matches` 選連結，配合 `eagerness`（`immediate`／`eager`／`moderate`／`conservative`），可加 `tag` 讓伺服器從 `Sec-Speculation-Tags` 辨識
- 對手：缺——指南只說在使用者造訪前先開始載入下一頁是改善載入效能最有效的方法之一，沒說不這麼做時具體出了什麼事
- 退路：失去主要好處——Firefox 與 Safari 忽略規則並照常點擊載入，失去預取與預渲染加速
- 解鎖：用 `<script type="speculationrules">` 宣告規則，讓瀏覽器在點擊前先預取或預渲染下一頁

經過：規則讓瀏覽器在使用者停在連結上、甚至一進頁面就先抓好或渲染好下一頁，可以先 eager 預取、等互動訊號再 moderate 預渲染。這是純粹的漸進增強，不支援的瀏覽器沒有任何好處。
%% line-end %%

### 細節（不索引）
- 對手組：載入優先序錯置
- 支援狀態：Speculation rules：Limited availability。Supported by: Chrome 109, Edge 109；Unsupported in: Firefox, Safari
- 戰報：僵持（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：線上課程、說明文件、分步驟表單的「下一步」可以預渲染好，按下去畫面就在，靜態網站不必改成 SPA 也有瞬間換頁的手感。目前僅 Chromium
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:improve-next-page-load-performance:2" %%
## 不要預載會改變狀態的網址，動態頁面小心過期內容
- 做法：document rule 裡用 `not` 排除 `/logout`、`add-to-cart` 這類網址、後台路徑與標了 `.do-not-prerender` 或 `rel~=nofollow` 的連結；內容常變的動態頁面慎用 prerender 與高 eagerness
- 對手：預載會觸發狀態改變的網址；動態頁面預載的內容可能已經過期（引用："DO NOT speculate URLs that likely trigger state changes, like `/logout` or `/add-to-cart`, and explicitly exclude them from your speculation rules if they are likely to be included in document rules."）
- 退路：保住主要行為——Firefox 與 Safari 忽略預載規則，不會在點擊前誤觸發狀態改變
- 解鎖：（缺）

經過：一條 `href_matches: "/*"` 的規則把頁面上所有同源連結都納入，登出、加入購物車也在裡面，使用者沒有點，這些網址就可能被預先請求。排除清單是寬鬆規則的必要配件。
%% line-end %%

### 細節（不索引）
- 對手組：動作被意外觸發
- 支援狀態：Speculation rules：Limited availability（同上）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 2 個糾錯提醒未拆（不要對每個連結都預載，非 eager 的預載有 2 個上限；SPA 不適用 speculation rules）
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2；2026-11-18 對手組由「新功能的副作用」改為「動作被意外觸發」
