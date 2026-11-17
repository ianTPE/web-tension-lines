---
guide: resolution-optimized-pseudo-elements
category: performance
upstream: https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/performance/resolution-optimized-pseudo-elements.md
first_seen: 2026-11-16（v1.0.0，回溯拆出）
license: CC-BY-4.0（上游指南）
---

# 依解析度最佳化的偽元素圖片

%% line-start id="mwg:resolution-optimized-pseudo-elements" %%
## 在 `::before`／`::after` 裡用 `image-set()` 讓瀏覽器挑格式與解析度
- 做法：裝飾圖示放在偽元素的 `content` 或 `background-image`，用 `image-set()` 列出 AVIF／WebP／PNG 與 1x／2x，格式由最佳化到最不佳化排序；前面先寫一行一般的 `url()` 當舊瀏覽器的退路
- 對手：指南只說這樣不必為裝飾圖示多加 DOM 節點、瀏覽器能挑最適合裝置的圖，沒說單一 `url()` 或額外節點在哪個時刻出問題（引用："allows you to add decorative icons or structural graphics without cluttering your HTML with extra DOM nodes."）
- 退路：不需要——`image-set()` 已 Widely（前一行寫 `url()` 可為極舊瀏覽器保底）
- 解鎖：（缺）

經過：圖示按鈕的小圖要兼顧高解析螢幕與新格式，以前得多放 `<img>` 或只給一張。寫進偽元素的 `image-set()`，HTML 不變，瀏覽器自己挑。
%% line-end %%

### 細節（不索引）
- 對手組：載入超過需要的資源
- 支援狀態：image-set()：Widely available（2023-09-18）。Supported by: Chrome 113, Edge 113, Firefox 89, Safari 17
- 戰報：勝（由支援狀態與退路推出）
- 槽判定：對手 有／解鎖 缺
- 類型：糾錯
- 另有 2 個糾錯提醒未拆（格式必須由 AVIF 往 PNG 排，瀏覽器停在第一個支援的格式；舊瀏覽器要先寫一行一般 `url()` 退路）
- 變更紀錄：2026-11-16（v1.0.0）回溯拆出；2026-11-18 改為槽 v2
