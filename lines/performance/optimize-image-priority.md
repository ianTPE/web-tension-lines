---
guide: optimize-image-priority
category: performance
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/performance/optimize-image-priority.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 最佳化圖片優先序

%% line-start id="mwg:optimize-image-priority" %%
## 用 fetchpriority 告訴瀏覽器哪張圖是 LCP、哪些藏著的圖可以晚點
- 做法：對 LCP 候選圖（通常是頂端英雄圖）加 `fetchpriority="high"`；對技術上在首屏、但一開始看不到的圖（輪播的隱藏投影片、大型選單裡的圖）加 `fetchpriority="low"`
- 對手：瀏覽器用啟發式規則分配圖片優先序，預設值不一定對得上頁面的 LCP（引用："Browsers use heuristics to assign loading priorities to images, but these defaults may not always align with your page's Largest Contentful Paint (LCP)."）
- 退路：失去主要好處——不支援時忽略該屬性而退回瀏覽器預設啟發式規則，失去手動調度優先序
- 解鎖：用 `fetchpriority` 主動告知瀏覽器 LCP 圖先抓、隱藏首屏圖延後，減少頻寬爭搶

經過：英雄圖和輪播裡其他五張投影片、選單裡的促銷圖在瀏覽器眼中差不多重要，一起排隊。標出哪張最重要、哪幾張只是先藏著，頻寬就先給真正被看到的那張。
%% line-end %%

### 細節（不索引）
- 對手組：載入優先序錯置
- 支援狀態：Fetch priority：Newly available（2024-10-29）。Supported by: Chrome 103, Edge 103, Firefox 132, Safari 17.2
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 有
- 類型：新能力
- 發想（非指南原文）：首屏塞了輪播、選單圖、頭像的首頁，可以只用 HTML 屬性排出「主圖先、其他後」的下載順序，不必為了 LCP 把輪播改成只放一張圖
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:optimize-image-priority:2" %%
## fetchpriority 標錯對象：high 太多、low 給了首屏以下的 lazy 圖
- 做法：`fetchpriority="high"` 最多給 1～2 張關鍵圖，且不與 `loading="lazy"` 並用；首屏以下的一般圖片只用 `loading="lazy"`，不加 `fetchpriority="low"`；LCP 圖不加 `loading="lazy"`
- 對手：`high` 給太多張會互搶網路、稀釋提升效果；首屏以下的 lazy 圖若再標 `low`，使用者捲到時它們不會以正常優先序載入（引用："Only use `fetchpriority="high"` on at most 1-2 critical images to avoid network contention and diluting the priority boost."）
- 退路：保住主要行為——不支援 `fetchpriority` 的瀏覽器自動忽略，一般圖片仍正常使用 `loading="lazy"`
- 解鎖：（缺）

經過：拿到新屬性的直覺是每張重要的圖都標 high、其他全部標 low，結果 high 彼此抵銷，捲到下方時圖片又慢吞吞。優先序是相對的，只有少數幾張被提升才有意義。
%% line-end %%

### 細節（不索引）
- 對手組：載入優先序錯置
- 支援狀態：Fetch priority：Newly available（同上）
- 戰報：部分改善（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 3 個糾錯提醒未拆（不用 `fetchpriority="auto"`、不用已棄用的 `importance` 屬性、不用已移除的 `loading="auto"`）
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
