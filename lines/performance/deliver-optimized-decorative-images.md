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
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：在 `background-image`、`mask-image`、`content` 用 `image-set()` 列出 AVIF／WebP／JPEG 各自的 `1x`、`2x`，由最佳化程度高的格式排到低
- 被什麼擋：缺——指南只說這能改善感知效能、瀏覽器會挑最小的合用圖，沒說只寫單一 `url()` 在哪個時刻出問題
- 戰報：勝——瀏覽器依支援的格式與裝置像素密度挑出最小的合用圖；舊瀏覽器在前面多寫一條普通的 `background-image` 當 fallback（官方宣稱）

經過：CSS 的裝飾圖以前只能寫一個網址，高解析螢幕與新格式都顧不到。`image-set()` 讓 CSS 圖片也有 `srcset` 般的選擇。指南沒有描述單一網址的具體代價。
%% line-end %%

### 細節（不索引）
- 對手組：載入超過需要的資源
- 支援狀態：image-set()：Widely available（2023-09-18）。Supported by: Chrome 113, Edge 113, Firefox 89, Safari 17
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 缺／戰報 有
- 類型：糾錯
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出

%% line-start id="mwg:deliver-optimized-decorative-images:2" %%
## 可能成為 LCP 的大圖不要只放在 CSS 的 image-set() 裡
- 誰在做：開發者（或寫程式的代理）
- 動作＋對象：英雄橫幅這類 LCP 候選圖改用 HTML 的 `<img>` 或 `<picture>`，或另外用帶 `media` 的 `<link rel=preload>` 預載
- 被什麼擋：CSS 裡 `image-set()` 引用的圖片，瀏覽器的預載掃描器找不到，載入被大幅延後、拖累 LCP（引用："images referenced in CSS via image-set() are not discoverable by the browser's preload scanner. This can significantly delay image loading and harm LCP."）
- 戰報：勝——放在 HTML 或預載後，預載掃描器在解析 HTML 時就發現圖片並開始下載（官方宣稱）

經過：首屏大圖寫成 CSS 背景，瀏覽器要等樣式表下載、套用到元素後才知道要抓它，LCP 被往後推。搬回 HTML 或預載，它就在最早的時間點開始下載。
%% line-end %%

### 細節（不索引）
- 對手組：載入優先序錯置
- 支援狀態：image-set()：Widely available（同上）；`<img>`、`<picture>`、`<link rel=preload>` 指南未列支援資料
- 槽判定：誰在做 有／動作＋對象 有／被什麼擋 有／戰報 有
- 類型：糾錯
- 另有 2 個糾錯提醒未拆（格式由最佳化程度高排到低、在 `image-set()` 前寫一般宣告當 fallback），都是 CSS 層疊的常識性提醒
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出
