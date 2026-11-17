---
guide: deliver-optimized-decorative-images
category: performance
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/performance/deliver-optimized-decorative-images.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 提供最佳化的裝飾圖片

%% line-start id="mwg:deliver-optimized-decorative-images" %%
## 用 image-set() 讓 CSS 背景圖也能依格式與解析度挑最小的檔
- 做法：在 `background-image`、`mask-image`、`content` 用 `image-set()` 列出 AVIF／WebP／JPEG 各自的 `1x`、`2x`，由最佳化程度高的格式排到低
- 對手：缺——指南只說這能改善感知效能、瀏覽器會挑最小的合用圖，沒說只寫單一 `url()` 在哪個時刻出問題
- 退路：不需要——`image-set()` 已 Widely（前一行寫單一圖檔可為極舊瀏覽器保底）
- 解鎖：（缺）

經過：CSS 的裝飾圖以前只能寫一個網址，高解析螢幕與新格式都顧不到。`image-set()` 讓 CSS 圖片也有 `srcset` 般的選擇。指南沒有描述單一網址的具體代價。
%% line-end %%

### 細節（不索引）
- 對手組：載入超過需要的資源
- 支援狀態：image-set()：Widely available（2023-09-18）。Supported by: Chrome 113, Edge 113, Firefox 89, Safari 17
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2

%% line-start id="mwg:deliver-optimized-decorative-images:2" %%
## 可能成為 LCP 的大圖不要只放在 CSS 的 image-set() 裡
- 做法：英雄橫幅這類 LCP 候選圖改用 HTML 的 `<img>` 或 `<picture>`，或另外用帶 `media` 的 `<link rel=preload>` 預載
- 對手：CSS 裡 `image-set()` 引用的圖片，瀏覽器的預載掃描器找不到，載入被大幅延後、拖累 LCP（引用："images referenced in CSS via image-set() are not discoverable by the browser's preload scanner. This can significantly delay image loading and harm LCP."）
- 退路：不需要——`image-set()` 與 `<img>` 等替代做法均已 Widely，不必退路
- 解鎖：（缺）

經過：首屏大圖寫成 CSS 背景，瀏覽器要等樣式表下載、套用到元素後才知道要抓它，LCP 被往後推。搬回 HTML 或預載，它就在最早的時間點開始下載。
%% line-end %%

### 細節（不索引）
- 對手組：載入優先序錯置
- 支援狀態：image-set()：Widely available（同上）；`<img>`、`<picture>`、`<link rel=preload>` 指南未列支援資料
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 2 個糾錯提醒未拆（格式由最佳化程度高排到低、在 `image-set()` 前寫一般宣告當 fallback），都是 CSS 層疊的常識性提醒
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
