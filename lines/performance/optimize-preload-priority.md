---
guide: optimize-preload-priority
category: performance
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/performance/optimize-preload-priority.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 最佳化預載優先序

%% line-start id="mwg:optimize-preload-priority" %%
## 用 <link rel=preload fetchpriority="high"> 讓預載的關鍵圖片不再以低優先序排隊
- 做法：對瀏覽器不會及早發現、但畫面必需的圖片（影片海報、CSS 背景裡的英雄圖）用 `<link rel="preload" as="image" fetchpriority="high">`；次要字型、背景影片的預載用 `fetchpriority="low"`
- 對手：預載沿用該資源類型的預設優先序，圖片的預設是低優先（引用："However, preloads inherit the default priority for the resource type and for images in particular this is low."）
- 退路：失去主要好處——不支援時忽略 `fetchpriority`，預載圖片仍沿用該類型的預設低優先序
- 解鎖：在 `<link rel=preload>` 加 `fetchpriority`，覆寫資源預設優先序讓關鍵圖提早下載

經過：好不容易用 preload 讓瀏覽器提早知道英雄背景圖，它卻被排在低優先，跟其他資源搶不贏。加上 `fetchpriority="high"`，提早發現也提早下載。
%% line-end %%

### 細節（不索引）
- 對手組：載入優先序錯置
- 支援狀態：Fetch priority：Newly available（2024-10-29）。Supported by: Chrome 103, Edge 103, Firefox 132, Safari 17.2
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：首屏是影片或 CSS 背景圖的落地頁，可以讓海報圖或背景圖跟一般 `<img>` 英雄圖一樣搶到第一順位，不必為了 LCP 改掉設計
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:optimize-preload-priority:2" %%
## 預載太多會彼此搶頻寬，as 寫錯預載就白費
- 做法：整頁預載最多約 2 張圖、2～3 個必要字型，`fetchpriority="high"` 最多給 1～2 個；正確寫 `as` 與 `type`；能放進 HTML `<img>` 的關鍵圖就不要靠預載
- 對手：預載數量過多造成頻寬互搶；`as` 不正確時預載不會被使用（引用："DO: Limit the total number of preloads on a page to at most 2 images and 2-3 essential fonts to prevent bandwidth contention."）
- 退路：保住主要行為——不支援 `fetchpriority` 時仍須控制預載數量與正確 `as`，避免互搶或白抓
- 解鎖：（缺）

經過：什麼都 preload 等於什麼都沒 preload，大家一起搶頻寬；`as` 寫錯，預載抓下來的東西頁面用不上，等於白抓。
%% line-end %%

### 細節（不索引）
- 對手組：載入優先序錯置
- 支援狀態：Fetch priority：Newly available（同上）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 2 個糾錯提醒未拆（字型預載一律加 `crossorigin`、不用已棄用的 `importance` 屬性）
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
